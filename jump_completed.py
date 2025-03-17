# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

# Function to create jump completed UI
def create_jump_completed_ui(user_data):
    # Initialize Tkinter Window for Jump Completed
    completed_window = tk.Tk()
    completed_window.title("Jump Completed")
    completed_window.geometry("1920x1080")  # Set window size to 1920x1080
    completed_window.configure(bg="#f0f0f0")

    # Flag to check if the window is still open
    window_open = True

    # Function to open GUI 5 (Project Owner Info)
    def open_gui5():
        nonlocal window_open
        window_open = False  # Stop the animation
        completed_window.destroy()  # Close the current window
        import project_owner  # Import and run the project_owner.py GUI
        project_owner.create_project_owner_ui()

    # Bind the window close event to open GUI 5
    completed_window.protocol("WM_DELETE_WINDOW", open_gui5)

    # Add a Title
    title_label = tk.Label(completed_window, text="🎉 Landing Successful! 🎉", font=("Arial", 24, "bold"), bg="#f0f0f0")
    title_label.pack(pady=20)

    # Add a Subtitle
    subtitle_label = tk.Label(completed_window, text="You have reached your final destination. Hope you enjoyed your dive!", font=("Arial", 16), bg="#f0f0f0")
    subtitle_label.pack(pady=10)

    # Add a Frame for Indicators
    indicators_frame = tk.Frame(completed_window, bg="#ffffff", padx=20, pady=20, relief="ridge", bd=3)
    indicators_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Add Indicators
    indicators = [
        "Glide Ratio = 0 ✅",
        "Impact Force shows a final spike, then stabilizes ✅",
        "Wind speed is stable, direction does not change ✅",
        "Altitude is near 0, pressure is at maximum, descent rate is 0 ✅",
        "Body position stability graph flattens out ✅",
    ]

    # Function to animate green ticks
    def animate_ticks():
        if window_open:  # Only animate if the window is still open
            for label in tick_labels:
                current_color = label.cget("fg")
                new_color = "#00ff00" if current_color == "#f0f0f0" else "#f0f0f0"
                label.config(fg=new_color)
            completed_window.after(500, animate_ticks)  # Repeat every 500ms

    tick_labels = []
    for indicator in indicators:
        label = tk.Label(indicators_frame, text=indicator, font=("Arial", 14), bg="#ffffff", fg="#00ff00")
        label.pack(anchor="w", pady=5)
        tick_labels.append(label)

    # Start the tick animation
    animate_ticks()

    # Add a Frame for User Data and Auto-Calculated Values
    data_frame = tk.Frame(completed_window, bg="#ffffff", padx=20, pady=20, relief="ridge", bd=3)
    data_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Add a Canvas and Scrollbar for User Data and Auto-Calculated Values
    canvas = tk.Canvas(data_frame, bg="#ffffff", bd=0, highlightthickness=0)
    scrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#ffffff")

    # Configure the Canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Bind the Canvas to the Scrollable Frame
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Pack the Canvas and Scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Add User Data on the Left
    user_data_label = tk.Label(scrollable_frame, text="User Input Data", font=("Arial", 16, "bold"), bg="#ffffff")
    user_data_label.grid(row=0, column=0, sticky="w", pady=10, padx=10)

    row = 1
    for key, value in user_data.items():
        tk.Label(scrollable_frame, text=f"{key}: {value}", font=("Arial", 14), bg="#ffffff").grid(row=row, column=0, sticky="w", pady=5, padx=10)
        row += 1

    # Add Auto-Calculated Values on the Right
    auto_calculated_label = tk.Label(scrollable_frame, text="Auto-Calculated Values", font=("Arial", 16, "bold"), bg="#ffffff")
    auto_calculated_label.grid(row=0, column=1, sticky="w", pady=10, padx=10)

    auto_calculated_values = {
        "Pressure (hPa)": user_data.get("Pressure (hPa)", "N/A"),
        "Humidity (%)": user_data.get("Humidity (%)", "N/A"),
        "Wind Speed (m/s)": user_data.get("Wind Speed (m/s)", "N/A"),
        "Descent Rate (m/s)": user_data.get("Descent Rate (m/s)", "N/A"),
        "Glide Ratio": user_data.get("Glide Ratio", "N/A"),
        "Impact Force (N)": user_data.get("Impact Force (N)", "N/A"),
        "Horizontal Displacement (m)": user_data.get("Horizontal Displacement (m)", "N/A"),
        "Body Position": user_data.get("Body Position", "N/A"),
    }

    row = 1
    for key, value in auto_calculated_values.items():
        tk.Label(scrollable_frame, text=f"{key}: {value}", font=("Arial", 14), bg="#ffffff", fg="#007acc").grid(row=row, column=1, sticky="w", pady=5, padx=10)
        row += 1

    # Add a Final Message
    final_message = tk.Label(completed_window, text="🔹 Thank you for using the Parachute Deployment System! 🔹", font=("Arial", 16, "bold"), bg="#f0f0f0")
    final_message.pack(pady=20)

    # Run the Jump Completed Window
    completed_window.mainloop()