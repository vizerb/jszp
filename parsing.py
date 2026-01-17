import datetime
from email.utils import format_datetime

def condAdd(source: dict,dest: dict,skey: str,dkey: str):
    if skey in source.keys():
        dest[dkey] = source[skey]
    return dest

def parseOkmanyAdatok(jsonResponse):
    result = {}
    result['rendszam'] = jsonResponse['ClientVariable']['bejelentes_elotoltes']['in_rendszam']
    ctrlValue = jsonResponse['CtrlValue']
    
    if not ("text-JarmuOkmany-Nincs_adat" in ctrlValue.keys()):
        tipusAdatok = ctrlValue['layout_list-JarmuOkmany-TipusAdatok']['VALUE'][0]
        result = condAdd(tipusAdatok, result, "text-Gyartmany", "gyartmany")
        result = condAdd(tipusAdatok, result, "text-Kerleiras", "kerleiras")
        result = condAdd(tipusAdatok, result, "text-Tipus", "tipus")
        result = condAdd(tipusAdatok, result, "text-Kategoria", "kategoria")

        muszakiAdatok = ctrlValue['layout_list-JarmuOkmany-MuszakiAdatok']['VALUE'][0]
        result = condAdd(muszakiAdatok, result, "text-UlohelySzam", "ulohelyszam")


    # Example value: Az adatszolgáltatás időpontja: 2025.12.23. 13:24:20
    timeYMD = ctrlValue['text-adatigenyles_datum']['VALUE'].split(" ")[-2].split(".")[:-1]
    timeYMD = [int(s) for s in timeYMD]
    
    timeHMS = ctrlValue['text-adatigenyles_datum']['VALUE'].split(" ")[-1].split(":")
    timeHMS = [int(s) for s in timeHMS]
    t = datetime.datetime(*timeYMD,*timeHMS)
    http_date = format_datetime(t.astimezone(datetime.timezone.utc), usegmt=True)

    result['adatigenyles_ideje'] = http_date

    return result

def parseMuszakiAdatok(jsonResponse):
    result = {}
    jsonResponse = jsonResponse['CtrlValue']['layout_list-MuszakiAllapot']['VALUE'][0]

    try:
        tipusAdatok = jsonResponse['layout_list-MuszakiAllapot-TipusAdatok'][0]                    
        result['gyartmany'] = tipusAdatok["text-MuszakiAllapot-Gyartmany"]
        result['kerleiras'] = tipusAdatok["text-MuszakiAllapot-Kerleiras"]
        result['tipus']  = tipusAdatok["text-MuszakiAllapot-Tipus"]
        result['kategoria'] = tipusAdatok["text-MuszakiAllapot-Kategoria"]
    except:
        result['gyartmany'] = "Nincs adat"
        result['kerleiras'] = "Nincs adat"
        result['tipus']  = "Nincs adat"
        result['kategoria'] = "Nincs adat"

    try:
        muszakiAdatok = jsonResponse['layout_list-MuszakiAllapot-MuszakiAdatok'][0]
        result['tengelyszam'] = muszakiAdatok['text-MuszakiAllapot-Tengelyszam']
        result['ulohelyszam'] = muszakiAdatok["text-MuszakiAllapot-Ulohelyszam"]
    except:
        result['tengelyszam'] = "Nincs adat"
        result['ulohelyszam'] = "Nincs adat"
    
    return result