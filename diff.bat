@echo off
for %%x in ('030006', '050468', '060011', '040020', '050028', '060024', '050641', '050663', '050060', '040027', '050771', '050780', '060020', '051334', '060049', '060003', '050091', '050122', '060104', '050135', '010087', '050245', '060114', '013301', '041307', '060118', '060132', '070027', '061326', '070029', '110100', '060124', '060125', '062011', '061312', '063301', '060129', '072003', '063303', '070012', '060130', '060131', '111305', '140015', '140095', '140049', '141305', '141315', '131314', '141324', '141338', '150007', '150074', '150128', '170023', '150082', '180056', '200037', '180087', '180088', '150048', '170110', '230017', '150169', '190167', '201312', '150113', '201315', '194069', '151319', '200021', '230024', '161381', '230081', '230097', '230303', '231332', '260025', '230058', '241332', '241371', '241336', '241381', '240022', '241347', '230104', '231301', '241354', '230085', '240100', '230075', '244015', '231322', '260034', '230273', '241302', '241303', '230277', '241304', '241315', '241369', '241328', '270057', '300020', '300017', '271344', '310069', '320004', '281313', '281319', '281334', '330157', '281338', '281357', '301302', '263303', '281359', '330166', '340069', '331314', '340173', '350011', '360068', '361301', '390032', '360125', '361318', '350015', '361328', '351302', '351329', '360259', '390050', '390057', '390081', '390090', '390160', '390097', '390146', '390266', '390180', '390267', '410005', '430027', '420053', '430097', '431305', '431307', '431309', '431311', '431329', '431333', '431334', '431336', '400021', '450040', '450604', '450678', '500015', '451300', '501330', '520063', '520103', '450133', '451330', '503301', '500037', '500129', '471306', '451391', '511300', '450587', '511301', '521341', '530014', '673057') do dolt diff HPI multi-code-fix prices --limit 1 --where=cms_certification_num=%%x
