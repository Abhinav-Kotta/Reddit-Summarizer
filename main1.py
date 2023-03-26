import tkinter as tk
import tkinter.messagebox
import textwrap
import customtkinter as ctk

def summarize():
    url = utext.get('1.0', "end").strip()
    
	

root = tk.Tk()

root.title("Reddit Summarizer")
root.geometry('1200x600')

tlabel = tk.Label(root, text='Title')
tlabel.pack()

title = tk.Text(root, height = 1, width = 140)
title.config(state='disabled', bg= '#dddddd')
title.pack()

alabel = tk.Label(root, text='Author')
alabel.pack()

author = tk.Text(root, height=1, width=140)
author.config(state='disabled', bg='#dddddd')
author.pack()

plabel = tk.Label(root, text='Publishing Date')
plabel.pack()

publication = tk.Text(root, height=1, width=140)
publication.config(state='disabled', bg='#dddddd')
publication.pack()

slabel = tk.Label(root, text='Summary')
slabel.pack()

summary = tk.Text(root, height=20, width=140)
summary.config(state='disabled', bg='#dddddd')
summary.pack()

selabel = tk.Label(root, text='Sentimental Analysis')
selabel.pack()

sentiment = tk.Text(root, height=1, width=140)
sentiment.config(state='disabled', bg='#dddddd')
sentiment.pack()

ulabel = tk.Label(root, text=' URL')
ulabel.pack()

utext = tk.Text(root, height=1, width=140)
utext.pack()

btn = tk.Button(root, text="Summarize", command=summarize)
btn.pack()

root.mainloop()
