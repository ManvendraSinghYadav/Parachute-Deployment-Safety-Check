# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import pandas as pd
import numpy as np

# Function to create GUI 2 with graphs
def create_graphs(user_data):
    # Create a new window for GUI 2
    graph_window = tk.Tk()
    graph_window.title("Parachute Deployment Analysis")
    graph_window.geometry("1280x800")
    graph_window.configure(bg="#f4f4f4")

    # Extract user data
    mass = float(user_data["Mass (kg)"])
    temperature = float(user_data["Temperature (°C)"])
    altitude = float(user_data["Altitude (m)"])
    velocity = float(user_data["Velocity (m/s)"])
    pressure = float(user_data["Pressure (hPa)"])
    humidity = float(user_data["Humidity (%)"])
    descent_rate = float(user_data["Descent Rate (m/s)"].split()[0])  # Extract numeric value

    # Create a figure with 4 subplots (2 rows, 2 columns)
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("Parachute Deployment Analysis", fontsize=16)

    # Plot 1: Temperature vs. Altitude (Line Plot)
    altitudes = np.linspace(0, altitude, 100)
    temperatures = temperature - (0.0065 * altitudes)  # Temperature decreases with altitude
    axes[0, 0].plot(altitudes, temperatures, color="red", marker="o")
    axes[0, 0].set_title("Temperature vs. Altitude")
    axes[0, 0].set_xlabel("Altitude (m)")
    axes[0, 0].set_ylabel("Temperature (°C)")
    axes[0, 0].grid(True)

    # Plot 2: Velocity vs. Descent Rate (Scatter Plot)
    velocities = np.linspace(0, velocity, 10)
    descent_rates = np.sqrt((2 * mass * 9.81) / (1.225 * 3.0 * 1.5))  # Simplified descent rate calculation
    axes[0, 1].scatter(velocities, [descent_rate] * len(velocities), color="blue")
    axes[0, 1].set_title("Velocity vs. Descent Rate")
    axes[0, 1].set_xlabel("Velocity (m/s)")
    axes[0, 1].set_ylabel("Descent Rate (m/s)")
    axes[0, 1].grid(True)

    # Plot 3: Pressure vs. Humidity (Heatmap)
    pressure_range = np.linspace(pressure - 50, pressure + 50, 10)
    humidity_range = np.linspace(humidity - 10, humidity + 10, 10)
    pressure_grid, humidity_grid = np.meshgrid(pressure_range, humidity_range)
    data = np.sqrt(pressure_grid**2 + humidity_grid**2)  # Dummy data for heatmap
    sns.heatmap(data, ax=axes[1, 0], cmap="coolwarm", annot=True, fmt=".1f")
    axes[1, 0].set_title("Pressure vs. Humidity (Heatmap)")
    axes[1, 0].set_xlabel("Pressure (hPa)")
    axes[1, 0].set_ylabel("Humidity (%)")

    # Plot 4: Mass vs. Descent Rate (Bar Plot)
    masses = np.linspace(mass - 10, mass + 10, 5)
    descent_rates = [np.sqrt((2 * m * 9.81) / (1.225 * 3.0 * 1.5)) for m in masses]
    axes[1, 1].bar(masses, descent_rates, color="green")
    axes[1, 1].set_title("Mass vs. Descent Rate")
    axes[1, 1].set_xlabel("Mass (kg)")
    axes[1, 1].set_ylabel("Descent Rate (m/s)")
    axes[1, 1].grid(True)

    # Adjust layout
    plt.tight_layout()

    # Embed the figure in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Add a deployment recommendation
    deployment_status = "Deploy Parachute" if descent_rate < 5 else "Do Not Deploy Parachute"
    status_color = "green" if descent_rate < 5 else "red"
    status_label = tk.Label(graph_window, text=f"Recommendation: {deployment_status}", font=("Arial", 16, "bold"), fg=status_color, bg="#f4f4f4")
    status_label.pack(pady=10)

    # Run the graph window
    graph_window.mainloop()