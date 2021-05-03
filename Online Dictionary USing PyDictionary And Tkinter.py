import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
from tkinter import messagebox as msg

import pyttsx3
from PyDictionary import PyDictionary

def internet_presence():
        import requests
        url = "http://www.google.com"  # Or any other site on the internet
        timeout = 5
        try:
        	request = requests.get(url, timeout=timeout)
        	return True
        except (requests.ConnectionError, requests.Timeout) as exception:
        	return False

def search():
        meaning_box.delete('1.0', END)
        synonym_box.delete('1.0', END)
        antonym_box.delete('1.0', END)
        if internet_presence() != True:
                msg.showerror("No Internet Connection", "Please Connect To The Internet And Try Again")
        elif word.get() == "":
                msg.showerror("Empty Field", "Please Fill The Word To Search")
        else:
                for i in PyDictionary().meaning(word.get()).values():
                        meaning_box.insert(tk.END, str(i)+"; ")
                for j in PyDictionary().synonym(word.get()):
                        synonym_box.insert(tk.END, j+", ")
                for k in PyDictionary().antonym(word.get()):
                        antonym_box.insert(tk.END, k+", ")
        
                
def speak():
        engine = pyttsx3.init()
        engine.setProperty('rate', 100)
        engine.say("Meaning "+meaning_box.get("1.0", tk.END))
        engine.say("Synonyms are "+synonym_box.get("1.0", tk.END))
        engine.say("Antonyms are "+antonym_box.get("1.0", tk.END))
        engine.runAndWait() 

if __name__ == "__main__":
        root = tk.Tk()
        root.geometry("600x400")
        root.title("Online Dictionary Using Python")
        root["background"] = 'green'
        ttk.Label(root, text="       ONLINE DICTIONARY           ", background="orange",
                foreground="red", font=("Times New Roman", 31, "bold")).place(x=0, y=0)

        ttk.Label(root, text="Enter Word :", background="green",
                foreground="red", font=("Comic Sans", 30)).place(x=0, y=70)
        word = tk.Entry(root, font=('Times New Roman', 20, 'italic',
                        'bold'), bd=1, relief=tk.RIDGE, justify=tk.CENTER)
        word.place(x=250, y=81, width=250, height=30)
        word.focus_set()
        search = tk.Button(root, text="Search", font=("Times New Roman", 13, "bold"), bd=0, bg='white', foreground='red',
                                cursor='hand2', command=search)
        search.place(x=450, y=120)
        speak = tk.Button(root, text="Speak", font=("Times New Roman", 13, "bold"), bd=0, bg='white', foreground='red',
                                cursor='hand2', command=speak)
        speak.place(x=520, y=120)


        ttk.Label(root, text="Meaning", font=("Times New Roman", 20, "bold"),
                background="green", foreground="red").place(x=5, y=145)
        meaning_box = scrolledtext.ScrolledText(root, width=30, height=5)
        meaning_box.place(x=20, y=180)


        ttk.Label(root, text="Synonyms", font=("Times New Roman", 20, "bold"),
                background="green", foreground="red").place(x=310, y=145)
        synonym_box = scrolledtext.ScrolledText(root, width=30, height=5)
        synonym_box.place(x=330, y=180)

        ttk.Label(root, text="Antonyms", font=("Times New Roman", 20, "bold"),
                background="green", foreground="red").place(x=5, y=265)
        antonym_box = scrolledtext.ScrolledText(root, width=30, height=5)
        antonym_box.place(x=20, y=300)

        root.mainloop()
