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
url_var = tkinter.StringVar(window,"Summarize a comment here...")
print(url_var.get())
link = ctk.CTkEntry(window, width=350, height=40, textvariable=url_var)
link.pack()

# url_var.set("testasdfasfasdf")
# print(url_var.get())

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
    command= lambda: print(f'Button was pressed: URL {url_var.get()}')
    )
button.pack(padx=10,pady =10)

# Summary textbox header
summary_header = ctk.CTkLabel(
    window, 
    text = 'Post/Comment Summary', 
    fg_color= '#FF5700',
    text_color= 'white',
    corner_radius= 5, 
    font=ctk.CTkFont(size=20, weight="bold"))
summary_header.pack(padx=10, pady=50)

# run 
window.mainloop()
