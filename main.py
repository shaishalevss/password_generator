from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols

    shuffle(password_list)

    password = "".join(password_list)
    pass_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    user_website = website_entry.get()
    user_email = email_user_entry.get()
    user_password = pass_entry.get()

    new_data = {user_website: {
        "email": user_email,
        "password": user_password
        }
    }

    if len(user_website) == 0 or len(user_email) == 0 or len(user_password) == 0:
        messagebox.showinfo(title="Oops!", message="Please verify you didn't leave any field empty.")
    else:
        is_ok = messagebox.askokcancel(title=user_website, message=f"These are the details entered:\nEmail: {user_email}\nPassword: {user_password}\nIs it ok to save?")

        if is_ok:
            try:
                with open("data.json", mode="r") as f:
                    # Read old data from JSON
                    data = json.load(f)

            except FileNotFoundError:
                with open("data.json", "w") as f:
                    # Saving updated data
                    json.dump(new_data, f, indent=4)
            else:
                # Update old data with the new data
                data.update(new_data)
                f = open("data.json", "w")
                # Saving updated data
                json.dump(new_data, f, indent=4)

            finally:
                website_entry.delete(0, END)
                pass_entry.delete(0, END)

# ---------------------------- Search for a Password ------------------------------- #


def find_password():
    website = website_entry.get()

    try:
        with open("data.json", mode="r") as f:
            # Read old data from JSON
            data = json.load(f)

    except FileNotFoundError:
        print("Website not found due to file not exists.")

    else:
        if website in data:
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=f"Your details for {website} are:", message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for{website} were found.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()

window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(window, width=200, height=200)
image = PhotoImage(file="logo-gif.gif")
canvas.create_image(100, 100, image=image)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
email_user_label = Label(text="Email/Username:")
pass_label = Label(text="Password:")

website_label.grid(row=1, column=0)
email_user_label.grid(row=2, column=0)
pass_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=28)
website_entry.focus()
email_user_entry = Entry(width=46)
email_user_entry.insert(0, "@gmail.com ")
pass_entry = Entry(width=28)

website_entry.grid(row=1, column=1)
email_user_entry.grid(row=2, column=1, columnspan=2)
pass_entry.grid(row=3, column=1)

# Buttons
generate_pass_button = Button(text="Generate Password", highlightbackground='#3E4149', width=14, command=generate_password)
add_button = Button(text="Add", width=43, highlightbackground='#3E4149', command=save_password)
search_button = Button(text="Search", highlightbackground='#3E4149', width=14, command=find_password)

generate_pass_button.grid(row=3, column=2)
add_button.grid(row=4, column=1, columnspan=2)
search_button.grid(row=1, column=2)




window.mainloop()
