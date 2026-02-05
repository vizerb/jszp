import tkinter as tk

class ResponseSection(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid = tk.Frame(self)
        self.grid.grid_columnconfigure(1, weight=1)
        self.grid.pack(fill="x", expand=True, padx=10)
        self.fields = {}
        
        for i,(key,value) in enumerate(self.response_labels.items()):
            self.fields[key+"_label"] = tk.Label(self.grid, text=value+":")
            self.fields[key+"_label"].grid(row=i, column=0, sticky="w", padx=6, pady=2)
            self.fields[key] = tk.Entry(self.grid)
            self.fields[key].grid(row=i, column=1, sticky="ew", padx=6, pady=2)
            self.fields[key].config(state='readonly')
    
    response_labels = {
        "rendszam": "Rendszám",
        "gyartmany": "Gyártmány",
        "kerleiras": "Kereskedelmi leírás",
        "tipus": "Típus",
        "kategoria": "Kategória",
        "tengelyszam": "Tengelyszám",
        "ulohelyszam": "Ülőhelyszám",
    }

    def clear_values(self):
        for key in self.response_labels:
            self.fields[key].config(state='normal')
            self.fields[key].delete(0,1000)
            self.fields[key].config(state='readonly')

    def apply_results(self, results: dict):
        self.clear_values()
        for key,value in results.items():
            if key in self.fields.keys():
                self.fields[key].config(state='normal')
                self.fields[key].insert(0, value)
                self.fields[key].config(state='readonly')