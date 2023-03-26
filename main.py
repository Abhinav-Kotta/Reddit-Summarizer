import tkinter
import tkinter.messagebox
import textwrap
import customtkinter as ctk


def button_event():
    entry_text = link.get()
    label2.configure(text=entry_text, wraplength = 500)

ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')

# window
window = ctk.CTk()
window.title('Reddit Web-Scraper')
window.geometry('1000x1000')

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
link = ctk.CTkEntry(window, width=350, height=40, placeholder_text="Type Here")
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
    command= button_event)
button.pack(padx=10,pady =10)

# Summary textbox header
summary_header = ctk.CTkLabel(
    window, 
    text = 'Post/Comment Summary', 
    fg_color= '#FF5700',
    text_color= 'white',
    corner_radius= 5, 
    font=ctk.CTkFont(size=20, weight="bold"))
summary_header.pack(padx=10, pady=40)
"""
frame = ctk.CTkFrame(window, width=600, height=150)
frame.pack()

label2 = ctk.CTkLabel(master=frame,  width=600, height=150)
label2.pack()
"""
optionmenu_var = ctk.StringVar(value="option 2")  # set initial value

def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)

    if choice == "option 1":
        frame2 = ctk.CTkFrame(window, width=600, height=150)
        frame2.pack()

        label3 = ctk.CTkLabel(master=frame,  width=600, height=150)
        label3.pack()
    elif choice == "option 2":
        frame3 = ctk.CTkFrame(window, width=600, height=150)
        frame3.pack()

        label4 = ctk.CTkLabel(master=frame,  width=600, height=150)
        label4.pack()

        frame4 = ctk.CTkFrame(window, width=600, height=150)
        frame4.pack()

        label5 = ctk.CTkLabel(master=frame,  width=600, height=150)
        label5.pack()



combobox = ctk.CTkOptionMenu(master=window,
                                       values=["option 1", "option 2"],
                                       command=optionmenu_callback,
                                       variable=optionmenu_var)
combobox.pack(padx=20, pady=10)
# run 
window.mainloop()
