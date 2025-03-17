# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext  # Import scrolledtext for scrollable text area
import webbrowser

# Function to open links in a web browser
def open_link(url):
    webbrowser.open(url)

# Function to create the project owner UI
def create_project_owner_ui():
    # Initialize Tkinter Window for Project Owner
    owner_window = tk.Tk()
    owner_window.title("Project Owner - Manvendra Singh Yadav")
    owner_window.geometry("1920x1080")  # Set window size to 1920x1080
    owner_window.configure(bg="#2c3e50")  # Dark theme background

    # Add a Title
    title_label = tk.Label(owner_window, text="🚀 Parachute Deployment System 🚀", font=("Arial", 28, "bold"), bg="#2c3e50", fg="#ecf0f1")
    title_label.pack(pady=20)

    # Add a Subtitle
    subtitle_label = tk.Label(owner_window, text="Developed by Manvendra Singh Yadav", font=("Arial", 18), bg="#2c3e50", fg="#bdc3c7")
    subtitle_label.pack(pady=10)

    # Add a Frame for Owner Information
    owner_frame = tk.Frame(owner_window, bg="#34495e", padx=20, pady=20, relief="ridge", bd=3)
    owner_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Add Owner Information
    tk.Label(owner_frame, text="👨‍💻 Owner Information:", font=("Arial", 16, "bold"), bg="#34495e", fg="#ecf0f1").pack(anchor="w", pady=10)

    # Name
    tk.Label(owner_frame, text="Name: Manvendra Singh Yadav", font=("Arial", 14), bg="#34495e", fg="#ecf0f1").pack(anchor="w", pady=5)

    # GitHub Profile Link
    github_link = tk.Label(owner_frame, text="GitHub Profile: https://github.com/ManvendraSinghYadav", font=("Arial", 14), bg="#34495e", fg="#3498db", cursor="hand2")
    github_link.pack(anchor="w", pady=5)
    github_link.bind("<Button-1>", lambda e: open_link("https://github.com/ManvendraSinghYadav"))

    # LinkedIn Profile Link
    linkedin_link = tk.Label(owner_frame, text="LinkedIn Profile: https://www.linkedin.com/in/manvendra-singh-yadav-roadkliq/", font=("Arial", 14), bg="#34495e", fg="#3498db", cursor="hand2")
    linkedin_link.pack(anchor="w", pady=5)
    linkedin_link.bind("<Button-1>", lambda e: open_link("https://www.linkedin.com/in/manvendra-singh-yadav-roadkliq/"))

    # Add a Frame for Project Summary
    summary_frame = tk.Frame(owner_window, bg="#34495e", padx=20, pady=20, relief="ridge", bd=3)
    summary_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Add Project Summary Title
    tk.Label(summary_frame, text="📝 Project Summary:", font=("Arial", 16, "bold"), bg="#34495e", fg="#ecf0f1").pack(anchor="w", pady=10)

    # Add a Scrollable Text Area for Project Summary
    summary_text = scrolledtext.ScrolledText(summary_frame, wrap=tk.WORD, width=100, height=10, font=("Arial", 14), bg="#34495e", fg="#ecf0f1")
    summary_text.pack(fill="both", expand=True)

    # Insert Project Summary Text
    summary_content = """
    The Parachute Deployment System is a simulation tool designed to analyze and predict the behavior of a parachute during descent. 
    It calculates key parameters such as descent rate, impact force, glide ratio, and body position stability based on user inputs.

    Key Features:
    - Real-time simulation of parachute deployment.
    - Interactive graphs for visualizing descent parameters.
    - Automatic calculation of pressure, humidity, and wind speed.
    - Reverse simulation to analyze landing conditions.

    Future Enhancements:
    - Integration with real-time sensors for live data analysis.
    - Advanced machine learning models for predictive analytics.
    - Compatibility with aerospace systems for real-world applications.
    """
    summary_text.insert(tk.END, summary_content)
    summary_text.configure(state="disabled")  # Make the text area read-only

    # Add a Frame for Benefits
    benefits_frame = tk.Frame(owner_window, bg="#34495e", padx=20, pady=20, relief="ridge", bd=3)
    benefits_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Add Benefits of the Project
    tk.Label(benefits_frame, text="🌟 Benefits of the Project:", font=("Arial", 16, "bold"), bg="#34495e", fg="#ecf0f1").pack(anchor="w", pady=10)

    benefits_text = """
    The Parachute Deployment System can revolutionize the aerospace industry by:
    - Providing real-time analysis of parachute performance.
    - Enhancing safety during parachute deployment.
    - Reducing the risk of accidents through predictive analytics.
    - Enabling better decision-making for pilots and engineers.

    With the addition of real-time sensors, this project can:
    - Monitor environmental conditions (e.g., wind speed, temperature, pressure).
    - Provide live feedback on parachute behavior.
    - Improve accuracy and reliability of simulations.
    """

    tk.Label(benefits_frame, text=benefits_text, font=("Arial", 14), bg="#34495e", fg="#ecf0f1", justify="left").pack(anchor="w", pady=5)

    # Add a Final Message
    final_message = tk.Label(owner_window, text="🔹 Thank you for exploring the Parachute Deployment System! 🔹", font=("Arial", 16, "bold"), bg="#2c3e50", fg="#ecf0f1")
    final_message.pack(pady=20)

    # Run the Project Owner Window
    owner_window.mainloop()