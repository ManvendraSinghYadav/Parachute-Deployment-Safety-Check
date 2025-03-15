# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import math
import csv
from parachute_graphs import create_graphs  # Import the create_graphs function

# Image Path (Update if needed)
logo_path = "D:/isro project image/parachute_background.jpg"
background_image_path = "D:/isro project image/pro img.jpg"  # Background image path

# Initialize Main Window
root = tk.Tk()
root.title("Parachute Deployment System")
root.geometry("1400x900")  # Wider window
root.configure(bg="#f0f0f0")

# Check if the background image exists
if not os.path.exists(background_image_path):
    messagebox.showerror("Error", f"Background image not found at: {background_image_path}")
    exit()

# Load Background Image
try:
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((1600, 900), Image.LANCZOS)  # Resize to fit window
    background_photo = ImageTk.PhotoImage(background_image)
except Exception as e:
    messagebox.showerror("Error", f"Failed to load background image: {e}")
    exit()

# Create a Canvas to set the background image
canvas = tk.Canvas(root, width=1600, height=900)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

# Check if the logo exists
if not os.path.exists(logo_path):
    messagebox.showerror("Error", f"Logo image not found at: {logo_path}")
    exit()

# Load & Display Logo
try:
    logo = Image.open(logo_path)
    logo = logo.resize((190, 150), Image.LANCZOS)
    logo = ImageTk.PhotoImage(logo)
except Exception as e:
    messagebox.showerror("Error", f"Failed to load logo image: {e}")
    exit()

logo_label = tk.Label(root, image=logo, bg="#f0f0f0")
logo_label.place(x=20, y=20)  # Position the logo

# Create Main Form Frame
form_frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief="ridge", bd=3)
form_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the form frame

# Title
tk.Label(form_frame, text="Enter Parachute Deployment Details", font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=10)

# Left Frame for User Input
left_frame = tk.LabelFrame(form_frame, text="Input Fields", bg="#ffffff", padx=10, pady=10, font=("Arial", 12, "bold"))
left_frame.pack(side="left", padx=20, pady=10, fill="y")

# Right Frame for Calculated Values
right_frame = tk.LabelFrame(form_frame, text="Calculated Values", bg="#ffffff", padx=10, pady=10, font=("Arial", 12, "bold"))
right_frame.pack(side="right", padx=20, pady=10, fill="both", expand=True)  # Make it wider and expandable

# Entry Fields (Left Side)
entries = {}
fields = [
    "Mass (kg)", "Temperature (°C)", "Altitude (m)", "Velocity (m/s)", 
    "Parachute Area (m²)"
]

for field in fields:
    row = tk.Frame(left_frame, bg="#ffffff")
    row.pack(pady=5, fill="x")

    tk.Label(row, text=f"{field}:", font=("Arial", 12), bg="#ffffff", width=18, anchor="w").pack(side="left", padx=5)
    entry = tk.Entry(row, font=("Arial", 12), width=20)
    entry.pack(side="right", padx=5)
    entries[field] = entry

# Dropdown for Parachute Shape (Left Side)
tk.Label(left_frame, text="Parachute Shape:", font=("Arial", 12), bg="#ffffff").pack(pady=5)
parachute_shape_var = tk.StringVar()
parachute_shape_dropdown = ttk.Combobox(left_frame, textvariable=parachute_shape_var, font=("Arial", 12), width=18)
parachute_shape_dropdown['values'] = ("Round", "Square", "Elliptical")
parachute_shape_dropdown.current(0)  # Default to Round
parachute_shape_dropdown.pack(pady=5)

# Auto-Calculated Fields (Right Side)
calculated_vars = {
    "Pressure (hPa)": tk.StringVar(),
    "Humidity (%)": tk.StringVar(),
    "Wind Speed (m/s)": tk.StringVar(),
    "Descent Rate (m/s)": tk.StringVar(),
    "Glide Ratio": tk.StringVar(),
    "Impact Force (N)": tk.StringVar(),
    "Horizontal Displacement (m)": tk.StringVar(),
    "Body Position": tk.StringVar()
}

for field, var in calculated_vars.items():
    row = tk.Frame(right_frame, bg="#ffffff")
    row.pack(pady=5, fill="x")

    # Label with fixed width for alignment
    tk.Label(row, text=f"{field}:", font=("Arial", 12), bg="#ffffff", width=25, anchor="w").pack(side="left", padx=5)
    
    # Value with fixed width for alignment
    label = tk.Label(row, textvariable=var, font=("Arial", 12, "bold"), bg="#ffffff", fg="#007acc", width=15, anchor="e")
    label.pack(side="right", padx=5)

# Function to Calculate Pressure and Humidity
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
        messagebox.showerror("Error", "Please enter valid numeric values for Temperature and Altitude!")

# Function to Calculate Descent Rate and Horizontal Displacement
def calculate_descent_rate():
    try:
        # Ensure pressure and humidity are calculated first
        calculate_pressure_and_humidity()

        # Get user inputs
        mass = float(entries["Mass (kg)"].get())
        temperature = float(entries["Temperature (°C)"].get())
        altitude = float(entries["Altitude (m)"].get())
        parachute_area = float(entries["Parachute Area (m²)"].get())
        parachute_shape = parachute_shape_var.get()

        # Air Density Calculation
        pressure = float(calculated_vars["Pressure (hPa)"].get())
        rho = pressure * 100 / (287.05 * (temperature + 273.15))

        # Drag Coefficient based on Parachute Shape
        if parachute_shape == "Round":
            Cd = 1.5
        elif parachute_shape == "Square":
            Cd = 1.2
        elif parachute_shape == "Elliptical":
            Cd = 1.0

        # Descent Rate Calculation
        g = 9.81
        descent_rate = math.sqrt((2 * mass * g) / (rho * parachute_area * Cd))
        calculated_vars["Descent Rate (m/s)"].set(f"{descent_rate:.2f}")

        # Time of Descent
        t = altitude / descent_rate

        # Estimate Wind Speed (if not provided)
        # Use a realistic wind speed range (3–8 m/s)
        V_wind = 5.0  # Default wind speed
        calculated_vars["Wind Speed (m/s)"].set(f"{V_wind:.2f}")

        # Calculate Horizontal Displacement using Glide Ratio
        glide_ratio = 0.7  # Realistic glide ratio for parachutes
        d = glide_ratio * altitude
        calculated_vars["Horizontal Displacement (m)"].set(f"{d:.2f}")

        # Update Glide Ratio
        calculated_vars["Glide Ratio"].set(f"{glide_ratio:.2f}")

        # Impact Force Calculation
        impact_force = mass * g  # Simplified calculation
        calculated_vars["Impact Force (N)"].set(f"{impact_force:.2f}")

        # Suggest Body Position
        if descent_rate > 10:  # High descent rate
            calculated_vars["Body Position"].set("Head Down")
        elif glide_ratio < 1:  # Low glide ratio
            calculated_vars["Body Position"].set("Sitting")
        else:  # Moderate conditions
            calculated_vars["Body Position"].set("Spread Eagle")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values!")

# Calculate Descent Rate Button (Center)
calc_button = tk.Button(form_frame, text="Calculate Descent Rate", command=calculate_descent_rate,
                        bg="#007acc", fg="white", font=("Arial", 12, "bold"))
calc_button.pack(pady=20)

# Check Deployment Button (Bottom)
def record_input():
    calculate_descent_rate()
    user_data = {
        "Mass (kg)": entries["Mass (kg)"].get(),
        "Temperature (°C)": entries["Temperature (°C)"].get(),
        "Altitude (m)": entries["Altitude (m)"].get(),
        "Velocity (m/s)": entries["Velocity (m/s)"].get(),
        "Parachute Area (m²)": entries["Parachute Area (m²)"].get(),
        "Parachute Shape": parachute_shape_var.get(),
        "Body Position": calculated_vars["Body Position"].get(),
        "Pressure (hPa)": calculated_vars["Pressure (hPa)"].get(),
        "Humidity (%)": calculated_vars["Humidity (%)"].get(),
        "Wind Speed (m/s)": calculated_vars["Wind Speed (m/s)"].get(),
        "Descent Rate (m/s)": calculated_vars["Descent Rate (m/s)"].get(),
        "Glide Ratio": calculated_vars["Glide Ratio"].get(),
        "Impact Force (N)": calculated_vars["Impact Force (N)"].get(),
        "Horizontal Displacement (m)": calculated_vars["Horizontal Displacement (m)"].get()
    }

    messagebox.showinfo("Input Recorded", "Data saved. Opening Graphs...")
    create_graphs(user_data)

submit_button = tk.Button(form_frame, text="Check Deployment", command=record_input,
                          bg="#00cc66", fg="white", font=("Arial", 12, "bold"))
submit_button.pack(pady=10)

# Run the App
root.mainloop()
