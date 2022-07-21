UPDATE `objects`
	SET `maker_role` = REPLACE(`maker_role`, '|        |', '')
	WHERE `maker_role` LIKE '%|        |%' and maker_full_name not like '%|%' and institution_name in ('Peabody Museum of Archaeology and Ethnology');

update objects set maker_role = REPLACE(maker_role, '\n', ' ') where maker_role like '%\n%' and institution_name in ('Peabody Museum of Archaeology and Ethnology');

select maker_full_name, maker_role from objects where maker_full_name like '%|%' and institution_name in ('Peabody Museum of Archaeology and Ethnology');

UPDATE `objects`
	SET `maker_role` = REPLACE(`maker_role`, '|        |         ', '|')
	WHERE `maker_role` LIKE '%|        |         %' and institution_name in ('Peabody Museum of Archaeology and Ethnology');
