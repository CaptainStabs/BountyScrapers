Step 1; Cleaning Cities:
1. Get all `city_registered` with a comma in it

  ```mysql
  select * from businesses where city_registered like "%,%";```

2. Setup `comma_cleaning.py`
3. Import resulting csv file into database
4. Remove trailing commas:
  ```mysql
  UPDATE businesses SET city_physical = SUBSTRING(city_physical, 1, char_length(city_physical) -1) where city_physical like '%,';
  ```

5. Repeat for `city_physical`

SQL Log:
UPDATE businesses set city_registered = "NEW YORK" where city_registered = "NY" and state_registered = "NY";

UPDATE businesses set city_registered = NULL WHERE city_registered = "FL" and state_registered = "FL";

UPDATE businesses set city_registered = "BROOKLYN" where city_registered = "BK" and state_registered = "NY";

UPDATE businesses set city_registered = "ALDEN" where city_registered = "A" and state_registered = "NY";
UPDATE businesses set city_registered = "STATEN ISLAND" where city_registered = "SI" and state_registered = "NY";

UPDATE businesses set city_registered = "GRAND JUNCTION" where city_registered = "GJ" and state_registered = "CO";

UPDATE businesses set city_registered = "ST. PETERSBURG" where city_registered = "ST" and state_registered = "FL";

UPDATE businesses set city_registered = NULL WHERE city_registered = state_registered;

UPDATE businesses set city_registered = NULL WHERE state_registered = city_registered;

UPDATE businesses set city_registered = NULL WHERE CHAR_LENGTH(city_registered) = 1;

UPDATE businesses set city_registered = "ST. PETERSBURG" where city_registered = "ST" and state_registered = "FL";

UPDATE businesses set city_registered = "TAMARAC" where city_registered = "TA" and state_registered = "FL";

UPDATE businesses set city_registered = "TAMARAC" where city_registered = "TA" and state_registered = "FL";

UPDATE businesses set city_registered = "NEW YORK" where city_registered = "NE" and state_registered = "NY";

UPDATE businesses set city_registered = "COLUMBUS" where city_registered = "CO" and state_registered = "GA";

UPDATE businesses set city_registered = "PANAMA CITY" where city_registered = "PC" and state_registered = "FL";

UPDATE businesses set city_registered = "FOREST HILLS" where city_registered = "FH" and state_registered = "NY";

UPDATE businesses set city_registered = "CROSS LANES" where city_registered = "C." and state_registered = "WV";

UPDATE businesses set city_registered = "SAN FRANCISCO" where city_registered = "SF" and state_registered = "CA";

UPDATE businesses set city_registered = "BRADENTON" where city_registered = "@@" and state_registered = "FL";

UPDATE businesses set city_registered = "GLENNVILLE" where city_registered = "GL" and state_registered = "GA";

UPDATE businesses set city_registered = "ORLANDO" where city_registered = "36" and state_registered = "FL";

UPDATE businesses set city_registered = "BRONX" where city_registered = "BX" and state_registered = "NY";

update businesses set city_physical = "LOS ANGELES" where city_physical = "LA" and state_physical = "CA";

update businesses set street_registered = NULL where street_registered = street_registered;

update businesses set street_registered = NULL where street_registered = "NONE";

update businesses set city_registered = NULL where city_registered = "NONE";
update businesses set city_registered = NULL where city_registered = "NAN";

update businesses set zip5_registered = NULL where zip5_registered = "NAN";
update businesses set zip5_registered = NULL where zip5_registered = "NULL";
update businesses set zip5_registered = NULL where zip5_registered = "NONE";
update businesses set zip5_physical = NULL where zip5_physical = "NAN";
update businesses set zip5_physical = NULL where zip5_physical = "NULL";
update businesses set zip5_physical = NULL where zip5_physical = "NONE";
update businesses set city_registered = NULL where city_registered = "NAN";
update businesses set street_physical = NULL where street_physical = "NULL";
update businesses set street_registered = NULL where street_registered = "NULL";
update businesses set city_registered = NULL where city_registered = "NULL";
update businesses set city_physical = NULL where city_physical = "NULL";
update businesses set city_physical = NULL where city_physical = "NAN";
update businesses set city_physical = NULL where city_physical = "NONE";
update businesses set filing_number = NULL where filing_number = "NULL";
update businesses set filing_number = NULL where filing_number = "NONE";
update businesses set filing_number = NULL where filing_number = "NAN";
update businesses set zip5_registered = NULL where zip5_registered = "";
update businesses set zip5_physical = NULL where zip5_physical = "";
update businesses set city_registered = NULL where city_registered = "";
update businesses set street_physical = NULL where street_physical = "";
update businesses set street_registered = NULL where street_registered = "";
update businesses set city_physical = NULL where city_physical = "";
update businesses set filing_number = NULL where filing_number = "";

update businesses set zip5_registered = NULL where zip5_registered = "N/A";
update businesses set zip5_physical = NULL where zip5_physical = "N/A";
update businesses set city_registered = NULL where city_registered = "N/A";
update businesses set street_physical = NULL where street_physical = "N/A";
update businesses set street_registered = NULL where street_registered = "N/A";
update businesses set city_physical = NULL where city_physical = "N/A";
update businesses set filing_number = NULL where filing_number = "N/A";
select * from businesses where LENGTH(city_registered) - LENGTH(REPLACE(city_registered, ' ', '')) >= 2 and street_registered = city_registered;

update businesses set city_registered = NULL where city_registered = name;
update businesses set city_physical = NULL where city_physical = name;
update businesses set street_registered = NULL where street_registered = state_registered;

UPDATE businesses SET city_physical = SUBSTRING(city_physical, 1, char_length(city_physical) -1) where city_physical like '%-';

UPDATE businesses SET street_registered = SUBSTRING(street_registered, 1, char_length(street_registered) -1) where street_registered like '%-';

update businesses set city_registered = "PATERSON" where name = "SENTA-SENATE OF TURKISH AMERICAN ORGANIZATION A NJ NONPROFIT CORPORATION" and business_type = "NONPROFIT" and state_registered = "NJ";

update businesses set street_physical = "631 S.W. 87 CT." where name = "ONELIA AND JUAN FAMILY LIMITED PARTNERSHIP" and business_type = "PARTNERSHIP" and state_registered = "FL";

update businesses set street_physical = "3443 40TH TERRACE E" where name = "INFINITY CLEANING LLC" and business_type = "LLC" and state_registered = "FL";

update businesses set street_physical = "2 WARRIOR WAY" where name = "NP ADVANTAGE, CHARTERED" and business_type = "CORPORATION" and state_registered = "FL";

update businesses set city_physical = NULL where city_physical like "%SELECT%";

UPDATE businesses SET city_physical = SUBSTRING(city_physical, 1, char_length(city_physical) -1) where city_physical like '%,';

UPDATE businesses set city_physical = TRIM(city_physical);

update businesses set city_registered = NULL where city_registered = "NOT ENTERED";

update businesses set city_physical = NULL where city_physical like "% OR %";

update businesses set street_registered = NULL where street_registered = "--";

update businesses set street_physical = NULL where street_physical = '--"';

update businesses set street_physical = "403 COMMERCE LN STE 5" where name = "METASENSE INC." and business_type = "CORPORATION" and state_registered = "NC";

update businesses set street_physical = NULL where street_physical = "-', ALPHARETTA";

update businesses set street_registered = trim(street_registered);
update businesses set city_registered = trim(city_registered);
update businesses set city_physical = trim(city_physical);
update businesses set street_physical = trim(street_physical);

update businesses set street_registered = NULL where street_registered = "";
update businesses set city_registered = NULL where city_registered = "";
update businesses set state_physical = NULL where state_physical = "";
update businesses set street_physical = NULL where street_physical = "";
update businesses set city_physical = NULL where city_physical = "";


UPDATE `businesses`
	SET `street_registered` = REPLACE(`street_registered`, 'AVENUESUITE', ' AVENUE SUITE')
	WHERE `street_registered` LIKE '%AVENUESUITE%'

	UPDATE `businesses`
	SET `street_physical` = REPLACE(`street_physical`, 'AVENUESUITE', ' AVENUE SUITE')
	WHERE `street_physical` LIKE '%AVENUESUITE%'
