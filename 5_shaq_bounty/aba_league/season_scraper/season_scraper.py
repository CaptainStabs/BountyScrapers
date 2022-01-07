import csv

input_columns = ["season_id"]
output_columns = ["league_id", "season_id"]

with open("aba_seasons.csv", "r", encoding="utf-8") as input_csv:
    reader = csv.DictReader(input_csv, input_columns)

    with open("aba_seasons_output.csv", "a", encoding="utf-8", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, output_columns)
        for i, row in enumerate(reader):
            if i == 0:
                continue

            output_dict = {
                "league_id": "1",
                "season_id": row["season_id"][:-3],
            }

            writer.writerow(output_dict)
