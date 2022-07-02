

a = {
    "inscriptions": {
        "primary": "A",
        "secondary": "B"
    }
}

insc = a["inscriptions"]
print("|".join([x for x in [insc["primary"], insc["secondary"]] if x]),)

jd = {
"persons": [
{
    "sex": None,
    "birthDate": None,
    "fullName": "Wet-Colodian",
    "organisation": "Wet-Colodian",
    "multimedia": [],
    "personTitle": None,
    "firstName": None,
    "irn": 793,
    "isPublished": "Yes",
    "nationality": None,
    "partyType": "Organisation",
    "lastName": None
},
{   "sex": None,
    "birthDate": None,
    "fullName": "Wet-Colodian",
    "organisation": "Wet-Colodian",
    "multimedia": [],
    "personTitle": None,
    "firstName": None,
    "irn": 793,
    "isPublished": "Yes",
    "nationality": None,
    "partyType": "Organisation",
    "lastName": None},]}
print("|".join([x["fullName"] for x in jd["persons"]]))

jd = {"multimedia": [
    {
      "MulIdentifier": "149266h.jpg",
      "summaryData": "149266h (image/jpeg)",
      "title": "149266h",
      "isPublished": "yes",
      "irn": 15803,
      "MulMimeType": "image",
      "identifier": "149266h.jpg",
      "mimeType": "image",
      "path": "15/803/",
      "rights": {}
    }
    ]
}
media = jd["multimedia"][0]
if media:
    img_path = media["path"]
    name = media["MulIdentifier"]



url = "https://hsm-online-collections-assets-prod.s3.eu-west-1.amazonaws.com/emu/emumultimedia/multimedia/"
print("".join([url, img_path, name]))
