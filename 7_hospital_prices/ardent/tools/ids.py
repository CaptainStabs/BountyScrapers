# ids = [170016,320009,320017,320074,320086,323028,370001,370015,370039,370099]
#
# with open("hospitals.csv", "r") as f:
#
#   real_id = []
#
#   for line in f:
#     real_id.append(line.split(",")[0])
#
#   print(real_id)
#   for id in ids:
#     if id not in real_id:
#     print(id)


ids = ['370228', '450231', '370183',  '370202', '670080', '370216',  '450389', '450210', '450475', '450194', '450690', '451367', '451380', '453072', '452051', '450083']

for id in ids:
    print(f"delete from prices where cms_certification_num = '{id}';")
