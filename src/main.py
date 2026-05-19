import tkinter as tk
import requests
import jszp
import parsing
from request_section import RequestSection
from response_section import ResponseSection

class RequestError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code


class JszpApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple jszp")
        self.geometry("640x500")

        # Bind enter to sending request
        self.bind('<Return>', self.handle_request)

        self.request_section = RequestSection(self, handle_request=self.handle_request)
        self.request_section.pack(side="top", fill="both", expand=True)

        self.response_section = ResponseSection(self)
        self.response_section.pack(side="bottom", fill="both", expand=True)
        
        jszp.login()
        self.session = requests.Session()
        self.session.cookies.update(jszp.cookies)
        self.session.headers.update(jszp.headers)
    
    def handle_request(self, event=None):
        plate = self.request_section.get_plate()
        self.request_section.toggle_button()
        
        try:
            result = self.make_request(plate)
            self.response_section.apply_results(result)
            self.countdown()
        except RequestError as e:
            self.response_section.clear_values()
            self.countdown()
            print(e)
        except Exception as e:
            self.response_section.clear_values()
            self.request_section.toggle_button()
            print(e)
                
    def make_request(self, plate):
        files,URL = [jszp.files, jszp.URL]
        result = {}
        request_timeout = 60
        files['hidden-rendszam'] = (None, plate)
        files['_sys_MapperID'] = (None, '7245949645153563')    
        
        try:
            response_1 = self.session.post(URL, files=files, timeout=request_timeout)
        except requests.exceptions.Timeout:
            raise RequestError("Nem érkezett időben válasz", 500)
        
        if response_1.status_code == 200:
            files['_sys_MapperID'] = (None, '7404720745143572')
            try:
                response_2 = self.session.post(URL, files=files, timeout=request_timeout)
            except requests.exceptions.Timeout:
                raise RequestError("Nem érkezett időben válasz", 500)
            
            if response_2.status_code == 200:
                jsonResponse = response_2.json()
                
                result1 = parsing.parseOkmanyAdatok(jsonResponse)
                
                if plate.capitalize() != result1['rendszam'].capitalize():
                    raise RequestError("Nem létezik ilyen rendszám", 404)

            # muszaki adatok
            files['_sys_MapperID'] = (None, '7393854745198637')

            try:
                response_3 = self.session.post(URL, files=files, timeout=request_timeout)
            except requests.exceptions.Timeout:
                raise RequestError("Nem érkezett időben válasz", 500)
            
            if response_3.status_code == 200:
                jsonResponse = response_3.json()

                result2 = parsing.parseMuszakiAdatok(jsonResponse)
                result = {**result2, **result1}
                
                return result
        else:
            raise RequestError(response_1.json(), response_1.status_code)

        return result

    
    def countdown(self, n=0):
        app.after(0, lambda: self.request_section.set_countdown_value(n))
        if (n<30):
            app.after(1000, self.countdown, n + 1)
        else:
            self.request_section.toggle_button()


if __name__ == "__main__":
    app = JszpApp()
    app.mainloop()