import ftplib
import os
import re
import argparse


def chunks(lst, size):
    """Yield successive n-sized chunks from lst."""
    n = len(lst) // size
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def download_suppfiles(input, email, size=200):
    p = re.compile("GSE\\d+")
    with open(input, "r") as i:
        filenames = i.readlines()
    filenames = chunks(filenames, size)
    for chunk in filenames:
        with ftplib.FTP("ftp.ncbi.nlm.nih.gov") as ftp:
            try:
                ftp.login("anonymous", email)
                for line in chunk:
                    path = "output/" + line.rstrip()
                    if not os.path.isfile(path):
                        filename = os.path.basename(path)
                        id = p.search(filename).group(0)
                        dir = (
                            "/geo/series/"
                            + id[0:-3]
                            + "nnn/"
                            + id
                            + "/"
                            + os.path.dirname(line.rstrip())
                        )
                        ftp.cwd(dir)
                        if ftp.size(filename) < 1e9:
                            with open(path, "wb") as file:
                                ftp.retrbinary("RETR " + filename, file.write, 1024)
            except ftplib.all_errors as e:
                print("FTP error:", e)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", metavar="FILE", help="input file with list of files to be downloaded"
    )
    parser.add_argument(
        "--email", metavar="EMAIL", help="email address for anonymous FTP"
    )
    parser.add_argument("--size", metavar="INT", help="batch size")
    args = parser.parse_args()

    download_suppfiles(**args.__dict__)
