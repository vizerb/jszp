import tkinter as tk

class RequestSection(tk.Frame):
    def __init__(self, master, handle_request, **kwargs):
        super().__init__(master, **kwargs)
        self.config(bg="lightblue")
        
        self.container = tk.Frame(self)
        self.container.config(bg='#bdbdbb')
        
        self.plate_entry = tk.Entry(self.container)
        self.plate_entry.insert(0, "Rendszam")
        
        self.plate_entry.bind("<FocusIn>", self._clear_placeholder)
        self.plate_entry.pack(expand=True,pady=15)

        self.request_button = tk.Button(self.container, text="Request", command=handle_request)
        self.request_button.pack(expand=True,pady=15)
        
        self.container.pack(expand=True)
        
        self.countdown_label = tk.Label(self, text="00:00")
        self.countdown_label.pack(anchor="s")
    
    def get_plate(self):
        return self.plate_entry.get()
    
    def toggle_button(self):
        if self.request_button["state"] in ["normal","active"]:
            self.request_button.config(state="disabled")
        else:
            self.request_button.config(state="normal")
    
    def set_countdown_value(self, val):
        self.countdown_label.configure(text=str(val))
    
    def _clear_placeholder(self, event):
            if self.plate_entry.get() == "Rendszam": 
                self.plate_entry.delete(0, tk.END)