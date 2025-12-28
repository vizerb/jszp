from playwright.sync_api import sync_playwright
import time
import datetime
import requests
import tkinter as tk

MAX32SINT = 2**31-1
URL = 'https://magyarorszag.hu/snap/repo02/mapper/process.php'

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9,hu;q=0.8',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Origin': 'https://magyarorszag.hu',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'X-Requested-With': 'XMLHttpRequest',
    'X-SNAP-SECURE-TOKEN': "",
}

files = {
    'hidden-valasztott_adatkorok': (None, 'JarmuOkmany,SzarmazasEredet,ForgtartasForgkorlat,MuszakiAllapot,FutasTeljesitmeny,BiztositasKartortenet'),
    'hidden-rendszam': (None, ""),
    '_sys_language': (None, 'hu'),
    '_sys_Variables': (None, '{}'),
    '_sys_MapperID': (None, ""),
    '_sys_TabID': (None, ""),
}

session = requests.Session()

def countdown(startTime : datetime.datetime, n):
    app.after(0, lambda: countdown_label.configure(text=str(datetime.datetime.now() - startTime)))
    # label['text'] = str(datetime.datetime.now() - startTime)
    
    if (n<30):
        app.after(1000, countdown, startTime, n + 1)
    else:
        btn.configure(state="normal", text="Request")
    

def login(p):
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://magyarorszag.hu/")        
    page.wait_for_load_state("networkidle")

    page.locator("iframe[name=\"D\"]").content_frame.get_by_role("button", name="Kizárólag az elengedhetetlen").click()
    page.locator("iframe[name=\"L\"]").content_frame.get_by_role("button", name="BEJELENTKEZÉS").click()
    page.locator("iframe[name=\"L\"]").content_frame.get_by_role("button", name="KIJELENTKEZÉS").wait_for(timeout=MAX32SINT)
    page.goto("https://magyarorszag.hu/jszp_szuf")
        
    cookies = {c['name']: c['value'] for c in context.cookies()}
    secureToken = page.evaluate("g_secureToken")
    tabId = page.evaluate("g_tabId")
    
    files['_sys_TabID'] = (None, tabId)
    headers['X-SNAP-SECURE-TOKEN'] = secureToken
    
    session.cookies.update(cookies)
    session.headers.update(headers)

    page.evaluate("cClientTimeout = 3600")
    page.mouse.click(0,0)
    
    return browser,context
    

def make_request():
    files['hidden-rendszam'] = (None, entry.get())
    files['_sys_MapperID'] = (None, '7245949645153563')    
    
    print("Executing Request 1 (Plate Submission)...")
    response_1 = session.post(URL, files=files)

    if response_1.status_code == 200:
        print("Request 1 successful.")
        # base
        files['_sys_MapperID'] = (None, '7404720745143572')

        print("Executing Request 2 (Fetching Result)...")
        response_2 = session.post(URL, headers=headers, files=files)
        #'text-adatigenyles_datum': {'VALUE': 'Az adatszolgáltatás időpontja: 2025.12.23. 13:24:20'}}
        
        if response_2.status_code == 200:
            print("Request 2 successful. Data received:")
            print(response_2.json())
            data_2 = response_2.json()['CtrlValue']
            
            # EXAMPLE:
            # {
            #    "text-Gyartmany":"OPEL",
            #    "text-Tipus":"ASTRA H ENJOY",
            #    "text-Tjhszam":"",
            #    "text-Kerleiras":"",
            #    "text-Kategoria":"M1 - Személygépkocsi",
            #    "text-GyartasiEv":"2006"
            # }
            brandData = data_2["layout_list-JarmuOkmany-TipusAdatok"]["VALUE"][0]
            print(f"{brandData}\n\n")
            
            gyartmany_value.configure(text=brandData["text-Gyartmany"])
            kerleiras_value.configure(text=brandData["text-Kerleiras"])
            tipus_value.configure(text=brandData["text-Tipus"])
            kategoria_value.configure(text=brandData["text-Kategoria"])
            
            # Example value: Az adatszolgáltatás időpontja: 2025.12.23. 13:24:20
            timeYMD = data_2['text-adatigenyles_datum']['VALUE'].split(" ")[-2].split(".")[:-1]
            timeYMD = [int(s) for s in timeYMD]
            
            timeHMS = data_2['text-adatigenyles_datum']['VALUE'].split(" ")[-1].split(":")
            timeHMS = [int(s) for s in timeHMS]
            t = datetime.datetime(*timeYMD,*timeHMS)
            btn.configure(state="disabled", text="Waiting")
            countdown(t,0)
            print(t)
        
        # muszaki adatok            
        files['_sys_MapperID'] = (None, '7393854745198637')

        print("Executing Request 3 (Fetching Result 2)...")
        response_3 = session.post(URL, headers=headers, files=files)
        
        if response_3.status_code == 200:
            print("Request 3 successful. Data received:")
            print(response_3.json())
            data_3 = response_3.json()['CtrlValue']['layout_list-MuszakiAllapot']['VALUE'][0]
            
            muszakiAdatok = data_3['layout_list-MuszakiAllapot-MuszakiAdatok'][0]
            tengelyszam = muszakiAdatok['text-MuszakiAllapot-Tengelyszam']
            tengelyszam_value.configure(text=tengelyszam)
    else:
        print(f"Request 1 failed: {response_1.status_code}")



if __name__ == "__main__":
    with sync_playwright() as p:
        browser,context = login(p)
        
        app = tk.Tk()
        app.geometry("500x500")

        entry = tk.Entry(app)
        entry.insert(0, "Rendszam")
        
        def _clear_placeholder(event):
            if entry.get() == "Rendszam": 
                entry.delete(0, tk.END)
                
        entry.bind("<FocusIn>", _clear_placeholder)

        btn = tk.Button(app, text="Request", command=make_request)

        frame = tk.Frame(app)

        gyartmany_label = tk.Label(frame, text="Gyártmány:")
        gyartmany_value = tk.Label(frame, text="___", anchor="w", wraplength=320, justify="left")

        kerleiras_label = tk.Label(frame, text="Kereskedelmi leírás:")
        kerleiras_value = tk.Label(frame, text="___", anchor="w", wraplength=320, justify="left")

        tipus_label = tk.Label(frame, text="Típus:")
        tipus_value = tk.Label(frame, text="___", anchor="w", wraplength=320, justify="left")

        kategoria_label = tk.Label(frame, text="Kategória:")
        kategoria_value = tk.Label(
            frame,
            text="N1G - Tehergépkocsi vagy vontató 3,5 t-ig, terepjáró",
            anchor="w",
            wraplength=320,
            justify="left",
        )

        tengelyszam_label = tk.Label(frame, text="Tengelyszám:")
        tengelyszam_value = tk.Label(frame, text="___", anchor="w", wraplength=320, justify="left")

        # make column 1 expand
        frame.grid_columnconfigure(1, weight=1)

        gyartmany_label.grid(row=0, column=0, sticky="w", padx=6, pady=2)
        gyartmany_value.grid(row=0, column=1, sticky="w", padx=6, pady=2)
        kerleiras_label.grid(row=1, column=0, sticky="w", padx=6, pady=2)
        kerleiras_value.grid(row=1, column=1, sticky="w", padx=6, pady=2)
        tipus_label.grid(row=2, column=0, sticky="w", padx=6, pady=2)
        tipus_value.grid(row=2, column=1, sticky="w", padx=6, pady=2)
        kategoria_label.grid(row=3, column=0, sticky="w", padx=6, pady=2)
        kategoria_value.grid(row=3, column=1, sticky="w", padx=6, pady=2)
        tengelyszam_label.grid(row=4, column=0, sticky="w", padx=6, pady=2)
        tengelyszam_value.grid(row=4, column=1, sticky="w", padx=6, pady=2)

        countdown_label = tk.Label(app, text="00:00")

        entry.pack(anchor="s", expand=True, pady=10)
        btn.pack(anchor="n", expand=True)
        countdown_label.pack(anchor="s")
        frame.pack(anchor="n", expand=True, fill="both")

        app.mainloop()
        
        context.close()
        browser.close()