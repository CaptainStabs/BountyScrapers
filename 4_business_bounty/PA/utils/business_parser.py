def business_type_parser(business_type_string):
    if "COOPERATIVE" in business_type_string:
        business_type = "COOP"
        print("      [?] Translated type 1: COOP")

    if "COOP " in business_type_string:
        business_type = "COOP"
        print("      [?] Translated type 2: COOP")
    if "CORP" in business_type_string:
        business_type = "CORPORATION"
        print("      [?] Translated type 1: CORPORATION")

    if "CORP " in business_type_string:
        business_type = "CORPORATION"
        print("      [?] Translated type 2: CORPORATION")

    if "CORPORATION" in business_type_string:
        business_type = "CORPORATION"
        print("      [?] Translated type 3: CORPORATION")

    if "DBA" in business_type_string:
        business_type = "DBA"
        print("      [?] Translated type: DBA")

    if "LIMITED LIABILITY COMPANY" in business_type_string:
        business_type = "LLC"
        print("      [?] Translated type 1: LLC")

    if "LLC" in business_type_string:
        business_type = "LLC"
        print("      [?] Translated type 2: LLC")

    if "L.L.C." in business_type_string:
        business_type = "LLC"
        print("      [?] Translated type 3: LLC")

    if "L.L.C" in business_type_string:
        business_type = "LLC"
        print("      [?] Translated type 4: LLC")

    if "NON-PROFIT" in business_type_string:
        business_type = "NONPROFIT"
        print("      [?] Translated type 1: NON-PROFIT")

    if "NONPROFIT" in business_type_string:
        business_type = "NONPROFIT"
        print("      [?] Translated type 2: NONPROFIT")

    if "PARTNERSHIP" in business_type_string:
        business_type = "PARTNERSHIP"
        print("      [?] Translated type: PARTNERSHIP")

    if "SOLE PROPRIETORSHIP" in business_type_string:
        business_type = "SOLE PROPRIETORSHIP"
        print("      [?] Translated type: SOLE PROPRIETORSHIP")

    if "TRUST" in business_type_string:
        business_type = "TRUST"
        print("      [?] Translated type: TRUST")

    if "INC " in business_type_string:
        business_type = "CORPORATION"
        print("      [?] Translated type 1: INC")

    if "INC" in business_type_string:
        business_type = "CORPORATION"
        print("      [?] Translated type 2: INC")

    if "INCORPORATED" in business_type_string:
        business_type = "CORPORATION"
        print("      [?] Translated type 3: INC")

    # if "LIMITED" in business_type_string:
    #     business_type = "LTD"
    #     print("      [?] Translaetd type1: LTD")

    if "LTD" in business_type_string:
        business_type = "LTD"
        print("      [?] Translaetd type 2: LTD")

    if "L.T.D" in business_type_string:
        business_type = "LTD"
        print("      [?] Translaetd type 3: LTD")

    try:
        return business_type
    except UnboundLocalError:
        print("      [!] No business type defined, defaulting to CORPORATION")
        return "CORPORATION"
