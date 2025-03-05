# run_graph_gui.py

import tkinter as tk
from tkinter import messagebox
import time
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import seaborn as sns

# Function to check optimal conditions
def check_optimal_conditions(user_data):
    mass = float(user_data["Mass (kg)"])
    temperature = float(user_data["Temperature (°C)"])
    altitude = float(user_data["Altitude (m)"])
    velocity = float(user_data["Velocity (m/s)"])
    pressure = float(user_data["Pressure (hPa)"])
    humidity = float(user_data["Humidity (%)"])
    wind_speed = float(user_data["Wind Speed (m/s)"])
    descent_rate = float(user_data["Descent Rate (m/s)"].split()[0])

    optimal_conditions = {
        "Mass (kg)": (50 <= mass <= 200),
        "Temperature (°C)": (-40 <= temperature <= 40),
        "Altitude (m)": (500 <= altitude <= 35000),
        "Velocity (m/s)": (5 <= velocity <= 200),
        "Pressure (hPa)": (50 <= pressure <= 1013),
        "Humidity (%)": (10 <= humidity <= 80),
        "Wind Speed (m/s)": (0 <= wind_speed <= 30),
        "Descent Rate (m/s)": (3 <= descent_rate <= 15)
    }

    return all(optimal_conditions.values())

# Function to create animated graphs
def create_animated_graphs(user_data):
    # Create a new window for the animated graphs
    graph_window = tk.Tk()
    graph_window.title("Parachute Deployment Analysis - Animation")
    graph_window.geometry("1280x800")
    graph_window.configure(bg="#f4f4f4")

    # Extract user data
    mass = float(user_data["Mass (kg)"])
    temperature = float(user_data["Temperature (°C)"])
    altitude = float(user_data["Altitude (m)"])
    velocity = float(user_data["Velocity (m/s)"])
    pressure = float(user_data["Pressure (hPa)"])
    humidity = float(user_data["Humidity (%)"])
    descent_rate = float(user_data["Descent Rate (m/s)"].split()[0])

    # Create a figure with 4 subplots (2 rows, 2 columns)
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("Parachute Deployment Analysis - Animation", fontsize=16)

    # Initialize data for animation
    altitudes = np.linspace(0, altitude, 100)
    temperatures = temperature - (0.0065 * altitudes)
    velocities = np.linspace(0, velocity, 10)
    pressure_range = np.linspace(pressure - 50, pressure + 50, 10)
    humidity_range = np.linspace(humidity - 10, humidity + 10, 10)
    masses = np.linspace(mass - 10, mass + 10, 5)

    # Plot 1: Temperature vs. Altitude (Line Plot)
    line, = axes[0, 0].plot(altitudes, temperatures, color="red", marker="o")
    axes[0, 0].set_title("Temperature vs. Altitude")
    axes[0, 0].set_xlabel("Altitude (m)")
    axes[0, 0].set_ylabel("Temperature (°C)")
    axes[0, 0].grid(True)

    # Plot 2: Velocity vs. Descent Rate (Scatter Plot)
    scatter = axes[0, 1].scatter(velocities, [descent_rate] * len(velocities), color="blue")
    axes[0, 1].set_title("Velocity vs. Descent Rate")
    axes[0, 1].set_xlabel("Velocity (m/s)")
    axes[0, 1].set_ylabel("Descent Rate (m/s)")
    axes[0, 1].grid(True)

    # Plot 3: Pressure vs. Humidity (Heatmap)
    pressure_grid, humidity_grid = np.meshgrid(pressure_range, humidity_range)
    data = np.sqrt(pressure_grid**2 + humidity_grid**2)
    heatmap = sns.heatmap(data, ax=axes[1, 0], cmap="coolwarm", annot=True, fmt=".1f")
    axes[1, 0].set_title("Pressure vs. Humidity (Heatmap)")
    axes[1, 0].set_xlabel("Pressure (hPa)")
    axes[1, 0].set_ylabel("Humidity (%)")

    # Plot 4: Mass vs. Descent Rate (Bar Plot)
    bars = axes[1, 1].bar(masses, [descent_rate] * len(masses), color="green")
    axes[1, 1].set_title("Mass vs. Descent Rate")
    axes[1, 1].set_xlabel("Mass (kg)")
    axes[1, 1].set_ylabel("Descent Rate (m/s)")
    axes[1, 1].grid(True)

    # Embed the figure in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Function to update the graphs dynamically
    def update_graphs():
        nonlocal temperatures, velocities, pressure_range, humidity_range, masses

        # Simulate reaching optimal conditions over time
        for i in range(100):
            # Update temperature and altitude
            temperatures = temperature - (0.0065 * altitudes * (i / 100))
            line.set_ydata(temperatures)

            # Update velocity and descent rate
            velocities = np.linspace(0, velocity * (i / 100), 10)
            scatter.set_offsets(np.c_[velocities, [descent_rate * (i / 100)] * len(velocities)])

            # Update pressure and humidity
            pressure_range = np.linspace(pressure - 50 * (1 - i / 100), pressure + 50 * (1 - i / 100), 10)
            humidity_range = np.linspace(humidity - 10 * (1 - i / 100), humidity + 10 * (1 - i / 100), 10)
            pressure_grid, humidity_grid = np.meshgrid(pressure_range, humidity_range)
            data = np.sqrt(pressure_grid**2 + humidity_grid**2)
            heatmap.set_data(data)

            # Update mass and descent rate
            masses = np.linspace(mass - 10 * (1 - i / 100), mass + 10 * (1 - i / 100), 5)
            for bar, h in zip(bars, [descent_rate * (i / 100)] * len(masses)):
                bar.set_height(h)

            # Redraw the canvas
            canvas.draw()
            time.sleep(0.1)

            # Check if optimal conditions are met
            user_data["Mass (kg)"] = str(mass)
            user_data["Temperature (°C)"] = str(temperature * (i / 100))
            user_data["Altitude (m)"] = str(altitude * (i / 100))
            user_data["Velocity (m/s)"] = str(velocity * (i / 100))
            user_data["Pressure (hPa)"] = str(pressure * (i / 100))
            user_data["Humidity (%)"] = str(humidity * (i / 100))
            user_data["Descent Rate (m/s)"] = f"{descent_rate * (i / 100)} m/s"

            if check_optimal_conditions(user_data):
                messagebox.showinfo("Deployment", "Deploy your parachute now!")
                break

    # Start the animation in a separate thread
    threading.Thread(target=update_graphs).start()

    # Run the graph window
    graph_window.mainloop()

# Function to start the countdown and then launch the animated graphs
def start_jump():
    def countdown():
        for i in range(3, 0, -1):
            countdown_label.config(text=str(i))
            root.update()
            time.sleep(1)
        countdown_label.config(text="GO!")
        root.update()
        time.sleep(1)
        countdown_label.config(text="")
        root.update()

        # Simulate user data (replace with actual data collection)
        user_data = {
            "Mass (kg)": "100",
            "Temperature (°C)": "20",
            "Altitude (m)": "10000",
            "Velocity (m/s)": "50",
            "Pressure (hPa)": "500",
            "Humidity (%)": "50",
            "Wind Speed (m/s)": "10",
            "Descent Rate (m/s)": "5 m/s"
        }

        # Launch the animated graphs
        create_animated_graphs(user_data)

    # Run the countdown in a separate thread to avoid blocking the main thread
    threading.Thread(target=countdown).start()

# Initialize Main Window
root = tk.Tk()
root.title("Parachute Deployment System - JUMP")
root.geometry("1280x800")
root.configure(bg="#f4f4f4")

# JUMP Button
jump_button = tk.Button(root, text="JUMP", command=start_jump, bg="#ff0000", fg="white", font=("Arial", 24, "bold"))
jump_button.pack(pady=50)

# Countdown Label
countdown_label = tk.Label(root, text="", font=("Arial", 48, "bold"), bg="#f4f4f4")
countdown_label.pack(pady=20)

# Run the App
root.mainloop()