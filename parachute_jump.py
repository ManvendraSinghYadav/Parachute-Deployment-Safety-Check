# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np

# Function to create jump simulation
def create_jump_simulation(user_data):
    # Initialize Tkinter Window for Jump Simulation
    jump_window = tk.Tk()
    jump_window.title("Parachute Jump Simulation")
    jump_window.geometry("1400x900")
    jump_window.configure(bg="#f0f0f0")

    # Extract User Data
    mass = float(user_data["Mass (kg)"])
    altitude = float(user_data["Altitude (m)"])
    descent_rate = float(user_data["Descent Rate (m/s)"])
    glide_ratio = float(user_data["Glide Ratio"])
    impact_force = float(user_data["Impact Force (N)"])
    parachute_area = float(user_data["Parachute Area (m²)"])
    wind_speed = float(user_data["Wind Speed (m/s)"])
    pressure = float(user_data["Pressure (hPa)"])

    # Check Weight Category
    if mass > 100:
        messagebox.showwarning("Weight Warning", "Weight is over 100 kg! It might be riskier for the parachute to ensure a safe glide.")

    # Create a Figure with 2x2 Subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 9), constrained_layout=True)
    (ax1, ax2), (ax3, ax4) = axes
    fig.suptitle("Parachute Jump Simulation", fontsize=16)

    # Graph 1: Impact Force vs. Glide Ratio (Reverse)
    def create_impact_force_vs_glide_ratio():
        ax1.set_title("Impact Force vs. Glide Ratio (Reverse)", fontsize=12)
        ax1.set_xlabel("Glide Ratio", fontsize=10)
        ax1.set_ylabel("Impact Force (N)", fontsize=10)
        ax1.grid(True)

        # Initial and Final Values
        glide_ratios = np.linspace(glide_ratio, 0.1, 100)
        impact_forces = mass * 9.81 * glide_ratios  # Simplified calculation

        line1, = ax1.plot([], [], lw=2, color="blue")
        ax1.set_xlim(glide_ratio + 0.1, 0)
        ax1.set_ylim(impact_force + 100, 0)

        def animate1(i):
            line1.set_data(glide_ratios[:i], impact_forces[:i])
            return line1,

        # Store the animation object to prevent garbage collection
        ani1 = FuncAnimation(fig, animate1, frames=len(glide_ratios), interval=50, blit=False)
        return ani1

    # Graph 2: Descent Rate vs. Altitude (Reverse)
    def create_descent_rate_vs_altitude():
        ax2.set_title("Descent Rate vs. Altitude (Reverse)", fontsize=12)
        ax2.set_xlabel("Altitude (m)", fontsize=10)
        ax2.set_ylabel("Descent Rate (m/s)", fontsize=10)
        ax2.grid(True)

        # Simulate descent rate based on altitude
        altitudes = np.linspace(altitude, 0, 100)
        descent_rates = np.sqrt((2 * mass * 9.81) / (1.225 * parachute_area * 1.5)) * np.ones_like(altitudes)  # Simplified calculation

        line2, = ax2.plot([], [], lw=2, color="red")
        ax2.set_xlim(altitude + 100, 0)
        ax2.set_ylim(descent_rate + 2, 0)

        def animate2(i):
            line2.set_data(altitudes[:i], descent_rates[:i])
            if altitudes[i] <= 0:  # Check if altitude reaches 0
                jump_window.after(1000, lambda: open_jump_completed(user_data))  # Open GUI 4 after 1 second
            return line2,

        # Store the animation object to prevent garbage collection
        ani2 = FuncAnimation(fig, animate2, frames=len(altitudes), interval=50, blit=False)
        return ani2

    # Graph 3: Body Position Stability (Reverse)
    def create_body_position_stability():
        ax3.set_title("Body Position Stability (Reverse)", fontsize=12)
        ax3.set_xlabel("Time (s)", fontsize=10)
        ax3.set_ylabel("Stability Index", fontsize=10)
        ax3.grid(True)

        # Simulate stability over time
        time = np.linspace(10, 0, 100)
        stability = np.sin(time)  # Simulated stability index

        line3, = ax3.plot([], [], lw=2, color="purple")
        ax3.set_xlim(10, 0)
        ax3.set_ylim(1, -1)

        def animate3(i):
            line3.set_data(time[:i], stability[:i])
            return line3,

        # Store the animation object to prevent garbage collection
        ani3 = FuncAnimation(fig, animate3, frames=len(time), interval=50, blit=False)
        return ani3

    # Graph 4: Wind Speed vs. Direction (Reverse)
    def create_wind_speed_vs_direction():
        ax4.set_title("Wind Speed vs. Direction (Reverse)", fontsize=12)
        ax4.set_xlabel("Direction (degrees)", fontsize=10)
        ax4.set_ylabel("Wind Speed (m/s)", fontsize=10)
        ax4.grid(True)

        # Simulate wind direction (0 to 360 degrees)
        directions = np.linspace(360, 0, 100)
        wind_speeds = wind_speed * np.sin(np.radians(directions))  # Simulated wind speed variation

        line4, = ax4.plot([], [], lw=2, color="green")
        ax4.set_xlim(360, 0)
        ax4.set_ylim(wind_speed + 2, 0)

        def animate4(i):
            line4.set_data(directions[:i], wind_speeds[:i])
            return line4,

        # Store the animation object to prevent garbage collection
        ani4 = FuncAnimation(fig, animate4, frames=len(directions), interval=50, blit=False)
        return ani4

    # Function to open GUI 4 (Jump Completed)
    def open_jump_completed(user_data):
        jump_window.destroy()  # Close the current window
        import jump_completed  # Import and run the jump_completed.py GUI
        jump_completed.create_jump_completed_ui(user_data)

    # Create Animations
    ani1 = create_impact_force_vs_glide_ratio()
    ani2 = create_descent_rate_vs_altitude()
    ani3 = create_body_position_stability()
    ani4 = create_wind_speed_vs_direction()

    # Embed the Figure in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=jump_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # Run the Jump Simulation Window
    jump_window.mainloop()