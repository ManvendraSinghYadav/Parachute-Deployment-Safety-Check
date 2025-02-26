# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import math
import csv
from parachute_graphs import create_graphs  # Import the create_graphs function

# Image Path (Update if needed)
logo_path = "D:/isro project image/parachute_background.jpg"

# Initialize Main Window
root = tk.Tk()
root.title("Parachute Deployment System")
root.geometry("1280x800")
root.configure(bg="#f4f4f4")

# Check if the logo exists
if not os.path.exists(logo_path):
    messagebox.showerror("Error", "Logo image not found! Place 'parachute_background.jpg' in 'D:/isro project image'")
    exit()

# Load & Display Logo
logo = Image.open(logo_path)
logo = logo.resize((250, 80), Image.LANCZOS)
logo = ImageTk.PhotoImage(logo)

logo_label = tk.Label(root, image=logo, bg="#f4f4f4")
logo_label.pack(pady=10)

# Create Form Frame (Center aligned)
form_frame = tk.Frame(root, bg="white", padx=20, pady=20, relief="ridge", bd=3)
form_frame.pack(pady=20)

tk.Label(form_frame, text="Enter Parachute Deployment Details", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

# Entry Fields
entries = {}
fields = ["Mass (kg)", "Temperature (°C)", "Altitude (m)", "Velocity (m/s)"]

for field in fields:
    row = tk.Frame(form_frame, bg="white")
    row.pack(pady=5, fill="x")

    tk.Label(row, text=f"{field}:", font=("Arial", 12), bg="white", width=18, anchor="w").pack(side="left", padx=5)
    entry = tk.Entry(row, font=("Arial", 12), width=20)
    entry.pack(side="right", padx=5)
    entries[field] = entry

# Auto-Calculated Fields
calculated_vars = {"Pressure (hPa)": tk.StringVar(), "Humidity (%)": tk.StringVar()}

def calculate_pressure_and_humidity():
    try:
        temperature = float(entries["Temperature (°C)"].get())
        altitude = float(entries["Altitude (m)"].get())

        # Constants for pressure calculation
        P0 = 1013.25  
        L = 0.0065  
        T0 = 288.15  
        g = 9.81  
        M = 0.028964  
        R = 8.314  

        temp_K = temperature + 273.15
        pressure = P0 * (1 - (L * altitude) / T0) ** ((g * M) / (R * L))
        calculated_vars["Pressure (hPa)"].set(f"{pressure:.2f}")

        humidity = 100 * (math.exp((17.625 * temperature) / (243.04 + temperature)) / math.exp((17.625 * (temperature - 5)) / (243.04 + (temperature - 5))))
        calculated_vars["Humidity (%)"].set(f"{humidity:.2f}")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values!")

for field in ["Pressure (hPa)", "Humidity (%)"]:
    row = tk.Frame(form_frame, bg="white")
    row.pack(pady=5, fill="x")
    
    tk.Label(row, text=f"{field}:", font=("Arial", 12), bg="white", width=18, anchor="w").pack(side="left", padx=5)
    label = tk.Label(row, textvariable=calculated_vars[field], font=("Arial", 12, "bold"), bg="white", fg="blue")
    label.pack(side="right", padx=5)

# Descent Rate (Auto-Calculated)
tk.Label(form_frame, text="Descent Rate (m/s):", font=("Arial", 12), bg="white").pack(pady=5)
descent_rate_var = tk.StringVar()
descent_rate_label = tk.Label(form_frame, textvariable=descent_rate_var, font=("Arial", 12, "bold"), bg="white", fg="blue")
descent_rate_label.pack(pady=5)

# Calculate Button
def calculate_descent_rate():
    try:
        # Ensure pressure and humidity are calculated first
        calculate_pressure_and_humidity()

        mass = float(entries["Mass (kg)"].get())
        temperature = float(entries["Temperature (°C)"].get())
        pressure = float(calculated_vars["Pressure (hPa)"].get())

        g = 9.81  # Gravity
        Cd = 1.5  # Drag Coefficient
        A = 3.0   # Parachute Area

        # Air Density Calculation
        rho = pressure * 100 / (287.05 * (temperature + 273.15))
        descent_rate = math.sqrt((2 * mass * g) / (rho * A * Cd))
        descent_rate_var.set(f"{descent_rate:.2f} m/s")

        # Save values to CSV after calculation
        file_path = "D:/isro project image/user_input.csv"
        user_data = {
            "Mass (kg)": entries["Mass (kg)"].get(),
            "Temperature (°C)": entries["Temperature (°C)"].get(),
            "Altitude (m)": entries["Altitude (m)"].get(),
            "Velocity (m/s)": entries["Velocity (m/s)"].get(),
            "Pressure (hPa)": calculated_vars["Pressure (hPa)"].get(),
            "Humidity (%)": calculated_vars["Humidity (%)"].get(),
            "Descent Rate (m/s)": descent_rate_var.get()
        }

        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(user_data.keys())
            writer.writerow(user_data.values())

        messagebox.showinfo("Success", "Descent rate calculated and saved!")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values!")

calc_button = tk.Button(form_frame, text="Calculate Descent Rate", command=calculate_descent_rate,
                        bg="#007acc", fg="white", font=("Arial", 12, "bold"))
calc_button.pack(pady=5)

# **Submit Button - Saves Input & Opens GUI 2**
def record_input():
    calculate_pressure_and_humidity()  
    calculate_descent_rate()  

    # Prepare user data
    user_data = {
        "Mass (kg)": entries["Mass (kg)"].get(),
        "Temperature (°C)": entries["Temperature (°C)"].get(),
        "Altitude (m)": entries["Altitude (m)"].get(),
        "Velocity (m/s)": entries["Velocity (m/s)"].get(),
        "Pressure (hPa)": calculated_vars["Pressure (hPa)"].get(),
        "Humidity (%)": calculated_vars["Humidity (%)"].get(),
        "Descent Rate (m/s)": descent_rate_var.get()
    }

    messagebox.showinfo("Input Recorded", "Data saved. Opening Graphs...")

    # Call the create_graphs function directly
    create_graphs(user_data)

submit_button = tk.Button(form_frame, text="Check Deployment", command=record_input,
                          bg="#00cc66", fg="white", font=("Arial", 12, "bold"))
submit_button.pack(pady=10)

# Run the App
root.mainloop()
