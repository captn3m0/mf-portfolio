hdfc:
	curl --silent "https://cms.hdfcfund.com/en/hdfc/api/v2/investor/weeklyDetails" \
  		--header 'referer: https://www.hdfcfund.com' | jq --raw-output '.data.filesData[]|.url' \
  		| wget --input-file=- --directory-prefix=raw_data/hdfc/ --no-clobber --no-verbose
