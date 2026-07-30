import json
import time
from PIL import Image
import customtkinter as ctk
ctk.set_widget_scaling(1)
ctk.set_window_scaling(1)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
default_data = {
    "is_logged_in": False,
    "is_account_created": False,
    "username": "",
    "password": "",
    "money": 0.0,
    "history": [],
    "currencies": ["PLN", "EUR", "USD", "GBP"]
}
app = ctk.CTk()
app.wm_title("ATM")
app.geometry("1920x1080")
frame = None
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)
def save_data():
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)
def clear_window():
    global frame
    if frame is not None:
        frame.destroy()
        frame = None

try:
    with open('data.json', 'r') as file:
        data = json.load(file)
        if not data:
            data = default_data
            save_data()
except (FileNotFoundError, json.JSONDecodeError):
    data = default_data
    save_data()
is_logged_in = data["is_logged_in"]
is_account_created = data["is_account_created"]
username = data["username"]
password = data["password"]
money = data["money"]
history = data["history"]
time = time.strftime("%H:%M")
currencies = data["currencies"]
settings_icon = ctk.CTkImage(
    dark_image=Image.open("settings_icon.png"),
    light_image=Image.open("settings_icon.png"),
    size=(70, 70)
)
currency = ctk.StringVar(value="PLN")
def login():
    global frame
    global login_username_entry
    global login_password_entry
    global login_error_label
    clear_window()
    frame = ctk.CTkFrame(app, corner_radius=60, width=600, height=750)
    login_title = ctk.CTkLabel(frame, text="ATM Login", font=("Cambria", 64, "bold"))
    login_username_entry = ctk.CTkEntry(frame, width=500, height=120, placeholder_text="Username", font=("Comfortaa", 34, "bold"), corner_radius=30, fg_color="#0f1b85", border_width=1, justify="center", border_color="black" )
    login_password_entry = ctk.CTkEntry(frame, width=500, height=120, placeholder_text="Password", font=("Comfortaa", 34, "bold"), corner_radius=30, fg_color="#0f1b85", border_width=1, justify="center", border_color="black")
    login_error_label = ctk.CTkLabel(frame, font=("Comfortaa", 30), text_color="red", wraplength=380)
    login_button_entry = ctk.CTkButton(frame, width=500, height=80, text="Log in", command=login_button_command, font=("Comfortaa", 34, "bold"), corner_radius=30, fg_color="#0f1b85", hover_color="green", )
    frame.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )
    frame.grid_propagate(False)
    frame.grid_columnconfigure(0, weight=1)
    login_title.grid(row=0, column=0, pady=100)
    login_password_entry.grid(row=2, column=0, pady=20)
    login_username_entry.grid(row=1, column=0, pady=0)
    login_button_entry.grid(row=4, column=0, pady=25)
def login_button_command():
    if login_username_entry.get() != data["username"].strip():
        login_error_label.grid(row=3, column=0, pady=0)
        login_error_label.configure(text=f'Account "{login_username_entry.get()}" not found"')
    else:
        if login_password_entry.get() != data["password"].strip():
            login_error_label.grid(row=3, column=0, pady=0)
            login_error_label.configure(text=f'Wrong password')
        else:
            data["is_logged_in"] = False
            save_data()
            atm()
            return username, password
def deposit_window():
    global frame
    global deposit_money
    global deposit_error_label
    global final_deposit_button
    clear_window()
    frame = ctk.CTkFrame(app, corner_radius=60, width=600, height=400, fg_color="#0f1b85")
    frame.grid_propagate(False)
    frame.grid_columnconfigure(0, weight=1)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    final_deposit_button = ctk.CTkButton(frame, text="Deposit", command=deposit, width=500, height=80, font=("Comfortaa", 34, "bold"), corner_radius=30, fg_color="#fff", text_color="#0f1b85", hover_color="green")
    deposit_money = ctk.CTkEntry(frame, placeholder_text="Money to deposit", placeholder_text_color="#0f1b85", fg_color="white", width=500, height=120, corner_radius=30, border_width=1, font=("Comfortaa", 36, "bold"), text_color="#0f1b85", justify="center", border_color="black")
    deposit_error_label = ctk.CTkLabel(frame, font=("Comfortaa", 30), text_color="red", wraplength=380)
    deposit_money.grid(row=0, column=0, pady=70)
    final_deposit_button.grid(row=2, column=0, pady=0)
def withdraw_window():
    global frame
    global withdraw_money
    global withdraw_error_label
    global final_withdraw_button
    clear_window()
    frame = ctk.CTkFrame(app, corner_radius=60, width=600, height=400, fg_color="#07108c")
    frame.grid_propagate(False)
    frame.grid_columnconfigure(0, weight=1)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    final_withdraw_button = ctk.CTkButton(frame, text="Withdraw", command=withdraw, width=500, height=80, font=("Comfortaa", 34, "bold"), corner_radius=30, fg_color="#fff", text_color="#0f1b85", hover_color="green")
    withdraw_money = ctk.CTkEntry(frame, placeholder_text="Money to withdraw", placeholder_text_color="#0f1b85", fg_color="white", width=500, height=120, corner_radius=30, border_width=1, font=("Comfortaa", 36, "bold"), text_color="#0f1b85", justify="center", border_color="black")
    withdraw_error_label = ctk.CTkLabel(frame, font=("Comfortaa", 30), text_color="red", wraplength=380)
    withdraw_money.grid(row=0, column=0, pady=70)
    final_withdraw_button.grid(row=2, column=0, pady=0)
def withdraw():
    withdraw_money_value = withdraw_money.get()
    try:
        if withdraw_money_value is float or int:
            withdraw_money_value = float(withdraw_money_value)
            withdraw_money.grid(row=0, column=0, pady=30)
            final_withdraw_button.grid(row=2, column=0, pady=45)
            withdraw_error_label.grid(row=1, column=0, pady=0)
            if withdraw_money_value > 0:
                data["money"] -= withdraw_money_value
                save_data()
                data["history"].append({
                    "time": time,
                    "money": withdraw_money_value,
                    "action": "Withdraw"
                })

                withdraw_error_label.configure(text=(f"{withdraw_money_value}zł has been withdraw"), text_color="#0dff00")
                app.after(2000, atm)
            else:
                withdraw_error_label.configure(text=("The amount of withdraw money must be positive"), text_color="red")
    except ValueError:
        withdraw_money.grid(row=0, column=0, pady=30)
        final_withdraw_button.grid(row=2, column=0, pady=45)
        withdraw_error_label.grid(row=1, column=0, pady=0)
        withdraw_error_label.configure(text="You have to enter a digit", text_color="red")
def deposit():
    deposit_money_value = deposit_money.get()
    try:
        if deposit_money_value is float or int:
            deposit_money_value = float(deposit_money_value)
            deposit_money.grid(row=0, column=0, pady=30)
            final_deposit_button.grid(row=2, column=0, pady=45)
            deposit_error_label.grid(row=1, column=0, pady=0)
            if deposit_money_value > 0:
                data["money"] += deposit_money_value
                data["history"].append({
                    "time": time,
                    "money": deposit_money_value,
                    "action": "Deposit"
                })
                save_data()

                deposit_error_label.configure(text=(f"{deposit_money_value}zł has been deposited"), text_color="#0dff00")
                app.after(2000, atm)
            else:
                deposit_error_label.configure(text=("The amount of deposit money must be positive"), text_color="red")

    except ValueError:
        deposit_money.grid(row=0, column=0, pady=30)
        final_deposit_button.grid(row=2, column=0, pady=45)
        deposit_error_label.grid(row=1, column=0, pady=0)
        deposit_error_label.configure(text="You have to enter a digit", text_color="red")

def atm():
    global frame
    global settings_button
    global history_box
    clear_window()
    frame = ctk.CTkFrame(app, corner_radius=60, width=800, height=1000)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    settings_button = ctk.CTkButton(app, text="", image=settings_icon, width=90, height=90, fg_color="transparent", corner_radius=45, command=settings, hover=False)
    user_welcomer = ctk.CTkLabel(frame, text=f'Welcome {data["username"]}', font=("Comfortaa", 64, "bold"))
    money_label = ctk.CTkLabel(frame, text=f'{data["money"]}zł', font=("Comfortaa", 64, "bold"))
    deposit_button = ctk.CTkButton(frame, text="Deposit", command=deposit_window, width=500, height=80, font=("Comfortaa", 34, "bold"), corner_radius=30, fg_color="#0f1b85", text_color="#fff", hover_color="green")
    withdraw_button = ctk.CTkButton(frame, text="Withdraw", command=withdraw_window, width=500, height=80, font=("Comfortaa", 34, "bold"), corner_radius=30, fg_color="#0f1b85", text_color="#fff", hover_color="red")
    history_box = ctk.CTkScrollableFrame(frame, width=450, height=400, fg_color="#0f1b85", corner_radius=30)
    for i, transaction in enumerate(data["history"]):
        transaction_frame = ctk.CTkFrame(history_box, width=425, height=100, fg_color="white", corner_radius=30)
        transaction_label = ctk.CTkLabel(transaction_frame, text=f"Time: {transaction['time']} Money: {transaction['money']} Action: {transaction['action']}", font=("Comfortaa", 21, "bold"), text_color="#0f1b85")
        transaction_label.grid(row=0, column=0)
        transaction_frame.grid(row=i, column=0, pady=10, padx=(5, 0))
        transaction_frame.grid_columnconfigure(0, weight=1)
        transaction_frame.grid_rowconfigure(0, weight=1)
        transaction_frame.grid_propagate(False)
    frame.grid_propagate(False)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=0)
    settings_button.grid(row=0, column=1, padx=(0, 20), pady=(20, 0), sticky="ne")
    user_welcomer.grid(row=0, column=0, pady=(40, 0))
    money_label.grid(row=1, column=0, pady=(50, 0))
    deposit_button.grid(row=2, column=0, pady=(80, 0))
    withdraw_button.grid(row=3, column=0, pady=(10, 10))
    history_box.grid(row=4, column=0, pady=(50, 0))
    if data["money"] < 0:

        money_label.configure(text_color="red")
    else:
        money_label.configure(text_color="white")

def settings():
    global frame
    global username_change_entry
    settings_button.destroy()
    clear_window()
    frame = ctk.CTkFrame(app, corner_radius=60, width=1600, height=1000)
    save_change = ctk.CTkButton(frame, corner_radius=30, width=450, height=75, fg_color="#0f1b85", font=("Comfortaa", 34, "bold"), text="Save changes", hover_color="green", text_color="white", command=save_changes)
    account_details_label = ctk.CTkLabel(frame, text_color="white", font=("Comfortaa", 34, "bold"), text="Account Details")
    preferences_label = ctk.CTkLabel(frame, text_color="white", font=("Comfortaa", 34, "bold"), text="Preferences")
    username_change_frame = ctk.CTkFrame(frame, corner_radius=30, width=650, height=100, border_width=1, border_color="grey")
    username_change_entry = ctk.CTkEntry(username_change_frame, corner_radius=30, width=300, height=70, placeholder_text="", fg_color="white", placeholder_text_color="#0f1b85", font=("Comfortaa", 36, "bold"), justify="center", text_color="#0f1b85", textvariable=ctk.StringVar(value=data["username"]))
    username_change_label = ctk.CTkLabel(username_change_frame, text="Your username:", text_color="white",font=("Comfortaa", 36, "bold"), justify="center")
    currency_change_frame = ctk.CTkFrame(frame, corner_radius=30, width=650, height=100, border_width=1, border_color="grey")
    currency_change_label = ctk.CTkLabel(currency_change_frame, text="Currency:", text_color="white", font=("Comfortaa", 36, "bold"))
    currency_change_option = ctk.CTkOptionMenu(currency_change_frame, variable=currency, values=(data["currencies"]), fg_color="white", dropdown_fg_color="#0f1b85", button_color="white", corner_radius=30, text_color="#0f1b85", button_hover_color="green", font=("Comfortaa", 36, "bold"), width=300, height=68, bg_color="transparent", dropdown_text_color="white", dropdown_font=("Comfortaa", 26, "bold"), dropdown_hover_color="green")

    username_change_frame.grid(row=1, column=0, pady=(0,60), padx=(0, 800))
    username_change_frame.grid_propagate(False)
    username_change_label.grid(row=0, column=0,  padx=(30,0), pady=(16, 0))
    username_change_entry.grid(row=0, column=1, padx=(20,0), pady=(16, 0))

    currency_change_frame.grid(row=1, column=0, pady=(160,0), padx=(0, 800))
    currency_change_frame.grid_propagate(False)
    currency_change_option.grid(row=0, column=1, pady=(16, 0), padx=(120,0))
    currency_change_label.grid(row=0, column=0, pady=(16, 0), padx=(30, 0))
    account_details_label.grid(row=0, column=0, pady=(60, 0), padx=(0, 770))
    save_change.grid(row=2, column=0, pady=(450, 0))
    preferences_label.grid(row=0, column=0, pady=(50, 0), padx=(810, 0))
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=0)
    frame.grid_propagate(False)
    frame.place(relx=0.5, rely=0.5, anchor="center")

def save_changes():
    if username_change_entry.get() != data["username"]:
        print("lol")
        data["username"] = username_change_entry.get()
        save_data()
def registriaton():
    global frame
    global registriation_username_entry
    global registriation_password_entry
    global registriation_error_label
    frame = ctk.CTkFrame(app, corner_radius=60, width=600, height=750)
    registriation_title = ctk.CTkLabel(frame, text="ATM Registriaton", font=("Cambria", 64, "bold"))
    registriation_username_entry = ctk.CTkEntry(frame, width=500, height=120, placeholder_text="Username", font=("Comfortaa", 34, "bold"), corner_radius=30, fg_color="#0f1b85", border_width=1, justify="center", border_color="black" )
    registriation_password_entry = ctk.CTkEntry(frame, width=500, height=120, placeholder_text="Password", font=("Comfortaa", 34, "bold"), corner_radius=30, fg_color="#0f1b85", border_width=1, justify="center", border_color="black")
    registriation_error_label = ctk.CTkLabel(frame, font=("Comfortaa", 30), text_color="red", wraplength=380)
    registriation_button_entry = ctk.CTkButton(frame, width=500, height=80, text="Sign up", command=register_button_command, font=("Comfortaa", 34, "bold"), corner_radius=30, fg_color="#0f1b85", hover_color="green", )
    frame.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )
    frame.grid_propagate(False)
    frame.grid_columnconfigure(0, weight=1)
    registriation_title.grid(row=0, column=0, pady=100)
    registriation_password_entry.grid(row=2, column=0, pady=20)
    registriation_username_entry.grid(row=1, column=0, pady=0)
    registriation_button_entry.grid(row=4, column=0, pady=25)
def register_button_command():
    if registriation_username_entry.get() == "".strip() and registriation_password_entry.get() == "".strip():
        registriation_error_label.configure(text = "Please enter your username and password")
        registriation_error_label.grid(row=3, column=0, pady=0)
    elif registriation_password_entry.get() =="".strip():
        registriation_error_label.configure(text = "Please enter your password")
        registriation_error_label.grid(row=3, column=0, pady=0)
    elif registriation_username_entry.get() =="".strip():
        registriation_error_label.configure(text = "Please enter your username")
        registriation_error_label.grid(row=3, column=0, pady=0)
    elif registriation_password_entry.get() == data["password"].strip() and registriation_username_entry.get() == data["username"].strip():
        registriation_error_label.configure(text = "Account already exists")
    else:
        if registriation_password_entry.get() == data["password"].strip() and registriation_username_entry.get() == data["username"].strip():
            registriation_error_label.configure(text="Account already exists")
        data["username"] = registriation_username_entry.get()
        data["password"] = registriation_password_entry.get()
        data["is_account_created"] = True
        save_data()
        atm()
        return username, password

if is_account_created:
    if is_logged_in:
        atm()
    else:
        login()
else:
    registriaton()

app.mainloop()