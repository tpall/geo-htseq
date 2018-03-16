#!/bin/bash

output/suppdata.rds: R/_common.R output/document_summaries.rds output/gsem.rds lib/munge_geo.R lib/checkFullRank.R lib/text_funs.R

	Rscript R/A06_munge_suppfiles.R

output/gsem.rds: R/_common.R

	Rscript R/A05_munge_series_matrixfiles.R


	Rscript R/A04_download_suppfiles.R

output/supfilenames_filtered.rds output/supfilenames_filtered.txt: R/_common.R output/suppfilenames.rds R/out_strings.R

	Rscript R/A03_filter_suppfilenames.R

output/suppfilenames.rds: output/document_summaries.rds R/A02_download_suppfilenames.R R/_common.R

	Rscript R/A02_download_suppfilenames.R

output/document_summaries.rds: R/A01_GEO_query.R

	Rscript R/A01_GEO_query.R