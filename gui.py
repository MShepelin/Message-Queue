import tkinter
from tkinter import scrolledtext

import asyncio
import threading


class WikiLengthGUI:
    def __init__(self, on_send):
        msg = tkinter.Tk()
        msg.withdraw()

        self.on_send = on_send

        self.win = tkinter.Tk()
        self.win.configure(bg="lightgrey")

        self.msg_label_url1 = tkinter.Label(self.win, text="First URL:", bg="lightgrey")
        self.msg_label_url1.config(font=("Arial", 12))
        self.msg_label_url1.pack(padx=20, pady=5)

        self.input_area_url1 = tkinter.Text(self.win, height=3)
        self.input_area_url1.pack(padx=20, pady=5)

        self.msg_label_url2 = tkinter.Label(self.win, text="Second URL:", bg="lightgrey")
        self.msg_label_url2.config(font=("Arial", 12))
        self.msg_label_url2.pack(padx=20, pady=5)

        self.input_area_url2 = tkinter.Text(self.win, height=3)
        self.input_area_url2.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.send_msg)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.chat_label = tkinter.Label(self.win, text="Response:", bg="lightgrey")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win, height = 10)
        self.text_area.config(font=('Arial', 12), state='disabled')
        self.text_area.pack(padx=20, pady=5)

    def receive_msg(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert('end', message)
        self.text_area.yview('end')
        self.text_area.config(state='disabled')

    def send_msg(self):
        url1 = self.input_area_url1.get('1.0', 'end-1c')
        url2 = self.input_area_url2.get('1.0', 'end-1c')
        self.input_area_url1.delete('1.0', 'end')
        self.input_area_url2.delete('1.0', 'end')

        self.send_button.config(state='disabled')

        threading.Thread(target=self.on_send, args=(url1, url2)).start()

    def enable_input(self):
        self.send_button.config(state='normal')

    def stop(self):
        self.win.quit()

    def start(self):
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()
