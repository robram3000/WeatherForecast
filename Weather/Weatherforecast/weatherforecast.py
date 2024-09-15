import customtkinter
from PIL import  Image
import requests
from datetime import datetime, timedelta
import threading
import time
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import atexit

API_KEY = 'b8994153586d2af0101ab7b11d462cfb'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
DATA_FILE = 'weather_data.json'
tree = None
stop_thread = False

def fetch_weather_data(location):
    params = {
        'q': location,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        country_city = f"{data['name']}, {data['sys']['country']}"
        temperature = f"{data['main']['temp']}°C"
        humidity = f"{data['main']['humidity']}%"
        speed = f"{data['wind']['speed']} m/s"
        status = data['weather'][0]['description'].capitalize()

        timezone_offset = data['timezone']
        local_time = datetime.utcnow() + timedelta(seconds=timezone_offset)
        date = local_time.strftime("%Y-%m-%d")
        local_time_str = local_time.strftime("%H:%M:%S")

        weather_record = {
            "location": country_city,
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": speed,
            "status": status,
            "date": date,
            "time": local_time_str
        }

        save_weather_data(weather_record)
        return (country_city, temperature, humidity, speed, status, date, local_time_str)
    else:
        return None

def save_weather_data(weather_record):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
    else:
        data = []
    data.append(weather_record)
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def display_weather_data(weather_data):
  
    if weather_data:
        country_label.configure(text=weather_data[0])
        temperature_label.configure(text=weather_data[1])
        humidity_label.configure(text=weather_data[2])
        windandspeed_label.configure(text=weather_data[3])
        status_label.configure(text=weather_data[4])
        localtimeanddate_label.configure(text=f"{weather_data[5]} {weather_data[6]}")
        update_graph()
        update_tree_view(weather_data)
  

def update_graph():
    ax.clear()
    ax.plot(time_data, temp_data, color='green')
    ax.tick_params(axis='both', which='major', labelsize=10)
    for i in range(len(time_data)):
        ax.text(time_data[i], temp_data[i], f'{temp_data[i]}°C', fontsize=8, ha='center', va='bottom')
    fig.autofmt_xdate()
    ax.grid(True, color='gray', linestyle='dotted', alpha=0.5)
    canvas.draw()

def fetch_and_update_data():
    global stop_thread
    while not stop_thread:
        location = input_data.get()
        app.after(10, fetch_weather_data_and_display, location) 
        time.sleep(10)

def fetch_weather_data_and_display(location):
    weather_data = fetch_weather_data(location)
    if weather_data and tree:  
        time_data.append(datetime.now().strftime('%H:%M:%S'))
        temp_data.append(float(weather_data[1].replace('°C', '')))
        if len(time_data) > 10:
            time_data.pop(0)
            temp_data.pop(0)
        display_weather_data(weather_data)
        update_tree_view(weather_data)


def update_tree_view(weather_data):
    global tree
    if tree:
        tree.insert("", "end", values=(
            weather_data[0], weather_data[1], weather_data[2],
            weather_data[3], weather_data[4], weather_data[5],
            weather_data[6]
        ))

def show_table_view():
    global table_app, tree 
    table_app = customtkinter.CTk()
    table_app.geometry("800x600")
    table_app.title("Weather Data Table")


    paned_window = ttk.Panedwindow(table_app, orient="horizontal")
    paned_window.pack(expand=True, fill="both")

    column_widths = (150, 100, 100, 100, 150, 100, 100)
    columns = ('Location', 'Temperature', 'Humidity', 'Wind Speed', 'Status', 'Date', 'Time')
    

    tree = ttk.Treeview(master=paned_window, columns=columns, show='headings')
    for col, width in zip(columns, column_widths):
        tree.heading(col, text=col)
        tree.column(col, width=width, stretch=tk.YES)
    paned_window.add(tree)


    load_data(tree)  


    retrieve_button = customtkinter.CTkButton(master=table_app, text="Retrieve Selected Data", fg_color="#7A7A78", width=150, height=35, command=retrieve_selected_data, bg_color="#BBB5B5")
    retrieve_button.pack()

    table_app.protocol("WM_DELETE_WINDOW", on_closing)
    table_app.mainloop()

def retrieve_selected_data():
    global tree
    selected_item = tree.focus()
    if selected_item:
        values = tree.item(selected_item, 'values')
       
        display_weather_data(values)


def on_closing():
    global table_app, tree
    if table_app:
        table_app.destroy()
        table_app = None 
    if tree:
        tree = None  

def load_data(tree):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            for record in data:
                tree.insert("", "end", values=(
                    record["location"], record["temperature"], record["humidity"],
                    record["wind_speed"], record["status"], record["date"], record["time"]
                ))


customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width // 2) - (946 // 2)
y = (screen_height // 2) - (739 // 2)
app.geometry(f"{946}x{739}+{x}+{y}")
app.title("Weather Forecast")
app.resizable(False, False)
app.attributes("-fullscreen", False)

image_path = "Weather/Weatherforecast/Framev1.jpg"
pil_image = Image.open(image_path)
ctk_image = customtkinter.CTkImage(pil_image, size=(946, 739))
main_frame = customtkinter.CTkFrame(master=app, width=946, height=739)
main_frame.place(x=0, y=0)

li = customtkinter.CTkLabel(master=main_frame, image=ctk_image, text="", width=946, height=739)
li.pack(anchor="center")

input_data = customtkinter.CTkEntry(master=li, placeholder_text="Enter location", width=300, height=35, border_color="silver", fg_color="white", text_color="#9B9797", bg_color="#BBB5B5")
input_data.place(x=300, y=5)
button_data = customtkinter.CTkButton(master=li, text="Submit", fg_color="#7A7A78", width=80, height=35, command=lambda: display_weather_data(fetch_weather_data(input_data.get())), bg_color="#BBB5B5")
button_data.place(x=600, y=5)

view_button = customtkinter.CTkButton(master=li, text="View", fg_color="#7A7A78", width=80, height=35, command=show_table_view, bg_color="#BBB5B5")
view_button.place(x=835, y=5)

country_label = customtkinter.CTkLabel(master=li, text_color="White", text="", font=("arial", 20), fg_color="Black", bg_color="Black")
country_label.place(x=170, y=85)
localtimeanddate_label = customtkinter.CTkLabel(master=li, text_color="White", text="", font=("arial", 20), fg_color="Black", bg_color="Black")
localtimeanddate_label.place(x=610, y=85)

temperature_label = customtkinter.CTkLabel(master=li, text_color="#414141", text="", font=("arial", 25), fg_color="white", bg_color="white")
temperature_label.place(x=120, y=270)

humidity_label = customtkinter.CTkLabel(master=li, text_color="#414141", text="", font=("arial", 25), fg_color="white", bg_color="white")
humidity_label.place(x=380, y=270)

windandspeed_label = customtkinter.CTkLabel(master=li, text_color="#414141", text="", font=("arial", 25), fg_color="white", bg_color="white")
windandspeed_label.place(x=560, y=270)

status_label = customtkinter.CTkLabel(master=li, text_color="#414141", text="", font=("arial", 20), fg_color="white", bg_color="white")
status_label.place(x=760, y=275)

graph_frame = customtkinter.CTkFrame(master=li, fg_color="#4f4f4d", width=620, height=400, bg_color="transparent")
graph_frame.place(relx=0.5, rely=0.72, anchor="center")

fig, ax = plt.subplots(figsize=(7, 3))
fig.patch.set_alpha(0)
ax.set_facecolor('#FFFFFF')
fig.set_facecolor('#FFFFFF')
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack()

time_data = []
temp_data = []

thread = threading.Thread(target=fetch_and_update_data)
thread.daemon = True
thread.start()

atexit.register(lambda: setattr(stop_thread, True))
main_frame.tkraise()  
app.mainloop()

