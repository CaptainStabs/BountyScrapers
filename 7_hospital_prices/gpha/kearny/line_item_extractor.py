import csv
from tqdm import tqdm
import traceback as tb

payer_dict = {
"Price": "GROSS CHARGE",
"De-Identified Minimum Outpatient Allowable Rate": "MIN",
"De-Identified Maximum Outpatient Allowable Rate": "MAX",
"De-Identified Minimum Inpatient Allowable Rate": "MIN",
"De-Identified Maximum Inpatient Allowable Rate": "MAX"
}

# Gross Charge,Discounted Cash Price,De-identified minimum negotiated charge,De-identified maximum negotiated charge,Blue_PPO,PROVIDRS_CARE_
columns = ["cms_certification_num", "payer", "code", "internal_revenue_code", "description", "price", "inpatient_outpatient", "code_disambiguator", "units"]
with open("KCH_Online_Posting_Line_Item_CDM.csv", "r", encoding="utf-8") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    header = input_csv.readline().split(",")
    insurance = header[(header.index("De-Identified Minimum Outpatient Allowable Rate")):-1]
    insurances = [x.replace("\n", "") for x in insurance]
    insurances.append("Price")
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("line_extracted.csv", "a", newline="", encoding="utf-8") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        # Price,,MODIFIER_1,MODIFIER_2,,,,,Medicare Outpatient Allowable Rate,Medicare Inpatient Allowable Rate,Blue Cross Outpatient Allowable Rate,Blue Cross Inpatient Allowable Rate,United Healthcare Outpatient Allowable Rate,United Healthcare Inpatient Allowable Rate,Cigna Outpatient Allowable Rate,Cigna Inpatient Allowable Rate,Aetna Outpatient Allowable Rate,Aetna Inpatient Allowable Rate,WPPA Inc Outpatient Allowable Rate,WPPA Inc Inpatient Allowable Rate Per Day
        for row in tqdm(reader, total=line_count):
            try:
                price_info = {
                    "cms_certification_num": "171313",
                    # "code": str(row["Procedure Code"]).upper(),
                    "internal_revenue_code": row["RevCode"],
                    "units": str(row["UnitofMeasure"]).strip(),
                    "description": " ".join(str(row["ChargeDesc"]).upper().split()),
                    "code_disambiguator": str(row["ChargeID"]).strip()
                }

                code = str(row["CPT_CODE"]).strip()

                if code:
                    price_info["code"] = code
                else:
                    price_info["code"] = "NONE"

                if not str(price_info["internal_revenue_code"]).strip():
                    price_info["internal_revenue_code"] = "NONE"

                for payer in insurances:
                    inpatient_outpatient = str(payer).upper()
                    if "INPATIENT" in inpatient_outpatient:
                        price_info["inpatient_outpatient"] = "INPATIENT"
                    elif "OUTPATIENT" in inpatient_outpatient:
                        price_info["inpatient_outpatient"] = "OUTPATIENT"
                    else:
                        price_info["inpatient_outpatient"] = "UNSPECIFIED"

                    price_info["price"] = row[payer].replace("$","").replace(",", "").strip()

                    try:
                        price_info["payer"] = payer_dict[payer]
                    except KeyError:
                        if "Inpatient" in payer:
                            payer = payer.split("Inpatient")[0]
                        elif "Outpatient" in payer:
                            payer = payer.split("Outpatient")[0]

                        price_info["payer"] = payer.strip()

                    if str(price_info["price"]) and str(price_info["price"]) != "N/A":
                        if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                            writer.writerow(price_info)
                        else:
                            import json; print(json.dumps(price_info, indent=2))
            except ValueError:
                tb.print_exc()
