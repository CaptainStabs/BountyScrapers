prov_stuff = ['Collector Name', 'Donor Name']
prov_role = ['Collector', 'Donor']

result = [f'{prov_role[i]}: {prov_stuff[i]}' for i in range(len(prov_role))]
print(result)
