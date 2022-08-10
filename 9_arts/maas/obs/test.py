# import json
# from numpy import unique
#
# with open("json_test2.json", "r") as f:
#     jd = json.load(f)
#
# events = jd['events']
# dates = "|".join([x['date'] for x in events if not isinstance(x['date'], type(None))])
# places = "|".join(unique([x['place'] for x in events]))
# print(dates)
# print(places)
#
#
# print(isinstance(jd["events"][0]["date"], type(None)))
# # print("|".join([x['date'] for x in a["events"] if not isinstance(x, type(None))]))

arguments = []
end_id = 199999
# start_num is supplemental for first run and is only used if the files don't exist
for i in range(5):
    if i == 0:
        start_num = 0
    else:
        # Use end_id before it is added to
        start_num = end_id - 199999
    print("Startnum: " + str(start_num))
    arguments.append((f"./files/extracted_data{i}.csv", start_num, end_id))
    end_id = end_id + 199999
print(arguments)
