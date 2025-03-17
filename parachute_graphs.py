# -*- coding: utf-8 -*-

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np

# Function to create graphs
def create_graphs(user_data):
    # Initialize Tkinter Window for Graphs
    graph_window = tk.Tk()
    graph_window.title("Parachute Deployment Analysis Graphs")
    graph_window.geometry("1400x900")
    graph_window.configure(bg="#f0f0f0")

    # Extract User Data
    mass = float(user_data["Mass (kg)"])
    temperature = float(user_data["Temperature (°C)"])
    altitude = float(user_data["Altitude (m)"])
    velocity = float(user_data["Velocity (m/s)"])
    parachute_area = float(user_data["Parachute Area (m²)"])
    parachute_shape = user_data["Parachute Shape"]
    body_position = user_data["Body Position"]
    pressure = float(user_data["Pressure (hPa)"])
    humidity = float(user_data["Humidity (%)"])
    wind_speed = float(user_data["Wind Speed (m/s)"])
    descent_rate = float(user_data["Descent Rate (m/s)"])
    glide_ratio = float(user_data["Glide Ratio"])
    impact_force = float(user_data["Impact Force (N)"])
    horizontal_displacement = float(user_data["Horizontal Displacement (m)"])

    # Create a Figure with 2x2 Subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 9), constrained_layout=True)
    (ax1, ax2), (ax3, ax4) = axes
    fig.suptitle("Parachute Deployment Analysis", fontsize=16)

    # Graph 1: Impact Force vs. Glide Ratio
    def create_impact_force_vs_glide_ratio():
        ax1.set_title("Impact Force vs. Glide Ratio", fontsize=12)
        ax1.set_xlabel("Glide Ratio", fontsize=10)
        ax1.set_ylabel("Impact Force (N)", fontsize=10)
        ax1.grid(True)

        # Initial and Final Values
        glide_ratios = np.linspace(0.1, glide_ratio, 100)
        impact_forces = mass * 9.81 * glide_ratios  # Simplified calculation

        line1, = ax1.plot([], [], lw=2, color="blue")
        ax1.set_xlim(0, glide_ratio + 0.1)
        ax1.set_ylim(0, impact_force + 100)

        def animate1(i):
            line1.set_data(glide_ratios[:i], impact_forces[:i])
            return line1,

        # Store the animation object to prevent garbage collection
        ani1 = FuncAnimation(fig, animate1, frames=len(glide_ratios), interval=50, blit=False)
        return ani1

    # Graph 2: Wind Speed vs. Direction
    def create_wind_speed_vs_direction():
        ax2.set_title("Wind Speed vs. Direction", fontsize=12)
        ax2.set_xlabel("Direction (degrees)", fontsize=10)
        ax2.set_ylabel("Wind Speed (m/s)", fontsize=10)
        ax2.grid(True)

        # Simulate wind direction (0 to 360 degrees)
        directions = np.linspace(0, 360, 100)
        wind_speeds = wind_speed * np.sin(np.radians(directions))  # Simulated wind speed variation

        line2, = ax2.plot([], [], lw=2, color="green")
        ax2.set_xlim(0, 360)
        ax2.set_ylim(0, wind_speed + 2)

        def animate2(i):
            line2.set_data(directions[:i], wind_speeds[:i])
            return line2,

        # Store the animation object to prevent garbage collection
        ani2 = FuncAnimation(fig, animate2, frames=len(directions), interval=50, blit=False)
        return ani2

    # Graph 3: Descent Rate vs. Pressure & Altitude
    def create_descent_rate_vs_pressure_altitude():
        ax3.set_title("Descent Rate vs. Altitude", fontsize=12)
        ax3.set_xlabel("Altitude (m)", fontsize=10)
        ax3.set_ylabel("Descent Rate (m/s)", fontsize=10)
        ax3.grid(True)

        # Simulate descent rate based on altitude
        altitudes = np.linspace(0, altitude, 100)
        descent_rates = np.sqrt((2 * mass * 9.81) / (1.225 * parachute_area * 1.5)) * np.ones_like(altitudes)  # Simplified calculation

        line3, = ax3.plot([], [], lw=2, color="red")
        ax3.set_xlim(0, altitude + 100)
        ax3.set_ylim(0, descent_rate + 2)

        def animate3(i):
            line3.set_data(altitudes[:i], descent_rates[:i])
            return line3,

        # Store the animation object to prevent garbage collection
        ani3 = FuncAnimation(fig, animate3, frames=len(altitudes), interval=50, blit=False)
        return ani3

    # Graph 4: Body Position Stability
    def create_body_position_stability():
        ax4.set_title("Body Position Stability", fontsize=12)
        ax4.set_xlabel("Time (s)", fontsize=10)
        ax4.set_ylabel("Stability Index", fontsize=10)
        ax4.grid(True)

        # Simulate stability over time
        time = np.linspace(0, 10, 100)
        stability = np.sin(time)  # Simulated stability index

        line4, = ax4.plot([], [], lw=2, color="purple")
        ax4.set_xlim(0, 10)
        ax4.set_ylim(-1, 1)

        def animate4(i):
            line4.set_data(time[:i], stability[:i])
            return line4,

        # Store the animation object to prevent garbage collection
        ani4 = FuncAnimation(fig, animate4, frames=len(time), interval=50, blit=False)
        return ani4

    # Create Animations
    ani1 = create_impact_force_vs_glide_ratio()
    ani2 = create_wind_speed_vs_direction()
    ani3 = create_descent_rate_vs_pressure_altitude()
    ani4 = create_body_position_stability()

    # Embed the Figure in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # Function to open GUI 3 after closing GUI 2
    def on_closing():
        graph_window.destroy()  # Close the current window
        import parachute_jump  # Import and run the parachute_jump.py GUI
        parachute_jump.create_jump_simulation(user_data)

    # Bind the window close event to the on_closing function
    graph_window.protocol("WM_DELETE_WINDOW", on_closing)

    # Run the Graph Window
    graph_window.mainloop()
