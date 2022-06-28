import pandas as pd
import xmltodict
import json


def build_dict(seq, key):
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))

def get_category(jd):
    cats = []
    desc_meta = jd.get("lido:descriptiveMetadata")
    # print(json.dumps(desc_meta, indent=2))
    if desc_meta:
        o_c = desc_meta.get("lido:objectClassificationWrap")
        if o_c:
            # Get lido:objectWorkTypeWrap
            o_c_t = o_c.get("lido:objectWorkTypeWrap").get("lido:objectWorkType")
            if isinstance(o_c_t, list):
                term_list = []
                for x in o_c_t: # Iterate through o_c_t list as x
                    term = x["lido:term"]
                    if isinstance(term, list): # check if term is a list
                        # print(term)
                        t_dict = build_dict(term, "@xml:lang")
                        t = term[t_dict.get("en")["index"]]["#text"] # Find english text
                        term_list.append(t)
                    else:
                        term_list.append(term["#text"])
                        # print("AAA", json.dumps(o_c_t, indent=2))
                cats.append("|".join(term_list))

            else:
                try:
                    cats.append(o_c.get("lido:objectWorkTypeWrap").get("lido:objectWorkType").get("lido:term")[0]["#text"])
                except AttributeError:
                    cats.append(o_c.get("lido:objectWorkTypeWrap").get("lido:objectWorkType").get("lido:term")["#text"])
                except KeyError:
                    cats.append(o_c.get("lido:objectWorkTypeWrap").get("lido:objectWorkType").get("lido:term")["#text"])

            # Get lido:classificationWrap
            c_w = o_c.get("lido:classificationWrap").get("lido:classification")

            if isinstance(c_w, list):
                term_list = []
                for x in c_w:
                    term = x["lido:term"]
                    if isinstance(term, list):
                        # print(term)
                        t_dict = build_dict(term, "@xml:lang")
                        t = term[t_dict.get("en")["index"]]["#text"]
                        term_list.append(t)
                    else:
                        term_list.append(term["#text"])
                        # print("AAA", json.dumps(c_w, indent=2))
                cats.append("|".join(term_list))
                # [print("A", x["lido:term"]) for x in c_w if x["lido:term"]["@xml:lang"] == "en"]
                # b = [x.get("lido:term").get("#text") for x in a if x["lido:term"]["@xml:lang"] == "en"]
                # print("AAAA")
            else:
                try:
                    cats.append(o_c.get("lido:classificationWrap").get("lido:classification").get("lido:term")[0]["#text"])
                except AttributeError:
                    cats.append(o_c.get("lido:classificationWrap").get("lido:classification").get("lido:term")["#text"])
                except KeyError:
                    cats.append(o_c.get("lido:classificationWrap").get("lido:classification").get("lido:term")["#text"])
            # Get
        # o_d = desc_meta.get("lido:objectIdentificationWrap")

        if len(cats) != 2:
            # print(json.dumps(desc_meta, indent=2))
            print("\n", "Not two category")
        return "|".join(cats)
    return

def get_title(jd):
    t_list = []
    title_set = jd.get("lido:descriptiveMetadata").get("lido:objectIdentificationWrap").get("lido:titleWrap")["lido:titleSet"]
    if isinstance(title_set, list):
        for x in title_set:
            if "@lido:type" not in x.keys():
                app_val = x.get("lido:appellationValue")

                if isinstance(app_val, list):
                    for y in app_val:
                        t_list.append(y.get("#text"))
        return "|".join(t_list)
    else:
        title_set = title_set["lido:appellationValue"]

    if isinstance(title_set, list):
        # # print(term)
        t_dict = build_dict(title_set, "@xml:lang")
        t = title_set[t_dict.get("en")["index"]]["#text"] # Find english text
        return t
    else:
        return title_set["#text"]

def get_inscription(jd):
    inscription = jd.get("lido:descriptiveMetadata").get("lido:objectIdentificationWrap").get("lido:inscriptionsWrap")
    if inscription:
        i = inscription.get("lido:inscriptions")
        # print(json.dumps(i, indent=2))
        inscriptions = [x.get("lido:inscriptionTranscription") for x in i if type(x) != str]
        inscriptions = [x for x in inscriptions if x]
        if len(inscriptions):
            return "|".join(inscriptions)
    return None

def get_description(jdm):
    desc_set = jdm.get("lido:objectIdentificationWrap").get("lido:objectDescriptionSet")
    if desc_set:
        return desc_set.get("lido:descriptiveNoteValue").get("#text")

def get_dimensions(jd):
    measures = jd.get("lido:objectIdentificationWrap").get("lido:objectMeasurementsWrap").get("lido:objectMeasurementsSet")
    # print("A",json.dumps(measures, indent=2))
    if measures:
        m_list = []
        unit_list = []

        for x in measures: # iterate through lido:objectMeasurementsSet
            try:
                x = x.get("lido:objectMeasurements").get("lido:measurementsSet")
                success = True
            except AttributeError:
                success = False
                continue

            if isinstance(x, list):
                for u in x:
                    y = u.get("lido:measurementValue")
                    # print("C",sets.get("lido:measurementUnit")[0].get("#text"))
                    units = u.get("lido:measurementUnit")[0].get("#text")
                    m_list.append(y)
                    unit_list.append(units)

            else:
                y = x.get("lido:measurementValue")
                units = x.get("lido:measurementUnit")[0].get("#text")

                unit_list.append(units)
                m_list.append(y)

        if success:
            print("A",unit_list)
            units = " ".join(unit_list)
            print("B", units)
            m = " x ".join([x for x in m_list if str(x)])
            return " ".join([m, units])
        else: return

def get_maker_name(jdm):
    events = jdm.get("lido:eventWrap").get("lido:eventSet")
    # print("A", json.dumps(events, indent=4))
    names = []
    for event in events:
        event = event.get("lido:event")
        event_set = event.get("lido:eventActor", {}).get("lido:actorInRole", {}).get("lido:actor", {}).get("lido:nameActorSet", None)
        if event_set:
            names.append(event_set.get("lido:appellationValue", {}).get("#text", None))

    print(names)
# with open("0.xml", "r", encoding='utf-8') as f:

with open("20.xml", "r", encoding="utf-8") as f:
    dd = xmltodict.parse(f.read())

dd = dd["OAI-PMH"]["ListRecords"]
dd = json.dumps({"data":dd})
dd = json.loads(dd)["data"]

for jd in dd["record"]:
    # print(json.dumps(jd, indent=4))
    header = jd["header"]
    jd = jd["metadata"]["lido:lidoWrap"]["lido:lido"]
    jdm = jd.get("lido:descriptiveMetadata")
    # print(json.dumps(jd.get("lido:descriptiveMetadata").get("lido:objectIdentificationWrap").get("lido:titleWrap")["lido:titleSet"], indent=2))
    data = {
        "institution_name": "Rijksmuseum",
        "institution_city": "Amsterdam",
        "institution_state": "New Holland",
        "institution_country": "Netherlands",
        "institution_latitude": 52.36006965261019,
        "institution_longitude": 4.885229527186643,
        "object_number": header["identifier"].split(":")[-1],
        "category": get_category(jd),
        "source_1": "https://data.rijksmuseum.nl/object-metadata/harvest/",
        "source_2": jd.get("lido:objectPublishedID").get("#text"),
        "title": get_title(jd),
        "inscriptions": get_inscription(jd),
        "description": get_description(jdm),
        "dimensions": get_dimensions(jdm),
        "maker_full_name": get_maker_name(jdm),
    }
    # print(json.dumps(data, indent=4))
    break
