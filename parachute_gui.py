import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import math

# Image Path (Updated)
logo_path = "D:/isro project image/parachute_background.jpg"

# Initialize Main Window
root = tk.Tk()
root.title("Parachute Deployment System")
root.geometry("1280x800")
root.configure(bg="#f4f4f4")  # Light background for a clean look

# Check if the logo exists
if not os.path.exists(logo_path):
    messagebox.showerror("Error", "Logo image not found! Place 'parachute_background.jpg' in 'D:/isro project image'")
    exit()

# Load & Display Logo
logo = Image.open(logo_path)
logo = logo.resize((250, 80), Image.LANCZOS)  # Resize for better fit
logo = ImageTk.PhotoImage(logo)

logo_label = tk.Label(root, image=logo, bg="#f4f4f4")
logo_label.pack(pady=10)  # Adds some space below the logo

# Create Form Frame (Center aligned)
form_frame = tk.Frame(root, bg="white", padx=20, pady=20, relief="ridge", bd=3)
form_frame.pack(pady=20)

tk.Label(form_frame, text="Enter Parachute Deployment Details", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

# Entry Fields
entries = {}
fields = [
    "Mass (kg)",
    "Temperature (°C)",
    "Altitude (m)",
    "Velocity (m/s)"
]

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
        P0 = 1013.25  # Standard pressure at sea level in hPa
        L = 0.0065  # Temperature lapse rate (K/m)
        T0 = 288.15  # Standard temperature at sea level (K)
        g = 9.81  # Gravity (m/s²)
        M = 0.028964  # Molar mass of Earth's air (kg/mol)
        R = 8.314  # Universal gas constant (J/(mol·K))

        # Convert temperature to Kelvin
        temp_K = temperature + 273.15

        # Calculate Pressure (hPa)
        pressure = P0 * (1 - (L * altitude) / T0) ** ((g * M) / (R * L))
        calculated_vars["Pressure (hPa)"].set(f"{pressure:.2f}")
        
        # Calculate Humidity Approximation (Relative Humidity %)
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
        mass = float(entries["Mass (kg)"].get())
        temperature = float(entries["Temperature (°C)"].get())
        pressure = float(calculated_vars["Pressure (hPa)"].get())
        
        # Constants
        g = 9.81  # Gravity (m/s²)
        Cd = 1.5  # Drag Coefficient (Parachute)
        A = 3.0  # Approximate parachute area (m²)

        # Air Density Calculation
        rho = pressure * 100 / (287.05 * (temperature + 273.15))  

        # Descent Rate Formula
        descent_rate = math.sqrt((2 * mass * g) / (rho * A * Cd))
        descent_rate_var.set(f"{descent_rate:.2f} m/s")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values!")

calc_button = tk.Button(form_frame, text="Calculate Descent Rate", command=calculate_descent_rate,
                        bg="#007acc", fg="white", font=("Arial", 12, "bold"))
calc_button.pack(pady=5)

# Submit Button
def record_input():
    calculate_pressure_and_humidity()  # Ensure pressure & humidity are updated
    messagebox.showinfo("Input Recorded", "Your input has been recorded.\nChecking parachute deployment...")

submit_button = tk.Button(form_frame, text="Check Deployment", command=record_input,
                          bg="#00cc66", fg="white", font=("Arial", 12, "bold"))
submit_button.pack(pady=10)

# Run the App
root.mainloop()
