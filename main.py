from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

GREEN = "#9bdeac"
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = randint(8, 10)
    nr_symbols = randint(2, 4)
    nr_numbers = randint(2, 4)

    # Hard Level
    password_letters = [choice(letters) for _ in range(nr_letters)]
    password_symbols = [choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    random_password = "".join(password_list)
    input_password.insert(0, random_password)
    pyperclip.copy(random_password)


def confirm_password():
    password = input_password.get()
    confirmation_password = input_confirmation.get()

    if confirmation_password != "" and password != "":
        if confirmation_password == password:
            messagebox.showinfo(title="Information", message="Validation completed successfully.")
            return True
        else:
            messagebox.showwarning(title="Warning", message="The passwords are different, please try again.")
            input_confirmation.delete(0, "end")
            return False

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_info():
    website_name = input_website.get()
    username = input_username.get()
    user_password = input_password.get()
    new_data = {
        website_name: {
            "email": username,
            "password": user_password
        }
    }

    if confirm_password():
        if website_name != "" and username != "" and user_password != "" and username != "admin@email.com":
            is_ok = messagebox.askokcancel(title=website_name,
                                           message=f"There are the details entered: \nEmail: {username}"
                                                   f"\n Password: {user_password} \n Is it ok to save?")
            if is_ok:
                try:
                    with open("data.json", mode="r") as file:
                        data = json.load(file)  # reading old data
                except FileNotFoundError:
                    with open("data.json", mode="w") as file:
                        json.dump(new_data, file, indent=4)
                else:
                    data.update(new_data)  # updating old data with new data
                    with open("data.json", mode="w") as file:
                        json.dump(data, file, indent=4)  # saving and writing updated data
                finally:
                    input_website.delete(0, "end")
                    input_username.delete(0, "end")
                    input_password.delete(0, "end")
                    input_confirmation.delete(0, "end")
            else:
                answer = messagebox.askyesno(title=website_name, message="Do you want to try again?")
                if answer:
                    input_website.delete(0, "end")
                    input_username.delete(0, "end")
                    input_password.delete(0, "end")
                    input_confirmation.delete(0, "end")
                    input_website.focus()
                    input_username.insert(0, "admin@email.com")
                else:
                    messagebox.showinfo(title=website_name, message="Saving the password successfully canceled.")
                    input_website.delete(0, "end")
                    input_username.delete(0, "end")
                    input_password.delete(0, "end")
                    input_confirmation.delete(0, "end")
        elif username == "admin@email.com":
            messagebox.showwarning(title=website_name, message="Please enter a valid username/email.")

        else:
            messagebox.showwarning(title=website_name, message="Please don't leave any fields empty.")
    else:
        messagebox.showwarning(title="Warning", message="Please, confirm the password before adding.")


def find_password():
    entry = input_website.get()
    try:
        with open("data.json", mode="r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found.")
    else:
        for key in data.keys():
            if entry == key:
                messagebox.showinfo(title=entry, message=f"Email: {data[entry]["email"]}"
                                                         f"\nPassword: {data[key]["password"]}")
        if entry not in data:
            messagebox.showinfo(title="Error", message="İt is not founded, please try again.")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=100, pady=100, bg="white")

canvas = Canvas(width=200, height=189, highlightthickness=0, bg="white")
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

label_website = Label(text="Website:", fg="black", bg="white", font=("Arial", 10, "normal"))
label_website.config(padx=5, pady=5)
label_website.grid(column=0, row=1)

input_website = Entry(width=32, highlightthickness=2)
input_website.grid(column=1, row=1, columnspan=1)
input_website.focus()

button_search = Button(text="Search", width=14, bg="white", command=find_password)
button_search.grid(column=2, row=1, columnspan=1)

label_username = Label(text="Email/Username:", fg="black", bg="white", font=("Arial", 10, "normal"))
label_username.config(padx=5, pady=5)
label_username.grid(column=0, row=2)

input_username = Entry(width=51, highlightthickness=2)
input_username.grid(column=1, row=2, columnspan=2)
input_username.insert(0, "admin@email.com")

label_password = Label(text="Password:", fg="black", bg="white", font=("Arial", 10, "normal"))
label_password.config(padx=5, pady=5)
label_password.grid(column=0, row=3)

input_password = Entry(width=32, highlightthickness=2)
input_password.grid(column=1, row=3, columnspan=1)

button_generate = Button(text="Generate Password", width=14, bg="white", command=generate_password)
button_generate.grid(column=2, row=3, columnspan=1)

confirmation_password = Label(text="Confirm password:", fg="black", bg="white", font=("Arial", 10, "normal"))
confirmation_password.config(padx=5, pady=5)
confirmation_password.grid(column=0, row=4)

input_confirmation = Entry(width=32, highlightthickness=2)
input_confirmation.grid(column=1, row=4, columnspan=1)

button_add = Button(text="Add", fg="black", bg="white", font=("Arial", 8, "normal"), width=50,
                    command=save_info)
button_add.grid(column=1, row=5, columnspan=2)

confirmation_button = Button(text="Confirm", font=("Arial", 8, "bold"), fg=GREEN, bg="white",
                             width=14, command=confirm_password)
confirmation_button.grid(column=2, row=4, columnspan=1)


window.mainloop()
