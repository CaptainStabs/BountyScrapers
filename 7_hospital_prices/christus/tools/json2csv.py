import csv
import pandas as pd
import os
import json


for file in os.listdir("./input_files/"):
    if file.endswith('.json'):
        print(file)
        filename = file.replace(".json", ".csv")
        if not os.path.exists(f"./output_files/{filename}"):
            df = pd.read_json(f"./input_files/{file}", dtype=str, encoding="iso-8859-1", lines = True)
            df = df[df.columns.difference(['disclaimer'])]
            df = df.reindex(columns=["file_create_date", "run_id", "name", "tax_id", "code", "code type", "code description", "payer", "patient_class", "gross charge", "de-identified minimum negotiated charge", "de-identified maximum negotiated charge", "payer-specific negotiated charge", "discounted cash price"])
            df.to_csv(f"./output_files/{filename}", index=False)
