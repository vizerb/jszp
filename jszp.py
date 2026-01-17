from playwright.sync_api import sync_playwright

MAX32SINT = 2**31-1
URL = 'https://magyarorszag.hu/snap/repo02/mapper/process.php'

cookies = {}

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

def login():
    with sync_playwright() as p:
        global cookies
        global headers
        global files
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        #page = browser
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
        
        #session.cookies.update(cookies)
        #session.headers.update(headers)

        page.evaluate("cClientTimeout = 3600")
        page.mouse.click(0,0)
        
        context.close()
        browser.close()
