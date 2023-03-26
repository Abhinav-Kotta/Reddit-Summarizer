import tkinter
import tkinter.messagebox
import customtkinter as ctk

ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')

# window
window = ctk.CTk()
window.title('Reddit Web-Scraper')
window.geometry('780x480')

# widgets
label = ctk.CTkLabel(
    window, 
    text = 'Too Long; Let Us Summarize', 
    fg_color= '#FF5700',
    text_color= 'white',
    corner_radius= 5, 
    font=ctk.CTkFont(size=20, weight="bold"))
label.pack(padx=10, pady=20)

# Entry for the Reddit URL
url_var = tkinter.StringVar()
link = ctk.CTkEntry(window, width=350, height=40, textvariable=url_var)
link.pack()

# Insert URL for Reddit to summarize
# command= lambda: print('Button was pressed')
# command= lambda: ctk.set_appearance_mode('dark')
button = ctk.CTkButton(
    window, text = 'Submit',
    fg_color= '#FF5700',
    text_color= 'white',
    corner_radius= 5, 
    font=ctk.CTkFont(size=20, weight="bold"),
    hover = True,
    command= lambda: print('Button was pressed' )
    )
button.pack(padx=10,pady =10)

# run 
window.mainloop()