import tkinter as tk
import webbrowser
import os

class CustomWebBrowser(tk.Frame):
    def __init__(self, master=None, whitelist = ['Homepage.html', 'https://www.neopets.com/', 'https://www.coolmathgames.com/', 'https://www.ixl.com/', 'https://mail.google.com/'], **kw):
        super().__init__(master=master, **kw)
        self.master = master
        self.master.overrideredirect(True)
        self.master.geometry("1080x1080")
        self.whitelist = whitelist or []
        homepage_path = os.path.join(os.getcwd(), 'Homepage.html')
        self.browser = webbrowser.open_new(homepage_path)
        self.create_widgets()
        self.bind_events()

    def create_widgets(self):
        # Frame for the browser window and text entry boxes
        self.frame = tk.Frame(self.master, bd=2, relief=tk.SOLID, highlightthickness=0, highlightbackground='#800080')
        self.frame.pack(fill=tk.BOTH, expand=tk.YES, padx=2, pady=2)

        # Browser window
        self.browser_frame = tk.Frame(self.frame)
        self.browser_frame.pack(fill=tk.BOTH, expand=tk.YES)
        self.browser_canvas = tk.Canvas(self.browser_frame, bg='white')
        self.browser_canvas.pack(fill=tk.BOTH, expand=tk.YES, padx=2, pady=2)
        self.scrollbar_x = tk.Scrollbar(self.browser_frame, orient=tk.HORIZONTAL, command=self.browser_canvas.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.scrollbar_y = tk.Scrollbar(self.browser_frame, orient=tk.VERTICAL, command=self.browser_canvas.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.browser_canvas.config(xscrollcommand=self.scrollbar_x.set, yscrollcommand=self.scrollbar_y.set)
        self.browser_canvas.create_window((0, 0), window=self.browser, anchor='nw')

        # Text entry boxes
        self.text_frame = tk.Frame(self.frame, bd=2, relief=tk.SOLID, highlightthickness=0, highlightbackground='#800080')
        self.sallie_entry = tk.Entry(self.text_frame, bg='white', bd=0, highlightthickness=0, font=('TkDefaultFont', 12))
        self.sallie_entry.pack(side=tk.LEFT, fill=tk.X, expand=1, padx=2, pady=2)
        self.user_entry = tk.Entry(self.text_frame, bg='white', bd=0, highlightthickness=0, font=('TkDefaultFont', 12))
        self.user_entry.pack(side=tk.LEFT, fill=tk.X, expand=1, padx=2, pady=2)
        self.text_frame.pack(fill=tk.X, padx=2, pady=2)

    def bind_events(self):
        self.browser.bind("<Button-1>", lambda event: self.link_clicked(self.browser.geturl()))
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.user_entry.bind("<Return>", self.on_user_message_sent)

    def link_clicked(self, url):
        if url.startswith('http'):
            if url in self.whitelist:
                webbrowser.open_new(url)
            else:
                tk.messagebox.showerror("Error", "Unauthorized site!")
        else:
            webbrowser.open_new(url)

    def on_closing(self):
        if homepage_path in self.browser.geturl():
            self.master.destroy()
        elif self.browser.geturl() in self.whitelist:
            self.master.destroy()
        else:
            tk.messagebox.showerror("Error", "Unauthorized site!")

    def set_border_color(self, color):
        self.frame.config(highlightbackground=color)

    def run(self):
        self.master.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    browser = CustomWebBrowser(root)
    browser.set_border_color('blue')
    browser.run()
