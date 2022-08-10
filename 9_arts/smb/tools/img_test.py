import requests

def image_get(id):
    url = "https://api.smb.museum/v1/graphql"

    payload = "{\"query\":\"query FetchPrimaryAttachmentsForObjects($object_ids: [bigint!]!) {\\n  smb_objects(where: {id: {_in: $object_ids}}) {\\n    id\\n    attachments(order_by: [{primary: desc}, {attachment: asc}], limit: 1) {\\n      attachment\\n    }\\n  }\\n}\\n\",\"variables\":{\"object_ids\":[" + str(id) + "]},\"operationName\":\"FetchPrimaryAttachmentsForObjects\"}"
    headers = {
      'host': 'api.smb.museum',
      'Content-Type': 'text/plain'
    }

    r = requests.request("POST", url, headers=headers, data=payload)
    r = r.json()

    data = r["data"]["smb_objects"]

    if data:
        f = data[0]["attachments"]
        if f:
            img = f[0]["attachment"].strip(".jpg")
            img = "".join(["https://recherche.smb.museum/images/", img, "_1000x600.jpg"])
            return img


print(image_get(2553990))
