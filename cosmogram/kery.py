from kerykeion import AstrologicalSubject, KerykeionChartSVG, SynastryAspects, KerykeionChartSVG


class Error(Exception):
    def __init__(self, txt):
        super().__init__(txt)


def confir(lis):
    t = {}
    for i in range(len(lis)):
        ar = lis[i].split("=")[1]
        if ar == "True" or ar == "False":
            ar = bool(ar)
        elif ar.upper() == ar and ar.lower() == ar:
            if '.' in ar:
                ar = float(ar)
            else:
                ar = int(ar)
        else:
            ar = ar.removeprefix("'")
            ar = ar.removesuffix("'")
        t[lis[i].split("=")[0]] = ar
    return t

def get_SVG_human(human):
    return str(KerykeionChartSVG(human, chart_language="RU").makeSVG(ret=True))

def anal_human(name="", year=-1, month=-1, day=-1, hour=0, min=0, lng=-1.0, lat=-1.0, city=""):
    ER = "No Function Argument(s): "
    err = ER
    if year == -1:
        ER += "year, "
    if month == -1:
        ER += "month, "
    if day == -1:
        ER += "day, "
    if lng == -1:
        ER += "lng, "
    if lat == -1:
        ER += "lat, "
    if ER != err:
        raise Error(ER.removesuffix(", ") + "\nAll Arguments: name, year, month, day, hour, min, lng, lat, city")
    return AstrologicalSubject(name=name, year=year, month=month, day=day, hour=hour, minute=min, lng=lng, lat=lat, city=city)


def anal_two_people(first="", second=""):
    ER = "No Function Argument(s): "
    err = ER
    if first == "":
        ER += "first, "
    if second == "":
        ER += "second, "
    if ER != err:
        raise Error(ER.removesuffix(", ")  + "\nAll Arguments: first, second")
    # Natal, Synastry or Transit
    synastry_chart = KerykeionChartSVG(first, "Synastry", second, chart_language="RU")
    svgg = synastry_chart.makeSVG(minify=False, ret=True)
    name = SynastryAspects(first, second).relevant_aspects

    t = []
    for i in range(len(name)):
        r = str(name[i]).split(" ")
        if 'is_major=True' in r:
            er = confir(r)
            t.append(er)
    r = 0.0
    rr = 0.0
    s = 0.0
    u = set()
    for i in t:
        u.add(i["aspect"])
        s += i["diff"]
        if i['aspect'] == "trine" or i['aspect'] == "sextile":
            # print(i)
            r += i["diff"]
        else:
            rr += i["diff"]
    # print(r, rr, u)
    # print(r / s * 100, rr / s * 100, ((r / s) + (rr / s)) * 100)
    return {"dif": float(r / s * 100), "svg": str(svgg)}

# aspect_list = [aspect.dict() for aspect in name.all_aspects]
# pprint.pprint(aspect_list[0])


if __name__ == "__main__":

    f = anal_human("Aleksey", 2002, 1, 4, lng=1, lat=1)
    print(get_SVG_human(f))
    s = anal_human("Aleksey", 2002, 1, 4, lng=1, lat=1)
    anal_two_people(f, s)