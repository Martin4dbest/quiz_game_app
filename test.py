from tkinter import *
import tkinter as tk
from tkinter.ttk import Progressbar
from pygame import mixer
import pyttsx3
from tkinter import ttk, messagebox
import json
from tkinter import Tk, Text, Button, Label, Frame, PhotoImage
import tkinter.messagebox as messagebox
from tkinter import StringVar
from tkinter import Tk,Text,Button,StringVar,Label
import random
import sqlite3
import re
from tkinter import Tk, Entry, Label, Button, messagebox
from tkinter import PhotoImage




# Define global variables for questions and options
question = []
First_options = []
Second_options = []
Third_options = []
Fourth_options = []
correct_answers = []
lifelines = []


#create database
def create_database():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, scores INTEGER, amount_won REAL)''')
    conn.commit()
    conn.close()

def update_scores(username, new_score):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("UPDATE users SET scores = ? WHERE username = ?", (new_score, username))
    conn.commit()
    conn.close()

def update_amount_won(username, amount):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("UPDATE users SET amount_won = ? WHERE username = ?", (amount, username))
    conn.commit()
    conn.close()

    

def register_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def username_exists(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    return result is not None

def authenticate_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None

def register():
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Error", "Please enter a username and password.")
        return
    if len(password) < 6 or not password.isalnum():
        messagebox.showerror("Error", "Password must be alphanumeric and at least 6 characters long.")
        return
    if username_exists(username):
        messagebox.showerror("Error", "Username already exists. Please choose a different username.")
        return
    if register_user(username, password):
        messagebox.showinfo("Success", "Registration successful. You can now log in.")
    else:
        messagebox.showerror("Error", "Failed to register user.")

category_window = None  
def logout():
    global category_window
    if category_window:
        category_window.destroy()  # Destroy the category selection window
    create_login_window()  # Show the login window again


def exit_game():
    global category_window
    category_window.destroy()





def login():
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Error", "Please enter a username and password.")
        return
    if authenticate_user(username, password):
        messagebox.showinfo("Success", "Login successful.")
        root.destroy()  # Destroy the login window
        show_category_selection()  # Show category selection window
    else:
        messagebox.showerror("Error", "Invalid username or password.")

def forgot_password():
    messagebox.showinfo("Forgot Password", "Please contact support for assistance.")

def show_password():
    if password_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")



def show_category_selection():
    global category_window
    category_window = tk.Tk()
    category_window.title("Category Selection")
    category_window.geometry("1430x1430")
    category_window.configure(bg="blue")

    img = tk.PhotoImage(file="logo90.png")
    img_label = tk.Label(category_window, image=img)
    img_label.pack()

    categories = ["GENERAL KNOWLEDGE", "GEOGRAPHY", "HISTORY", "LITERATURE", "MUSIC", "POP CULTURE", "SPORT", "COMPUTER SCIENCE", "RIDDLES", "SCIENCE AND TECHNOLOGY"]

    def start_game_with_category(category):
        global category_window
        category_window.destroy() 
        #correct_answers, question, options = main_game(category)
        main_game(category)
        #start_game_with_category("General Knowledge") 
        
     

    

    category_frame = ttk.Frame(category_window)
    category_frame.pack()
    



    for category in categories:
        button = ttk.Button(category_frame, text=category, command=lambda cat=category: start_game_with_category(cat))

        button.pack(side=tk.LEFT, padx=5, pady=5, ipadx=10, ipady=5)  # Adjust internal padding
       

        # Create logout button
    logout_button = ttk.Button(category_window, text="Logout", command=logout)
    logout_button.pack(pady=(20, 5))  # Adjust vertical padding with tuple (top, bottom)

        # Create exit button
    exit_button = ttk.Button(category_window, text="Exit", command=exit_game)
    exit_button.pack(pady=(5, 20))  # Adjust
    

 



    category_window.mainloop()


"""
def start_timer(category):
    timer_decision_window = tk.Toplevel()  # Create a new window for timer decision
    timer_decision_window.title("Timer Decision")
    timer_decision_window.geometry("300x150")

    decision_label = ttk.Label(timer_decision_window, text="Do you want to enable the timer?")
    decision_label.pack(pady=10)

    def start_with_timer():
        timer_decision_window.destroy()  # Close the decision window
        start_timer_window(category)

    def start_without_timer():
        timer_decision_window.destroy()  # Close the decision window
        #start_quiz(category, enable_timer=False)  # Start the quiz without a timer
        
       

    timer_button_frame = ttk.Frame(timer_decision_window)
    timer_button_frame.pack(pady=10)

    timer_button = ttk.Button(timer_button_frame, text="Start with Timer", command=start_with_timer)
    timer_button.grid(row=0, column=0, padx=10)

    no_timer_button = ttk.Button(timer_button_frame, text="Continue without Timer", command=start_without_timer)
    no_timer_button.grid(row=0, column=1, padx=10)

def start_timer_window(category):
    timer_window = tk.Toplevel()  # Use Toplevel instead of Tk
    timer_window.title("Timer")
    timer_window.geometry("300x200")

    img = tk.PhotoImage(file="timerr.png")
    img_label = tk.Label(timer_window, image=img)
    img_label.pack()

    countdown_label = ttk.Label(timer_window, text="Time Left:")
    countdown_label.pack()

    countdown_var = tk.StringVar()
    countdown_display = ttk.Label(timer_window, textvariable=countdown_var)
    countdown_display.pack()

    # Timer countdown functionality
    def countdown(seconds):
        if seconds > 0:
            countdown_var.set(seconds)
            timer_window.after(1000, countdown, seconds - 1)  # Schedule the next call after 1000ms (1 second)
        else:
            countdown_var.set("Time's up!")
            try_again_button = ttk.Button(timer_window, text="Try Again", command=timer_window.destroy)
            try_again_button.pack(pady=5)

            # Call the appropriate quiz function based on the selected category
            start_quiz(category)
           

    countdown(60)  # Start the countdown from 60 seconds

    timer_window.mainloop()

"""



def create_login_window():
    global root, username_entry, password_entry, password_var

    root = tk.Tk()
    root.title("Who Wants to Be a Millionaire - Login")
    root.geometry("1430x1430")
    root.resizable(True, True)  # Allow window expansion

    # Add image of Who Wants to Be a Millionaire
    img = tk.PhotoImage(file="logo90.png")
    img_label = tk.Label(root, image=img)
    img_label.pack()

    frame = ttk.Frame(root)
    frame.pack(pady=10)

    username_label = ttk.Label(frame, text="Username:")
    username_label.grid(row=0, column=0, padx=5, pady=5)

    # Create a rounded entry widget for username
    username_entry = ttk.Entry(frame, style="Rounded.TEntry")
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    password_label = ttk.Label(frame, text="Password:")
    password_label.grid(row=1, column=0, padx=5, pady=5)

    # Create a rounded entry widget for password
    password_var = tk.BooleanVar()
    password_entry = ttk.Entry(frame, show="*", style="Rounded.TEntry")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    # Add "Show Password" checkbutton
    password_checkbutton = ttk.Checkbutton(frame, text="Show Password", variable=password_var, command=show_password)
    password_checkbutton.grid(row=2, columnspan=2, pady=5)

    login_button = ttk.Button(frame, text="Login", command=login, style="Green.TButton")
    login_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

    register_button = ttk.Button(frame, text="Register", command=register, style="Blue.TButton")
    register_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

    forgot_password_label = tk.Label(root, text="Forgot Password?", fg="blue", cursor="hand2")
    forgot_password_label.pack(pady=5)
    forgot_password_label.bind("<Button-1>", lambda e: forgot_password())

    # Define custom style for rounded entry widgets
    root.style = ttk.Style()
    root.style.theme_use("classic")
    #root.style.configure("Rounded.TEntry", padding=10, relief="flat", foreground="black")
    root.style.configure("Rounded.TEntry", padding=(10, 5), relief="raised", foreground="black")
   
  

    root.mainloop()


def main_game(category):
    # Initialize pyttsx3 engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty("voice", voices[0].id)

    # Initialize mixer and play background music
    mixer.init()
    mixer.music.load("kbc.mp3")
    mixer.music.play(-1)



    





    

    def select(event):
        callButtton.place_forget()
        progressBarA.place_forget()
        progressBarB.place_forget()
        progressBarC.place_forget()
        progressBarD.place_forget()


        progressbarLabelA.place_forget()
        progressbarLabelB.place_forget()
        progressbarLabelC.place_forget()
        progressbarLabelD.place_forget()
        b=event.widget
        value=b["text"]

        for i in range(15):
            if value==correct_answers[i]:
                if value==correct_answers[14]:
                    def close():
                        root2.destroy()
                        root.destroy()
                    def playagain():
                        lifeline50Button.config(state=NORMAL,image=image50)
                        audiencePoleButton.config(state=NORMAL,image=audiencePole)
                        phoneLifeLineButton.config(state=NORMAL,image=phoneImage)
                        root2.destroy()
                        questionArea.delete(1.0,END)
                        questionArea.insert(END,question[0])
                        optionButton1.config(text=First_options[0])
                        optionButton2.config(text=Second_options[0])
                        optionButton3.config(text=Third_options[0])
                        optionButton4.config(text=Fourth_options[0])
                        amountLabel.config(image=amountImages)

                # load_new_questions()

                    mixer.music.stop()
                    mixer.music.load("kbcwon.mp3")
                    mixer.music.play()
                    root2=Toplevel()
                    root2.config(bg="black")
                    root2.geometry("500x400+140+30")
                    root2.title("You won 100,000,000 pounds")
                    imgLabel=Label(root2,image=centerImage,bd=0)
                    imgLabel.pack(pady=30)

                    
                    winLabel=Label(root2, text="You Won",font=("arial", 40, "bold",), bg='black', fg="white")
                    winLabel.pack()

                    playagainButton=Button(root2, text="Play Again",font=("arial",20,"bold"),bg="black", fg="white",activebackground="black",activeforeground="white",bd=0,cursor="hand2",command=playagain)
                    playagainButton.pack()

                    closeButton=Button(root2, text="Close",font=("arial",20,"bold"),bg="black", fg="white",activebackground="black",activeforeground="white",bd=0,cursor="hand2",command=close)
                    closeButton.pack()

                    happyimage=PhotoImage(file="happy.png")
                    happyLabel=Label(root2,image=happyimage,bg="black")
                    happyLabel.place(x=30,y=280)
                        
                    happyLabel1=Label(root2,image=happyimage,bg="black")
                    happyLabel1.place(x=400,y=280)


                    root2.mainloop()
                    break

                questionArea.delete(1.0,END)
                questionArea.insert(END,question[i+1])
                optionButton1.config(text=First_options[i+1])
                optionButton2.config(text=Second_options[i+1])
                optionButton3.config(text=Third_options[i+1])
                optionButton4.config(text=Fourth_options[i+1])
                amountLabel.configure(image=amountImages[i])
                amountLabel.image = amountImages[i]


            if value not in correct_answers:
                def close():
                    root1.destroy()
                    root.destroy()
                def tryagain():
                    lifeline50Button.config(state=NORMAL,image=image50)
                    audiencePoleButton.config(state=NORMAL,image=audiencePole)
                    phoneLifeLineButton.config(state=NORMAL,image=phoneImage)
                    root1.destroy()
                    questionArea.delete(1.0,END)
                    questionArea.insert(END,question[0])
                    optionButton1.config(text=First_options[0])
                    optionButton2.config(text=Second_options[0])
                    optionButton3.config(text=Third_options[0])
                    optionButton4.config(text=Fourth_options[0])
                    amountLabel.config(image=amountImages[0])

                root1=Toplevel()
                root1.config(bg="black")
                root1.geometry("500x400+140+30")
                root1.title("You won 0 pounds")
                imgLabel=Label(root1,image=centerImage,bd=0)
                imgLabel.pack(pady=30)

                loseLabel=Label(root1, text="You lose",font=("arial", 40, "bold",), bg='black', fg="white")
                loseLabel.pack()

                tryagainButton=Button(root1, text="Try Again",font=("arial",20,"bold"),bg="black", fg="white",activebackground="black",activeforeground="white",bd=0,cursor="hand2",command=tryagain)
                tryagainButton.pack()

                closeButton=Button(root1, text="Close",font=("arial",20,"bold"),bg="black", fg="white",activebackground="black",activeforeground="white",bd=0,cursor="hand2",command=close)
                closeButton.pack()

                sadimage=PhotoImage(file="sad.png")
                sadLabel=Label(root1,image=sadimage,bg="black")
                sadLabel.place(x=30,y=280)
                
                sadLabel1=Label(root1,image=sadimage,bg="black")
                sadLabel1.place(x=400,y=280)
                root1.mainloop()
                break
    def lifeline50():
        lifeline50Button.config(image=image50X,state=DISABLED)
        if questionArea.get(1.0,"end-1c")==question[0]:
           optionButton2.config(text='')
           optionButton4.config(text="")
        if questionArea.get(1.0,"end-1c")==question[1]:
           optionButton1.config(text='')
           optionButton2.config(text="")
        if questionArea.get(1.0,"end-1c")==question[2]:
           optionButton1.config(text="")
           optionButton4.config(text="")
        if questionArea.get(1.0,"end-1c")==question[3]:
           optionButton2.config(text="")
           optionButton4.config(text="")
        if questionArea.get(1.0,"end-1c")==question[4]:
           optionButton1.config(text="")
           optionButton3.config(text="")
        if questionArea.get(1.0,"end-1c")==question[5]:
           optionButton2.config(text="")
           optionButton4.config(text="")
        if questionArea.get(1.0,"end-1c")==question[6]:
           optionButton1.config(text="")
           optionButton3.config(text="")
        if questionArea.get(1.0,"end-1c")==question[7]:
           optionButton1.config(text="")
           optionButton3.config(text="")
        if questionArea.get(1.0,"end-1c")==question[8]:
           optionButton2.config(text="")
           optionButton4.config(text="")
        if questionArea.get(1.0,"end-1c")==question[9]:
           optionButton1.config(text="")
           optionButton3.config(text="")
        if questionArea.get(1.0,"end-1c")==question[10]:
           optionButton1.config(text="")
           optionButton2.config(text="")
        if questionArea.get(1.0,"end-1c")==question[11]:
           optionButton3.config(text="")
           optionButton4.config(text="")
        if questionArea.get(1.0,"end-1c")==question[12]:
           optionButton1.config(text="")
           optionButton4.config(text="")
        if questionArea.get(1.0,"end-1c")==question[13]:
           optionButton1.config(text="")
           optionButton3.config(text="")
        if questionArea.get(1.0,"end-1c")==question[14]:
           optionButton2.config(text="")
           optionButton4.config(text="")
    def audiencePoleLifeLine():
        audiencePoleButton.config(image=audiencePoleX, state=DISABLED)
        progressBarA.place(x=580, y=190)
        progressBarB.place(x=620, y=190)
        progressBarC.place(x=660, y=190)
        progressBarD.place(x=700, y=190)

        progressbarLabelA.place(x=580, y=320)
        progressbarLabelB.place(x=620, y=320)
        progressbarLabelC.place(x=660, y=320)
        progressbarLabelD.place(x=700, y=320)

        if questionArea.get(1.0,"end-1c")==question[0]:
           progressBarA.config(value=30)
           progressBarB.config(value=50)
           progressBarC.config(value=90)
           progressBarD.config(value=60)
        if questionArea.get(1.0,"end-1c")==question[1]:
           progressBarA.config(value=30)
           progressBarB.config(value=50)
           progressBarC.config(value=70)
           progressBarD.config(value=40)
        if questionArea.get(1.0,"end-1c")==question[2]:
           progressBarA.config(value=20)
           progressBarB.config(value=70)
           progressBarC.config(value=40)
           progressBarD.config(value=30)
        if questionArea.get(1.0,"end-1c")==question[3]:
           progressBarA.config(value=70)
           progressBarB.config(value=20)
           progressBarC.config(value=40)
           progressBarD.config(value=50)
        if questionArea.get(1.0,"end-1c")==question[4]:
           progressBarA.config(value=20)
           progressBarB.config(value=30)
           progressBarC.config(value=40)
           progressBarD.config(value=70)
        if questionArea.get(1.0,"end-1c")==question[5]:
           progressBarA.config(value=70)
           progressBarB.config(value=40)
           progressBarC.config(value=20)
           progressBarD.config(value=10)
        if questionArea.get(1.0,"end-1c")==question[6]:
           progressBarA.config(value=40)
           progressBarB.config(value=60)
           progressBarC.config(value=30)
           progressBarD.config(value=50)
        if questionArea.get(1.0,"end-1c")==question[7]:
           progressBarA.config(value=10)
           progressBarB.config(value=60)
           progressBarC.config(value=40)
           progressBarD.config(value=30)
        if questionArea.get(1.0,"end-1c")==question[8]:
           progressBarA.config(value=20)
           progressBarB.config(value=40)
           progressBarC.config(value=70)
           progressBarD.config(value=50)
        if questionArea.get(1.0,"end-1c")==question[9]:
           progressBarA.config(value=30)
           progressBarB.config(value=70)
           progressBarC.config(value=50)
           progressBarD.config(value=20)
        if questionArea.get(1.0,"end-1c")==question[10]:
           progressBarA.config(value=20)
           progressBarB.config(value=50)
           progressBarC.config(value=70)
           progressBarD.config(value=30)
        if questionArea.get(1.0,"end-1c")==question[11]:
           progressBarA.config(value=20)
           progressBarB.config(value=70)
           progressBarC.config(value=50)
           progressBarD.config(value=40)
        if questionArea.get(1.0,"end-1c")==question[12]:
           progressBarA.config(value=20)
           progressBarB.config(value=70)
           progressBarC.config(value=40)
           progressBarD.config(value=50)
        if questionArea.get(1.0,"end-1c")==question[13]:
           progressBarA.config(value=20)
           progressBarB.config(value=70)
           progressBarC.config(value=30)
           progressBarD.config(value=40)
        if questionArea.get(1.0,"end-1c")==question[14]:
           progressBarA.config(value=20)
           progressBarB.config(value=40)
           progressBarC.config(value=70)
           progressBarD.config(value=50)

    def phoneLifeLine():
        mixer.music.load("calling.mp3")
        mixer.music.play()
        callButtton.place(x=70,y=260)
        phoneLifeLineButton.config(image=phoneImageX,state=DISABLED)

    def phoneclick():
        for i in range(15):
           if questionArea.get(1.0,'end-1c')==question[i]:
              engine.say(f"The answer is {correct_answers[i]}")
              engine.runAndWait()
              mixer.init()
              mixer.music.load("kbc.mp3")
              mixer.music.play(-1)

    





    if category == "GENERAL KNOWLEDGE":
        correct_answers = [
        "Tokyo","Canberra", "Mars","Shakespeare","Pacific Ocean",
        "1776", "Vincent van Gogh", "Yen", "Nitrogen",
        "Albert Einstein", "Japan", "Blue whale",
        "Helium", "Harper Lee", "Ottawa"]

        question=["What is the capital of Japan?",
            "What is the capital city of Australia?",
            "Which planet is known as the Red Planet?",
            "Who wrote 'Romeo and Juliet?",
            "What is the largest ocean on Earth?",
            "In what year did the United States declare its independence?",
            "Who painted the famous artwork \"Starry Night\"?",
            "What is the currency of Japan?",
            "Which gas makes up the majority of Earth's atmosphere?",
            "Who is known as the \"Father of Modern Physics\"?",
            "Which country is known as the \"Land of the Rising Sun\"?",
            "What is the largest mammal in the world?",
            "Which of the following elements is a noble gas?",
            "Who wrote the famous novel \"To Kill a Mockingbird\"?",
            "What is the capital city of Canada?"]

        First_options = [
            "Seoul",
            "Sydney",
            "Venus",
            "Shakespeare",
            "Atlantic Ocean",
            "1776",
            "Pablo Picasso",
            "Won",
            "Oxygen",
            "Isaac Newton",
            "China",
            "Elephant",
            "Oxygen",
            "J.K. Rowling",
            "Vancouver"
        ]
        Second_options = [
        "Beijing","Melbourne", "Mars", "Jane Aust", "Indian Ocean",
        "1789", "Vincent van Gogh", "Yen", "Carbon dioxide",
        "Albert Einstein", "South Korea", "Blue whale",
        "Helium", "Harper Lee", "Toronto"
        ]

        Third_options = [
        "Tokyo","Canberra", "Jupiter", "C.Dickens","Southern Ocean",
        "1800", "Leonardo Vinci", "Baht", "Nitrogen",
        "Galilei", "Japan", "Giraffe",
        "Sodium", "Ernest Hemingway", "Ottawa"
        ]

        Fourth_options = [
        "BangKok","Brisbane", "Saturn","Emily Brontë", "Pacific Ocean",
        "1865", "Claude Monet", "Ringgit", "Hydrogen",
        "Nikola Tesla", "Vietnam","Gorilla",
        "Carbon", "Scott gerald", "Montreal"
        ]
        
    
    #GEOGRAPHY 

    elif category == "GEOGRAPHY": 
          correct_answers = [
            "Canberra",
            "Brazil",
            "Nile",
            "Russia",
            "Canada",
            "Mount Everest",
            "Tokyo",
            "France",
            "Arctic Ocean",
            "India",
            "Antarctica",
            "China",
            "Pacific Ocean",
            "Mexico",
            "Africa"
            ]
          question = [
                "What is the capital city of Australia?",
                "Which country is the largest by land area?",
                "What is the longest river in the world?",
                "Which country spans across Europe and Asia?",
                "Which is the second largest country by land area?",
                "Which is the highest mountain peak on Earth?",
                "What is the capital city of Japan?",
                "Which country is famous for the Eiffel Tower?",
                "Which ocean is the smallest and shallowest?",
                "Which country is known for the Taj Mahal?",
                "Which continent is entirely located in the Southern Hemisphere?",
                "Which country has the largest population?",
                "Which ocean is the largest and deepest?",
                "Which country is known for the ancient ruins of Chichen Itza?",
                "Which continent is known as the 'Dark Continent'?"
            ]

          First_options = [
                "Sydney",
                "Australia",
                "Amazon",
                "United States",
                "Russia",
                "K2",
                "Beijing",
                "Italy",
                "Indian Ocean",
                "Brazil",
                "Asia",
                "India",
                "Atlantic Ocean",
                "USA",
                "Asia"
            ]

          Second_options = [
                "Melbourne",
                "India",
                "Mississippi",
                "China",
                "China",
                "Kangchenjunga",
                "Osaka",
                "Germany",
                "Southern Ocean",
                "India",
                "Australia",
                "Brazil",
                "Indian Ocean",
                "Spain",
                "Europe"
            ]

          Third_options = [
                "Canberra",
                "Brazil",
                "Nile",
                "Canada",
                "USA",
                "Mount Everest",
                "Seoul",
                "UK",
                "Arctic Ocean",
                "Japan",
                "Europe",
                "USA",
                "Pacific Ocean",
                "Canada",
                "South America"
            ]

          Fourth_options = [
                "Perth",
                "Australia",
                "Ganges",
                "Russia",
                "India",
                "Mont Blanc",
                "Tokyo",
                "France",
                "Atlantic Ocean",
                "Australia",
                "Antarctica",
                "China",
                "Southern Ocean",
                "Mexico",
                "Australia"
   
            ]

        #HISTORY 
    elif category == "HISTORY":
          correct_answers = [
                    "1776",
                    "Julius Caesar",
                    "Marie Curie",
                    "World War II",
                    "Industrial Revolution",
                    "Magna Carta",
                    "Nelson Mandela",
                    "Vietnam War",
                    "Russia",
                    "Napoleon Bonaparte",
                    "Great Depression",
                    "Cleopatra",
                    "Renaissance",
                    "Winston Churchill",
                    "Silk Road"
        ]

          question = [
            "In what year did the United States declare its independence?",
            "Who was the first Roman Emperor?",
            "Who was the first woman to win a Nobel Prize?",
            "During which conflict was the Battle of Stalingrad fought?",
            "Which period saw major advancements in manufacturing, transportation, and technology?",
            "What was the name of the document signed by King John of England in 1215?",
            "Who was the first black President of South Africa?",
            "Which war ended with the fall of Saigon in 1975?",
            "The Bolshevik Revolution of 1917 took place in which country?",
            "Who famously said, 'A soldier will fight long and hard for a bit of colored ribbon'?",
            "What was the name given to the period of severe economic downturn in the 1930s?",
            "Who was the last active pharaoh of ancient Egypt?",
            "Which period in European history is known for its revival of art, literature, and learning?",
            "Who was the British Prime Minister during World War II?",
            "What ancient network of trade routes connected the East and West?"
        ]

          First_options = [
            "1789",
            "Julius Caesar",
            "Margaret Thatcher",
            "World War I",
            "Industrial Revolution",
            "Treaty of Versailles",
            "Martin Luther King Jr.",
            "Korean War",
            "Germany",
            "Napoleon Bonaparte",
            "World War I",
            "Hatshepsut",
            "Middle Ages",
            "Franklin D. Roosevelt",
            "Spice Route"
        ]

          Second_options = [
            "1776",
            "Augustus",
            "Rosa Parks",
            "World War II",
            "Victorian Era",
            "Magna Carta",
            "Malcolm X",
            "Gulf War",
            "Russia",
            "Winston Churchill",
            "Great Depression",
            "Cleopatra",
            "Renaissance",
            "Neville Chamberlain",
            "Trans-Saharan Route"
        ]

          Third_options = [
            "1800",
            "Nero",
            "Marie Curie",
            "Cold War",
            "Renaissance",
            "Declaration of Independence",
            "Nelson Mandela",
            "Afghanistan War",
            "France",
            "Joseph Stalin",
            "Cold War",
            "Nefertiti",
            "Enlightenment",
            "Margaret Thatcher",
            "Silk Road"
        ]

          Fourth_options = [
            "1865",
            "Claudius",
            "Florence Nightingale",
            "Vietnam War",
            "Enlightenment",
            "Emancipation Proclamation",
            "Barack Obama",
            "Vietnam War",
            "China",
            "Otto von Bismarck",
            "Dust Bowl",
            "Queen Elizabeth I",
            "Industrial Revolution",
            "Winston Churchill",
            "Marco Polo Route"
        ]

    

            #LITERATURE

    
    elif category == "LITERATURE":
          correct_answers = [
            "William Shakespeare",
            "Charles Dickens",
            "Leo Tolstoy",
            "J.K. Rowling",
            "Herman Melville",
            "Romeo and Juliet",
            "George Orwell",
            "Harper Lee",
            "Agatha Christie",
            "Hamlet",
            "J.R.R. Tolkien",
            "Mark Twain",
            "George R.R. Martin",
            "Jane Austen",
            "Miguel de Cervantes"
        ]

          question = [
            "Who is the author of 'Romeo and Juliet'?",
            "Who wrote the novel 'Great Expectations'?",
            "Who wrote 'War and Peace'?",
            "Who is the author of the 'Harry Potter' series?",
            "Who wrote 'Moby-Dick'?",
            "Which play is known as 'The Tragedy of the Prince of Denmark'?",
            "Who wrote '1984'?",
            "Who authored 'To Kill a Mockingbird'?",
            "Who created the fictional detective Hercule Poirot?",
            "Which Shakespearean tragedy features the character Ophelia?",
            "Who wrote 'The Lord of the Rings' trilogy?",
            "Who wrote 'The Adventures of Huckleberry Finn'?",
            "Who is the author of 'A Song of Ice and Fire' series?",
            "Who wrote 'Pride and Prejudice'?",
            "Who wrote 'Don Quixote'?"
        ]

          First_options = [
            "William Wordsworth",
            "Charles Dickens",
            "Fyodor Dostoevsky",
            "J.K. Rowling",
            "Herman Melville",
            "Macbeth",
            "George Orwell",
            "Harper Lee",
            "Arthur Conan Doyle",
            "King Lear",
            "J.K. Rowling",
            "Ernest Hemingway",
            "J.R.R. Tolkien",
            "Emily Brontë",
            "Leo Tolstoy"
        ]

          Second_options = [
            "George Orwell",
            "George Eliot",
            "Leo Tolstoy",
            "Stephen King",
            "Mark Twain",
            "Romeo and Juliet",
            "Aldous Huxley",
            "Truman Capote",
            "Agatha Christie",
            "Hamlet",
            "George R.R. Martin",
            "F. Scott Fitzgerald",
            "George R.R. Martin",
            "Jane Austen",
            "Miguel de Cervantes"
        ]

          Third_options = [
            "John Milton",
            "Jane Austen",
            "Leo Tolstoy",
            "J.R.R. Tolkien",
            "Charles Dickens",
            "Othello",
            "J.R.R. Tolkien",
            "J.D. Salinger",
            "Raymond Chandler",
            "Macbeth",
            "J.R.R. Tolkien",
            "Charles Dickens",
            "J.K. Rowling",
            "Charlotte Brontë",
            "Fyodor Dostoevsky"
        ]

          Fourth_options = [
            "William Shakespeare",
            "Herman Melville",
            "Fyodor Dostoevsky",
            "Dan Brown",
            "Ernest Hemingway",
            "King Lear",
            "George Orwell",
            "Harper Lee",
            "Sir Arthur Conan Doyle",
            "Othello",
            "Mark Twain",
            "Mark Twain",
            "J.K. Rowling",
            "Jane Austen",
            "Kodor Dostoe"
        ]


        #MUSIC
    elif category == "MUSIC":
          correct_answers = [
            "Michael Jackson",
            "Mozart",
            "The Beatles",
            "Elvis Presley",
            "Adele",
            "Led Zeppelin",
            "Beethoven",
            "Madonna",
            "Bach",
            "Queen",
            "Johnny Cash",
            "Taylor Swift",
            "Pink Floyd",
            "Stevie Wonder",
            "Beyoncé"
        ]

          question = [
            "Who is known as the 'King of Pop'?",
            "Who composed 'The Magic Flute'?",
            "Which band is often referred to as the 'Fab Four'?",
            "Who is often referred to as the 'King of Rock and Roll'?",
            "Which artist released the album '21'?",
            "Which band released the iconic song 'Stairway to Heaven'?",
            "Who composed 'Für Elise'?",
            "Who is often referred to as the 'Queen of Pop'?",
            "Which composer is known for composing 'Air on the G String'?",
            "Which band sang 'Bohemian Rhapsody'?",
            "Who is known as the 'Man in Black'?",
            "Which artist released the album '1989'?",
            "Which band released the album 'The Dark Side of the Moon'?",
            "Who is often referred to as the 'Prince of Motown'?",
            "Which artist released the album 'Lemonade'?"
        ]

          First_options = [
            "Michael Jackson",
            "Beethoven",
            "The Rolling Stones",
            "Elton John",
            "Beyoncé",
            "Pink Floyd",
            "J.S. Bach",
            "Madonna",
            "Mozart",
            "The Beatles",
            "Johnny Cash",
            "Adele",
            "The Beatles",
            "Stevie Wonder",
            "Rihanna"
        ]

          Second_options = [
            "Elvis Presley",
            "Mozart",
            "The Beatles",
            "Bob Dylan",
            "Taylor Swift",
            "Led Zeppelin",
            "Mozart",
            "Lady Gaga",
            "Beethoven",
            "Led Zeppelin",
            "Elvis Presley",
            "Katy Perry",
            "The Rolling Stones",
            "Marvin Gaye",
            "Britney Spears"
        ]

          Third_options = [
            "Prince",
            "Bach",
            "The Beach Boys",
            "Chuck Berry",
            "Adele",
            "The Eagles",
            "Johann Strauss II",
            "Whitney Houston",
            "Chopin",
            "The Rolling Stones",
            "David Bowie",
            "Ariana Grande",
            "Pink Floyd",
            "Ray Charles",
            "Mariah Carey"
        ]

          Fourth_options = [
            "Stevie Wonder",
            "Beethoven",
            "The Beatles",
            "Elvis Presley",
            "Mariah Carey",
            "AC/DC",
            "Frederic Chopin",
            "Celine Dion",
            "Brahms",
            "Pink Floyd",
            "Johnny Cash",
            "Taylor Swift",
            "Led Zeppelin",
            "B.B. King",
            "Beyoncé"
        ]

        #POP CULTURE
    elif category == "POP CULTURE":
          correct_answers = [
            "Beyoncé",
            "Leonardo DiCaprio",
            "Taylor Swift",
            "Kim Kardashian",
            "Harry Potter",
            "Stranger Things",
            "Drake",
            "Ariana Grande",
            "Game of Thrones",
            "Michael Jackson",
            "Friends",
            "Beyoncé and Jay-Z",
            "BTS",
            "Lady Gaga",
            "Justin Bieber"
        ]

          question = [
            "Who is known as the 'Queen B' of music?",
            "Who won an Oscar for Best Actor for his role in 'The Revenant'?",
            "Who is known as the 'Queen of Pop'?",
            "Who became famous after a leaked tape with Ray J?",
            "Which book series features a character named Hermione Granger?",
            "Which TV series features a group of kids facing supernatural events in a small town called Hawkins?",
            "Who released the album 'Scorpion' in 2018?",
            "Which singer is known as the 'Princess of Pop'?",
            "Which TV series is based on the book series 'A Song of Ice and Fire'?",
            "Who is known as the 'King of Pop'?",
            "Which TV series revolves around the lives of six friends living in New York City?",
            "Which celebrity couple is often referred to as 'Bey-Z'?",
            "Which K-pop group has members named RM, Jin, Suga, J-Hope, Jimin, V, and Jungkook?",
            "Who performed the halftime show at the Super Bowl LI in 2017?",
            "Who gained popularity after being discovered by talent manager Scooter Braun on YouTube?"
        ]

          First_options = [
            "Adele",
            "Johnny Depp",
            "Rihanna",
            "Paris Hilton",
            "Twilight",
            "The Crown",
            "Kanye West",
            "Britney Spears",
            "Breaking Bad",
            "Elvis Presley",
            "How I Met Your Mother",
            "Kanye West and Kim Kardashian",
            "BLACKPINK",
            "Madonna",
            "Selena Gomez"
        ]

          Second_options = [
            "Taylor Swift",
            "Leonardo DiCaprio",
            "Madonna",
            "Kim Kardashian",
            "The Hunger Games",
            "Stranger Things",
            "Drake",
            "Lady Gaga",
            "Stranger Things",
            "Michael Jackson",
            "The Office",
            "Jay-Z and Rihanna",
            "EXO",
            "Rihanna",
            "Justin Timberlake"
        ]

          Third_options = [
            "Beyoncé",
            "Tom Cruise",
            "Beyoncé",
            "Kylie Jenner",
            "Harry Potter",
            "Riverdale",
            "Eminem",
            "Katy Perry",
            "The Witcher",
            "Prince",
            "Friends",
            "Beyoncé and Jay-Z",
            "NCT",
            "Beyoncé",
            "Shawn Mendes"
        ]

          Fourth_options = [
            "Ariana Grande",
            "Brad Pitt",
            "Taylor Swift",
            "Kendall Jenner",
            "Game of Thrones",
            "Gossip Girl",
            "Justin Bieber",
            "Ariana Grande",
            "Game of Thrones",
            "Justin Bieber",
            "Glee",
            "Selena Gomez and Justin Bieber",
            "BTS",
            "Katy Perry",
            "Justin Bieber"
        ]
   
        #SPORT
    elif category == "SPORT" :
          correct_answers = [
            "Michael Jordan",
            "Muhammad Ali",
            "Cristiano Ronaldo",
            "Serena Williams",
            "Lionel Messi",
            "Usain Bolt",
            "Basketball",
            "Novak Djokovic",
            "Roger Federer",
            "Michael Phelps",
            "Simone Biles",
            "Tiger Woods",
            "Rafael Nadal",
            "Tom Brady",
            "Sachin Tendulkar"
        ]

          question = [
            "Who is often considered the greatest basketball player of all time?",
            "Who is known as 'The Greatest' in boxing?",
            "Which footballer has won the most FIFA Ballon d'Or awards?",
            "Who holds the record for the most Grand Slam singles titles in tennis?",
            "Who has won the most FIFA Ballon d'Or awards in football?",
            "Who holds the world record for the 100m sprint?",
            "Which sport is associated with Wilt Chamberlain?",
            "Who has won the most Australian Open titles in men's singles tennis?",
            "Which tennis player has won the most Wimbledon titles?",
            "Who holds the record for the most Olympic gold medals in swimming?",
            "Who is often regarded as the greatest gymnast of all time?",
            "Who is considered one of the greatest golfers of all time?",
            "Who has won the most French Open titles in men's singles tennis?",
            "Who is the quarterback with the most Super Bowl wins?",
            "Who is often referred to as the 'God of Cricket'?"
        ]

          First_options = [
            "Kobe Bryant",
            "Mike Tyson",
            "Lionel Messi",
            "Venus Williams",
            "Cristiano Ronaldo",
            "Carl Lewis",
            "Football",
            "Rafael Nadal",
            "Novak Djokovic",
            "Mark Spitz",
            "Nadia Comăneci",
            "Jack Nicklaus",
            "Andre Agassi",
            "Peyton Manning",
            "Virat Kohli"
        ]

          Second_options = [
            "LeBron James",
            "Floyd Mayweather Jr.",
            "Cristiano Ronaldo",
            "Serena Williams",
            "Lionel Messi",
            "Usain Bolt",
            "Tennis",
            "Andy Murray",
            "Roger Federer",
            "Michael Phelps",
            "Simone Biles",
            "Arnold Palmer",
            "Roger Federer",
            "Tom Brady",
            "Sachin Tendulkar"
        ]

          Third_options = [
            "Magic Johnson",
            "Muhammad Ali",
            "Neymar",
            "Steffi Graf",
            "Neymar",
            "Asafa Powell",
            "Golf",
            "Stan Wawrinka",
            "Rafael Nadal",
            "Usain Bolt",
            "Aly Raisman",
            "Phil Mickelson",
            "Rafael Nadal",
            "Joe Montana",
            "Ricky Ponting"
        ]

          Fourth_options = [
            "Michael Jordan",
            "Sugar Ray Robinson",
            "Diego Maradona",
            "Margaret Court",
            "Diego Maradona",
            "Michael Johnson",
            "Basketball",
            "Novak Djokovic",
            "Pete Sampras",
            "LeBron James",
            "Nastia Liukin",
            "Tiger Woods",
            "Novak Djokovic",
            "Tom Brady",
            "Brian Lara"
        ]

        # COMPUTER SCIENCE 
    elif category == "COMPUTER SCIENCE":
          correct_answers = [
            "To analyze algorithm complexity",
            "A programming paradigm based on objects",
            "TCP provides reliable data delivery, while UDP is connectionless and unreliable",
            "To translate high-level code into machine code",
            "To eliminate redundancy and improve data integrity",
            "Symmetric encryption uses the same key for encryption and decryption",
            "It allows the execution of programs larger than physical memory",
            "A machine learning model inspired by the human brain",
            "To reduce the size of data for storage or transmission",
            "To store frequently accessed data for faster access",
            "A stack follows Last In, First Out (LIFO) principle",
            "Encourages code reusability and modularity",
            "A linked list stores elements sequentially in memory",
            "Recursion involves a function calling itself until a base case is reached",
            "HTTP is unencrypted, while HTTPS encrypts data for secure transmission"
        ]

          question = [
            "What is Big O notation used for in computer science?",
            "Explain the concept of object-oriented programming.",
            "What are the primary differences between TCP and UDP protocols?",
            "Describe the role of a compiler in software development.",
            "What is data normalization in databases and why is it important?",
            "Differentiate between symmetric and asymmetric encryption algorithms.",
            "Explain the concept of virtual memory in operating systems.",
            "What is a neural network and how does it differ from traditional algorithms?",
            "Describe the principles of data compression.",
            "What is the purpose of a cache in computer architecture?",
            "Differentiate between a stack and a queue in data structures.",
            "What are the advantages and disadvantages of object-oriented programming?",
            "Explain the difference between a linked list and an array.",
            "How does recursion work in algorithm design?",
            "Describe the role of HTTP and HTTPS in web communication."
        ]

          First_options = [
            "To analyze algorithm complexity",
            "A programming paradigm based on objects",
            "TCP provides reliable data delivery, while UDP is connectionless and unreliable",
            "To translate high-level code into machine code",
            "To eliminate redundancy and improve data integrity",
            "Symmetric encryption uses the same key for encryption and decryption",
            "It allows the execution of programs larger than physical memory",
            "A machine learning model inspired by the human brain",
            "To reduce the size of data for storage or transmission",
            "To store frequently accessed data for faster access",
            "A stack follows Last In, First Out (LIFO) principle",
            "Encourages code reusability and modularity",
            "A linked list stores elements sequentially in memory",
            "Recursion involves a function calling itself until a base case is reached",
            "HTTP is unencrypted, while HTTPS encrypts data for secure transmission"
        ]

          Second_options = [
            "To store large datasets efficiently",
            "A programming paradigm based on functions",
            "TCP is connectionless, while UDP provides reliable data delivery",
            "To interpret code line by line during execution",
            "To organize data in a hierarchical structure",
            "Asymmetric encryption is faster than symmetric encryption",
            "It allows multiple processes to share a single CPU",
            "A search algorithm for finding optimal solutions",
            "To increase the size of data for better analysis",
            "To enhance the functionality of CPU registers",
            "A queue follows First In, First Out (FIFO) principle",
            "Encourages procedural programming",
            "An array provides constant-time access to elements",
            "Recursion involves dividing a problem into smaller subproblems",
            "HTTP compresses data for faster transmission"
        ]

          Third_options = [
            "To design user interfaces",
            "A programming paradigm based on procedures",
            "TCP guarantees packet delivery, while UDP doesn't guarantee",
            "To manage hardware resources and provide services",
            "To optimize database query performance",
            "Symmetric encryption is more secure than asymmetric encryption",
            "It increases the execution speed of programs",
            "A sorting algorithm for arranging data alphabetically",
            "To eliminate data redundancy for better storage efficiency",
            "To facilitate parallel processing",
            "Both have the same principles",
            "Encourages functional programming",
            "Both have the same characteristics",
            "Recursion involves sorting elements sequentially",
            "HTTP adds layers of security to data transmission"
        ]

          Fourth_options = [
            "To measure the speed of data transmission",
            "A programming paradigm based on events",
            "TCP is faster than UDP",
            "To debug code during development",
            "To increase redundancy for data recovery",
            "Asymmetric encryption is more secure than symmetric encryption",
            "It simulates the behavior of a physical memory",
            "A machine learning model for natural language processing",
            "To improve data compression ratio",
            "To allocate memory for program execution",
            "None of the above",
            "None of the above",
            "None of the above",
            "Recursion involves a function calling itself indefinitely",
            "HTTPS slows down web communication"
        ]

            # RIDDLES

    elif category == "RIDDLES":


          correct_answers = [
            "A piano",
            "A candle",
            "The letter 'm'",
            "A coin",
            "Footsteps",
            "The piano",
            "A stamp",
            "A towel",
            "Rain",
            "Your name",
            "A bottle",
            "A leg",
            "A clock",
            "A joke",
            "A map"
    ]       
          question = [
            "What has keys but can't open locks?",
            "I'm tall when I'm young, and I'm short when I'm old. What am I?",
            "What comes once in a minute, twice in a moment, but never in a thousand years?",
            "What has a head, a tail, is brown, and has no legs?",
            "The more you take, the more you leave behind. What am I?",
            "What has many keys but can't open a single lock?",
            "What can travel around the world while staying in a corner?",
            "What gets wet while drying?",
            "What comes down but never goes up?",
            "What belongs to you, but other people use it more than you do?",
            "What has a neck but no head?",
            "What has a bottom at the top?",
            "What has a face and two hands but no arms or legs?",
            "What can be cracked, made, told, and played?",
            "What has cities, but no houses; forests, but no trees; and rivers, but no water?"
        ]

          First_options = [
            "A piano",
            "A tree",
            "The letter 'a'",
            "A snake",
            "Footsteps",
            "A keyboard",
            "A stamp",
            "A towel",
            "Rain",
            "Your name",
            "A bottle",
            "A leg",
            "A clock",
            "A joke",
            "A map"
        ]

          Second_options = [
            "A keyboard",
            "A candle",
            "The letter 'e'",
            "A coin",
            "Leaves",
            "A piano",
            "The book",
            "A sponge",
            "Sunset",
            "Your phone number",
            "A giraffe",
            "A hat",
            "A watch",
            "A song",
            "A globe"
        ]

          Third_options = [
            "A book",
            "A pencil",
            "The letter 'm'",
            "A penny",
            "Memories",
            "A remote",
            "A stone",
            "A mirror",
            "A bird",
            "Your email address",
            "A book",
            "A snake",
            "A mirror",
            "A story",
            "A dictionary"
        ]

          Fourth_options = [
            "A flute",
            "A coin",
            "The letter 'o'",
            "A dog",
            "Time",
            "A password",
            "A wind",
            "A hairdryer",
            "A moon",
            "Your social security number",
            "A niddle",
            "A tree",
            "A clamp",
            "A riddle",
            "A forest"
        ]



            # SCIENCE AND TECHNOLOGY
        
    elif category == "SCIENCE AND TECHNOLOGY":


          correct_answers = [
                "Photosynthesis",
                "Albert Einstein",
                "Atom",
                "Central Processing Unit",
                "Mercury",
                "Tim Berners-Lee",
                "Deoxyribonucleic Acid",
                "Carbon Dioxide",
                "H2O",
                "Meteorology",
                "Cheetah",
                "Albert Einstein",
                "Newton",
                "Evaporation",
                "Skin"
        ]

          question = [
            "What is the process of converting light energy into electrical energy known as?",
            "Which famous scientist developed the theory of relativity?",
            "What is the smallest unit of matter?",
            "What does CPU stand for in the context of computing?",
            "What is the name of the closest planet to the Sun in our solar system?",
            "Who is credited with inventing the World Wide Web?",
            "What does DNA stand for in biology?",
            "Which gas do plants use for photosynthesis?",
            "What is the chemical symbol for water?",
            "What is the study of Earth's atmosphere called?",
            "What is the fastest animal on land?",
            "Who is known as the 'father of modern physics'?",
            "What is the SI unit of force?",
            "What is the process of a liquid turning into a gas called?",
            "What is the largest organ in the human body?"
        ]

          First_options = [
            "Photosynthesis",
            "Isaac Newton",
            "Atom",
            "Central Processing Unit",
            "Mars",
            "Tim Berners-Lee",
            "Deoxyribonucleic Acid",
            "Oxygen",
            "H2O",
            "Geology",
            "Cheetah",
            "Albert Einstein",
            "Joule",
            "Sublimation",
            "Liver"
        ]

          Second_options = [
            "Respiration",
            "Albert Einstein",
            "Molecule",
            "Computer Processing Unit",
            "Venus",
            "Nikola Tesla",
            "Ribonucleic Acid",
            "Carbon Dioxide",
            "O2",
            "Meteorology",
            "Lion",
            "Galileo Galilei",
            "Watt",
            "Evaporation",
            "Brain"
        ]

          Third_options = [
            "Transmutation",
            "Galileo Galilei",
            "Proton",
            "Central Power Unit",
            "Mercury",
            "Tim Cook",
            "Deoxyribonucleic Acid",
            "Nitrogen",
            "CO",
            "Oceanography",
            "Leopard",
            "Isaac Newton",
            "Newton",
            "Condensation",
            "Skin"
        ]

          Fourth_options = [
            "Solarization",
            "Johannes Kepler",
            "Electron",
            "Central Power Unit",
            "Earth",
            "Al Gore",
            "None of the above",
            "Hydrogen",
            "H2O2",
            "Meteorology",
            "Giraffe",
            "Niels Bohr",
            "Pascal",
            "Deposition",
            "Heart"
        ]

   
    else:
        messagebox.showerror("Invalid Category", "Please select a valid category.")
        return
      

  


    def shuffle_questions_and_options():
        global question, First_options, Second_options, Third_options, Fourth_options, correct_answers, lifelines
        # Shuffle the questions, options, correct answers, and lifelines together
        questions_and_options = list(zip(question, First_options, Second_options, Third_options, Fourth_options, correct_answers, lifelines))
        random.shuffle(questions_and_options)

        # Unpack the shuffled values
        question, First_options, Second_options, Third_options, Fourth_options, correct_answers, lifelines = zip(*questions_and_options)

        # Shuffle the lifelines
        random.shuffle(lifelines)

        # Place the function call here to shuffle questions and options initially
        shuffle_questions_and_options()






    root=Tk()
    root.geometry("1430x1430+0+0")
    root.title("who want to be a millionaire created by Terry.G.")

    root.config(bg="black")
    #==============================================Frames=====================================#
    leftframe=Frame(root,bg = "black",padx=90)
    leftframe.grid()

    topFrame = Frame(leftframe,bg="black",pady=15)
    topFrame.grid()

    centerFrame = Frame(leftframe,bg="black",pady=15)
    centerFrame.grid(row=1, column=0)

    bottomFrame = Frame(leftframe)
    bottomFrame.grid(row=2, column=0)

    rightframe=Frame(root,pady=25,padx=50,bg="black")
    rightframe.grid(row=0, column=1)
    #===============================================IMAGES================================================#
    image50=PhotoImage(file="50-50.png")
    image50X=PhotoImage(file="50-50-X.png")

    lifeline50Button = Button(topFrame, image=image50, bg="black",bd=0,activebackground='black',width=180,height=80,command=lifeline50)

    lifeline50Button.grid(row=0,column=0)

    audiencePoleX=PhotoImage(file="audiencePoleX.png")
    audiencePoleButton = Button(topFrame, image=audiencePoleX,bg="black",bd=0,activebackground="black",width=180,height=80,command=audiencePoleLifeLine)
    audiencePoleButton.grid(row=0,column=1)

    audiencePole=PhotoImage(file="audiencePole.png")
    audiencePoleButton = Button(topFrame, image=audiencePole,bg="black",bd=0,activebackground="black",width=180,height=80,command=audiencePoleLifeLine)
    audiencePoleButton.grid(row=0,column=1)

    phoneImage=PhotoImage(file="phoneAFriend.png")
    phoneImageX=PhotoImage(file="phoneAFriendX.png")

    phoneLifeLineButton = Button(topFrame,image=phoneImage,bg="black",bd=0,activebackground='black',width=180,height=80,command=phoneLifeLine)
    phoneLifeLineButton.grid(row=0,column=2)

    callimage=PhotoImage(file="phone.png")
    callButtton=Button(root,image=callimage,bd=0,bg="black",activebackground="black",cursor="hand2", command=phoneclick)

    centerImage= PhotoImage(file="center.png")
    logoLabel=Label(centerFrame, image=centerImage,bg="black",width=300,height=200)
    logoLabel.grid()

    amountImage=PhotoImage(file="Picture0.png")
    amountImage1=PhotoImage(file="Picture1.png")
    amountImage2=PhotoImage(file="Picture2.png")
    amountImage3=PhotoImage(file="Picture3.png")
    amountImage4=PhotoImage(file="Picture4.png")
    amountImage5=PhotoImage(file="Picture5.png")
    amountImage6=PhotoImage(file="Picture6.png")
    amountImage7=PhotoImage(file="Picture7.png")
    amountImage8=PhotoImage(file="Picture8.png")
    amountImage9=PhotoImage(file="Picture9.png")
    amountImage10=PhotoImage(file="Picture10.png")
    amountImage11=PhotoImage(file="Picture11.png")
    amountImage12=PhotoImage(file="Picture12.png")
    amountImage13=PhotoImage(file="Picture13.png")
    amountImage14=PhotoImage(file="Picture14.png")
    amountImage15=PhotoImage(file="Picture15.png")

    amountImages = [amountImage1, amountImage2, amountImage3, amountImage4, amountImage5,
                    amountImage6, amountImage7, amountImage8, amountImage9, amountImage10,
                    amountImage11, amountImage12, amountImage13, amountImage14, amountImage15]
    amountLabel=Label(rightframe,image=amountImage,bg="black")
    amountLabel.grid()

    LayoutImage=PhotoImage(file="lay.png")
    LayoutLabel=Label(bottomFrame, image=LayoutImage,bg="black")
    LayoutLabel.grid()
    #shufffle the questions and corresponding options
    #questions_and_options = list(zip(question, First_options, Second_options, Third_options, Fourth_options, correct_answers))
    #random.shuffle(questions_and_options)

    # Unpack the shuffled values
    #question, First_options, Second_options, Third_options, Fourth_options, correct_answers = zip(*questions_and_options)
    ##shuffled_data = list(zip(shuffled_questions, shuffled_options, correct_answers))
    #random.shuffle(shuffled_data)
    #shuffled_questions, shuffled_options, correct_answers = zip(*shuffled_data)

    #=============================================QUESTION AREA==========================================#
    questionArea=Text(bottomFrame, font=("arial",18,"bold"),width=34,height=2,wrap="word",bg="black",fg="white",bd=0)
    questionArea.place(x=70,y=10)

    questionArea.insert(END,question[0])

    labelA = Label(bottomFrame,font=("arial",16,"bold"), text="A: ", bg="black", fg="white",)
    labelA.place(x=60,y=110)

    optionButton1=Button(bottomFrame, text= First_options[0],font=("arial",16,"bold"),bg="black", fg="white",bd=0,activebackground="black",activeforeground='white',cursor="hand2",wraplength=130)#width=20)
    #optionButton1 = Button(bottomFrame, text=First_options[0], font=("arial", 18, "bold"), bg="black", fg="white",
                        #  bd=0, activebackground="black", activeforeground='white', cursor="hand2",
                        #  command=lambda: show_full_text(First_options[0]), wraplength=200)
    optionButton1.place(x=100, y=100)

    labelB = Label(bottomFrame,font=("arial",15,"bold"), text="B: ", bg="black", fg="white",)
    labelB.place(x=330,y=110)
    optionButton2=Button(bottomFrame, text= Second_options[0],font=("arial",15,"bold"),bg="black", fg="white",bd=0,activebackground="black",activeforeground='white',cursor="hand2",wraplength=130)#idth=20)
    optionButton2.place(x=370, y=100)

    labelC = Label(bottomFrame,font=("arial",16,"bold"), text="C: ", bg="black", fg="white",)
    labelC.place(x=60,y=190)
    optionButton3=Button(bottomFrame, text= Third_options[0],font=("arial",15,"bold"),bg="black", fg="white",bd=0,activebackground="black",activeforeground='white',cursor="hand2",wraplength=130)#,wraplength=200,width=20)
    optionButton3.place(x=100, y=180)
    labelD = Label(bottomFrame,font=("arial",16,"bold"), text="D: ", bg="black", fg="white",)
    labelD.place(x=330,y=190)
    optionButton4=Button(bottomFrame, text= Fourth_options[0],font=("arial",15,"bold"),bg="black", fg="white",bd=0,activebackground="black",activeforeground='white',cursor="hand2",wraplength=130)#width=20)
    optionButton4.place(x=370, y=180)
    #===========================Progress Bar(AUDIENCE POLL BUTTONS AND LABEL)=================================#
    progressBarA=Progressbar(root,orient=VERTICAL,length=120)
    progressBarB=Progressbar(root,orient=VERTICAL,length=120)
    progressBarC=Progressbar(root,orient=VERTICAL,length=120)
    progressBarD=Progressbar(root,orient=VERTICAL,length=120)

    progressbarLabelA=Label(root, text="A", font=("arial",20,"bold"),bg='black', fg="white")
    progressbarLabelB=Label(root, text="B", font=("arial",20,"bold"),bg='black', fg="white")
    progressbarLabelC=Label(root, text="C", font=("arial",20,"bold"),bg='black', fg="white")
    progressbarLabelD=Label(root, text="D", font=("arial",20,"bold"),bg='black', fg="white")
    #option_mapping = {"A": progressBarA, "B": progressbarLabelB, "C": progressbarLabelC, "D": progressbarLabelD}
    #correct_answer=StringVar()



    #=======================================OPTION FUNCTION==================================================#
    optionButton1.bind('<Button-1>', select)
    optionButton2.bind('<Button-1>', select)
    optionButton3.bind('<Button-1>', select)
    optionButton4.bind('<Button-1>', select)
    


    def exit_game():
        if messagebox.askokcancel("Exit", "Are you sure you want to exit the game?"):
            # Add any necessary cleanup code here
            # For example: stop music, close files, etc.
            # Then destroy the root window
            root.destroy()
            # Optionally, you can also return to the category selection window
            show_category_selection()

    def exit_game():
        if messagebox.askokcancel("Exit", "Are you sure you want to exit the game?"):
            # Add any necessary cleanup code here
            # For example: stop music, close files, etc.
            # Then destroy the root window
            mixer.music.stop()
            root.destroy()
            # Optionally, you can also return to the category selection window
            show_category_selection()


    # Set the default style to have a red background
    root.style = ttk.Style()
    root.style.configure(".", background="red", foreground="black")

    # Create the exit button with the default style
    exit_button = ttk.Button(root, text="Exit", command=exit_game)
    exit_button.grid(row=0, column=1, sticky="ne")  



    root.mainloop()


create_login_window()



#main_game("GENERAL KNOWLEDGE")


