update hospitals as h1 set chargemaster_direct_url=(select chargemaster_direct_url from hospitals as of '5if2rhvg8sd61deerdsl87saed4t0mjr' where name=h1.name and ccn=h1.ccn and state_code=h1.state_code

dolt sql -q "select * from hospitals where chargemaster_direct_url not REGEXP '\.json|\.csv|\.xml|\.xls|\.xlx|\.xlsx|\.pdf|\.ashx|cdmpricing|apps\.para-hcfs|hospitalpriceindex|\.zip|\.txt|rackcdn\.com|portalapprev|hospitalpricedisclosure|gundersenhealth\.org|\.aspx' order by homepage_url;" -r csv > check_urls.csv


update hospitals as h1 set chargemaster_direct_url=(select chargemaster_direct_url from hospitals as of 'mi3gjf6rle9cni2j37jq5711r09tq0kj' where name=h1.name and ccn=h1.ccn and state_code=h1.state_code and name like '%PROVIDENCE'
