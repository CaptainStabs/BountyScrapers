import pandas as pd
import xmltodict
import json
import os
import csv
from tqdm import tqdm
# import heartrate; heartrate.trace(browser=True, daemon=True)
from send_mail import send_mail


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
            try:
                o_c_t = o_c.get("lido:objectWorkTypeWrap", {}).get("lido:objectWorkType", None)
            except:
                return

            if not o_c_t:
                return

            if isinstance(o_c_t, list):
                term_list = []
                for x in o_c_t: # Iterate through o_c_t list as x
                    term = x["lido:term"]
                    if isinstance(term, list): # check if term is a list
                        # print(term)
                        t_dict = build_dict(term, "@xml:lang")
                        t = term[t_dict.get("en")["index"]].get("#text") # Find english text
                        if not t:
                            t = term[t_dict.get("nl")["index"]].get("#text")

                        term_list.append(t)
                    else:
                        term_list.append(term.get("#text"))
                        # print("AAA", json.dumps(o_c_t, indent=2))
                cats.append("|".join([x for x in term_list if x]))

            else:
                term = o_c_t["lido:term"]
                if isinstance(term, list): # check if term is a list
                    # print(term)
                    t_dict = build_dict(term, "@xml:lang")
                    t = term[t_dict.get("en")["index"]].get("#text") # Find english text
                    if not t:
                        t = term[t_dict.get("nl")["index"]].get("#text")

                    term_list.append(t)
                else:
                    term_list.append(term.get("#text"))
                    # print("AAA", json.dumps(o_c_t, indent=2))
                cats.append("|".join([x for x in term_list if x]))
                

            # Get lido:classificationWrap
            if  o_c.get("lido:classificationWrap"):
                c_w = o_c.get("lido:classificationWrap").get("lido:classification")

                if isinstance(c_w, list):
                    term_list = []
                    for x in c_w:
                        term = x.get("lido:term")
                        if not term:
                            continue
                        if isinstance(term, list):
                            # print(term)
                            t_dict = build_dict(term, "@xml:lang")
                            t = term[t_dict.get("en")["index"]].get("#text")
                            term_list.append(t)
                        else:
                            term_list.append(term["#text"])
                            # print("AAA", json.dumps(c_w, indent=2))
                    cats.append("|".join([x for x in term_list if x]))
                    # [print("A", x["lido:term"]) for x in c_w if x["lido:term"]["@xml:lang"] == "en"]
                    # b = [x.get("lido:term").get("#text") for x in a if x["lido:term"]["@xml:lang"] == "en"]
                    # print("AAAA")
                else:
                    try:
                        cats.append(o_c.get("lido:classificationWrap").get("lido:classification").get("lido:term")[0].get("#text"))
                    except AttributeError:
                        cats.append(o_c.get("lido:classificationWrap").get("lido:classification").get("lido:term").get("#text"))
                    except KeyError:
                        try:
                            cats.append(o_c.get("lido:classificationWrap").get("lido:classification").get("lido:term").get("#text"))
                        except AttributeError:
                            print(json.dumps(o_c.get("lido:classificationWrap"), indent=4))
                            cats.append(o_c.get("lido:classificationWrap").get("lido:classification").get("lido:term")[0].get("#text"))
                # Get
            # o_d = desc_meta.get("lido:objectIdentificationWrap")

        if len(cats) != 2:
            # print(json.dumps(desc_meta, indent=2))
            print("\n", "Not two category")
        return "|".join([x for x in cats if x])
    return

def get_title(jd):
    if jd:
        t_list = []
        try:
            title_set = jd.get("lido:descriptiveMetadata", {}).get("lido:objectIdentificationWrap", {}).get("lido:titleWrap", {}).get("lido:titleSet", None)
        except:
            return
        if isinstance(title_set, list):
            for x in title_set:
                if x:
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
    inscription = jd.get("lido:descriptiveMetadata", {}).get("lido:objectIdentificationWrap", {}).get("lido:inscriptionsWrap", None)
    if inscription:
        i = inscription.get("lido:inscriptions")
        # print(json.dumps(i, indent=2))
        inscriptions = [x.get("lido:inscriptionTranscription") for x in i if type(x) != str]
        inscriptions = [x for x in inscriptions if x]
        if len(inscriptions):
            return "|".join(inscriptions)
    return None

def get_description(jdm):
    desc_set = jdm.get("lido:objectIdentificationWrap", {}).get("lido:objectDescriptionWrap", {}).get("lido:objectDescriptionSet")
    if desc_set:
        if isinstance(desc_set, list):
            return desc_set[0].get("lido:descriptiveNoteValue").get("#text")
        else:
            return desc_set.get("lido:descriptiveNoteValue").get("#text")

def get_dimensions(jd):
    measures = jd.get("lido:objectIdentificationWrap", {}).get("lido:objectMeasurementsWrap", {}).get("lido:objectMeasurementsSet")
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
                    if u:
                        y = u.get("lido:measurementValue")
                        # print("C",sets.get("lido:measurementUnit")[0].get("#text"))
                        unit = u.get("lido:measurementUnit")
                        m_list.append(y)

                        if unit:
                            units = u.get("lido:measurementUnit")[0].get("#text")
                            unit_list.append(units)

            else:
                try:
                    y = x.get("lido:measurementValue")
                    m_list.append(y)
                except AttributeError:
                    pass
                try:
                    if x.get('lido:measurementUnit'):
                        units = x.get("lido:measurementUnit")[0].get("#text")
                        unit_list.append(units)
                except AttributeError:
                    pass


        if success:
            units = " ".join(unit_list)
            m = " x ".join([x for x in m_list if x != None])
            return " ".join([m, units])
        else: return

def get_maker_name(jdm):
    events = jdm.get("lido:eventWrap", {})
    events = events.get("lido:eventSet", None) if events else None
    if events:
        names = []
        for event in events:
            if not isinstance(event, str):
                event = event.get("lido:event")
            else:
                continue

            event_set = event.get("lido:eventActor", {}).get("lido:actorInRole", {}).get("lido:actor", {}).get("lido:nameActorSet", None)
            if event_set:
                app_val = event_set.get("lido:appellationValue")
                if isinstance(app_val, list):
                    names.append(event_set.get("lido:appellationValue", {})[0].get("#text", None))
                else:
                    names.append(event_set.get("lido:appellationValue", {}).get("#text", None))

        return "|".join(names)
    else:
        return

def get_maker_role(jdm):
    events = jdm.get("lido:eventWrap", {})
    events = events.get("lido:eventSet") if events else None
    if events:
        roles = []
        for event in events:
            if not isinstance(event, str):
                event = event.get("lido:event")
            else:
                continue

            event_set = event.get("lido:eventActor", {}).get("lido:actorInRole", {}).get("lido:roleActor", None)

            if event_set:
                app_val = event_set.get("lido:term")
                if isinstance(app_val, list):
                    roles.append(app_val[0].get("#text", None))
                else:
                    roles.append(app_val.get("#text", None))

        return "|".join([x for x in roles if x])
    else: return

def get_maker_birth(jdm, death=False):
    events = jdm.get("lido:eventWrap", {})
    events = events.get("lido:eventSet") if events else None
    if events:
        births = []
        for event in events:
            if not isinstance(event, str):
                event = event.get("lido:event")
            else:
                continue

            event_set = event.get("lido:eventActor", {}).get("lido:actorInRole", {}).get("lido:actor", {}).get("lido:vitalDatesActor", None)
            if event_set:
                if not death:
                    if isinstance(event_set, list):
                        b = event_set[0].get("lido:earliestDate", None)
                    else:
                        b = event_set.get("lido:earliestDate", None)
                else:
                    if isinstance(event_set, list):
                        b = event_set[0].get("lido:latestDate", None)
                    else:
                        b = event_set.get("lido:latestDate", None)

                if b:
                    births.append(b.split("-")[0])
        return "|".join([x for x in births if x])
    else: return

def get_year(jdm, start=True, acquisition=False, desc=False, mat=False):
    events = jdm.get("lido:eventWrap", {})
    events = events.get("lido:eventSet") if events else None
    if events:
        births = []
        for event in events:
            if not isinstance(event, str):
                event = event.get("lido:event")
            else:
                continue

            event_type = event.get("lido:eventType")
            if event_type:
                term = event_type.get("lido:term")
            else:
                term = ""

            if isinstance(term, list):
                term = term[0]
                # print("\nIS term")
                # print(json.dumps(term, indent=2))
                # import sys; sys,exit()

            elif mat:
                mats = event.get("lido:eventMaterialsTech")

                mat_list = []
                if mats:
                    if isinstance(mats, list):
                        for m in mats:
                            terms = m.get("lido:materialsTech", {}).get("lido:termMaterialsTech", {}).get("lido:term", {})

                            # if len(terms) > 2:
                            #     print("\nTERMSSS:", terms)

                            if isinstance(terms, list):
                                m = terms[0].get("#text")
                            else:
                                m = terms.get("#text")
                            mat_list.append(m)
                        return "|".join([x for x in mat_list if x])
                    # else:
                        # print(json.dumps(mats, indent=2))
                        # print("mats is not list")
                        # import sys; sys.exit()

            else:
                if "Acquisition" not in term.get("#text") and not acquisition:
                    if not desc:
                        event_date = event.get("lido:eventDate", None)
                        if event_date:
                            l_date = event_date.get("lido:date")
                            ll_date = event_date.get("lido:date", [])
                            b = None
                            if start:
                                if isinstance(event_date, list):
                                    # print(json.dumps(ll_date, indent=4))
                                    b = ll_date[0].get("lido:earliestDate", None)
                                else:
                                    if l_date:
                                        b = l_date.get("lido:earliestDate", None)
                            else:
                                if isinstance(event_date, list):
                                    # print(json.dumps(ll_date, indent=4))
                                    b = ll_date[0].get("lido:latestDate", None)
                                else:
                                    if l_date:
                                        b = l_date.get("lido:latestDate", None)
                            if b:
                                return b.split("-")[0]
                            else: return None
                    else:
                        period_name = event.get("lido:periodName")
                        if isinstance(period_name, list):
                            # print("\n Period name length =",len(period_name), period_name)

                            period_name = period_name[0]
                        # print(json.dumps(period_name, indent=4))
                        if period_name:
                            p = period_name.get("lido:term")
                            if isinstance(p, list):
                                b = p[0].get("#text")
                            else:
                                b = p.get("#text")

                            return b

                elif "Acquisition" in term.get("#text") and acquisition:
                    print("!!!!acquisition")
                    event_date = event.get("lido:eventDate", None)

                    if event_date:
                        if start:
                            if isinstance(event_date, list):
                                b = event_date.get("lido:date", [])[0].get("lido:earliestDate", None)
                            else:
                                b = event_date.get("lido:date").get("lido:earliestDate", None)

                        else:
                            if isinstance(event_date, list):
                                b = event_date.get("lido:date")[0].get("lido:latestDate", None)
                            else:
                                b = event_date.get("lido:date").get("lido:latestDate", None)
                        return b.split("-")[0]
        try:
            if b:
                return b.split("-")[0]
            else: return None
        except UnboundLocalError:
            return None
    else:
        return
# with open("0.xml", "r", encoding='utf-8') as f:
columns = [
    "object_number",
    "institution_name",
    "institution_city",
    "institution_state",
    "institution_country",
    "institution_latitude",
    "institution_longitude",
    "category",
    "title",
    "description",
    "dimensions", #
    "accession_year",
    "credit_line",
    "source_1",
    "date_description",
    "maker_full_name",
    "maker_role",
    "year_start",
    "year_end",
    "materials",
    "maker_death_year",
    "maker_birth_year",
    "source_2",
    "inscriptions"
    ]

try:
    filename = "extracted_data.csv"
    with open(filename, "a", encoding='utf-8', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)
        if os.stat(filename).st_size == 0:
            writer.writeheader()

        dir = "F:\\museum-collections\\rijks\\"
        for files in tqdm(os.listdir(dir)):
            if "xml" not in files:
                # skip directories
                continue
            with open(os.path.join(dir, files), "r", encoding="utf-8") as f:
                dd = xmltodict.parse(f.read())
        # for files in ["0.xml", "20.xml"]:
        #     with open(files, "r", encoding="utf-8") as f:
        #         dd = xmltodict.parse(f.read())


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
                    "maker_role": get_maker_role(jdm),
                    "maker_birth_year": get_maker_birth(jdm),
                    "maker_death_year": get_maker_birth(jdm, death=True),
                    "year_start": get_year(jdm),
                    "year_end": get_year(jdm, start=False),
                    "date_description": get_year(jdm, desc=True),
                    "materials": get_year(jdm, mat=True),
                    # "accession_year": get_year(jdm, acquisition=True)
                }

                writer.writerow(data)
                # print(json.dumps(data, indent=4))
except:
    send_mail("Extractor crashed", "")
    raise
