data = {
    "texts": [
    {
      "texttype": "Online",
      "textpurpose": "Description",
      "textentryhtml": "A hollow trumpet-shaped foot with everted rim supports a cup with sides flaring up to a wide mount. Two strap-like handles run the full height of the cup, linked to it at the bottom, middle and top. Projections flare out at the top of each handle and are decorated with small round impressions, resembling metal studs, stamped on the top and side surfaces. One strap handle is decorated on the outer surface with a crosshatch design inside a rectangular field and the other with stamped circles and grooves. Three grooves ring the foot and four encircle the body of the cup. This earthenware vessel is modeled, and the gray clay when fired under oxidation has turned a warm reddish-brown with black specks. The surface appears to have been burnished before firing. Thermo luminescence analysis of samples taken from the upper and lower sections of the cup are consistent with the dating of this vessel.",
      "remarks": "as per object file"
    },
    {"textpurpose": "test"}
    ]
    }

a = [x["textpurpose"] for x in data["texts"]]
if "Description" in a:
    print(a.index("Description"))
    print("A")
else:
    print("B")
