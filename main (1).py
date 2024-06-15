import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import matplotlib.pyplot as plt

class FitnessChallengeApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Fitness Challenge App")
        self.geometry("600x400")

        self.current_page = None
        self.user_data = {}  # Store user data

        self.show_home_page()

    def show_home_page(self):
        if self.current_page:
            self.current_page.destroy()

        self.current_page = tk.Frame(self)
        self.current_page.pack(fill="both", expand=True)

        # Add widgets for home page
        label = ttk.Label(self.current_page, text="Welcome to Fitness Challenge App", font=("Helvetica", 20))
        label.pack(pady=20)

        button = ttk.Button(self.current_page, text="Register", command=self.show_registration_page)
        button.pack(pady=10)

    def show_registration_page(self):
        if self.current_page:
            self.current_page.destroy()

        self.current_page = tk.Frame(self)
        self.current_page.pack(fill="both", expand=True)

        # Add widgets for registration page
        label = ttk.Label(self.current_page, text="Registration", font=("Helvetica", 16))
        label.pack(pady=20)

        # Add form fields
        name_label = ttk.Label(self.current_page, text="Name:")
        name_label.pack()
        self.name_entry = ttk.Entry(self.current_page)
        self.name_entry.pack(pady=5)

        age_label = ttk.Label(self.current_page, text="Age:")
        age_label.pack()
        self.age_entry = ttk.Entry(self.current_page)
        self.age_entry.pack(pady=5)

        weight_label = ttk.Label(self.current_page, text="Weight (kg):")
        weight_label.pack()
        self.weight_entry = ttk.Entry(self.current_page)
        self.weight_entry.pack(pady=5)

        height_label = ttk.Label(self.current_page, text="Height (cm):")
        height_label.pack()
        self.height_entry = ttk.Entry(self.current_page)
        self.height_entry.pack(pady=5)

        register_button = ttk.Button(self.current_page, text="Register", command=self.register_user)
        register_button.pack(pady=10)

    def register_user(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        weight = self.weight_entry.get()
        height = self.height_entry.get()

        if not name or not age or not weight or not height:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            age = int(age)
            weight = float(weight)
            height = float(height)
        except ValueError:
            messagebox.showerror("Error", "Age must be an integer, weight and height must be numeric values.")
            return

        # Save user data
        self.user_data['name'] = name
        self.user_data['age'] = age
        self.user_data['weight'] = weight
        self.user_data['height'] = height

        messagebox.showinfo("Success", "Registration successful!")

        self.show_challenge_page()

    def show_challenge_page(self):
        if self.current_page:
            self.current_page.destroy()

        self.current_page = tk.Frame(self)
        self.current_page.pack(fill="both", expand=True)

        # Add widgets for challenge page
        label = ttk.Label(self.current_page, text="Choose Your Challenge", font=("Helvetica", 16))
        label.pack(pady=20)

        # Add challenge options
        challenges = ["Walking", "Cycling", "Swimming", "Running"]
        self.challenge_var = tk.StringVar(self.current_page)
        self.challenge_var.set(challenges[0])  # Set default value

        for challenge in challenges:
            radio_button = ttk.Radiobutton(self.current_page, text=challenge, variable=self.challenge_var, value=challenge)
            radio_button.pack()

        select_button = ttk.Button(self.current_page, text="Select", command=self.start_challenge)
        select_button.pack(pady=10)

    def start_challenge(self):
        challenge = self.challenge_var.get()
        message = random.choice(motivational_messages.get(challenge, []))

        messagebox.showinfo("Challenge Selected", f"You've selected {challenge} challenge.\n\n{message}")

        # Save challenge choice
        self.user_data['challenge'] = challenge

        self.show_track_activity_page()

    def show_track_activity_page(self):
        if self.current_page:
            self.current_page.destroy()

        self.current_page = tk.Frame(self)
        self.current_page.pack(fill="both", expand=True)

        # Add widgets for track activity page
        label = ttk.Label(self.current_page, text="Track Your Activity", font=("Helvetica", 16))
        label.pack(pady=20)

        # Add form fields
        height_label = ttk.Label(self.current_page, text="Height (cm):")
        height_label.pack()
        self.height_entry = ttk.Entry(self.current_page)
        self.height_entry.pack(pady=5)

        weight_label = ttk.Label(self.current_page, text="Weight (kg):")
        weight_label.pack()
        self.weight_entry = ttk.Entry(self.current_page)
        self.weight_entry.pack(pady=5)

        calories_label = ttk.Label(self.current_page, text="Calories Burned:")
        calories_label.pack()
        self.calories_entry = ttk.Entry(self.current_page)
        self.calories_entry.pack(pady=5)

        submit_button = ttk.Button(self.current_page, text="Submit", command=self.show_output_page)
        submit_button.pack(pady=10)

    def show_output_page(self):
        height = self.user_data['height']
        weight = self.user_data['weight']
        calories_burned = self.calories_entry.get()

        try:
            calories_burned = float(calories_burned)
        except ValueError:
            messagebox.showerror("Error", "Calories burned must be a numeric value.")
            return

        bmi = self.calculate_bmi(height, weight)
        suggestions = self.get_suggestions(bmi)
        message = self.get_message(bmi)

        # Save activity data
        self.user_data['calories_burned'] = calories_burned
        self.user_data['bmi'] = bmi

        # Generate graph
        self.generate_graph()

        messagebox.showinfo("Output", f"BMI: {bmi}\n\n{suggestions}\n\n{message}")

        # Display graph
        plt.show()

    def calculate_bmi(self, height, weight):
        height_meters = height / 100.0
        bmi = weight / (height_meters ** 2)
        return bmi

    def get_suggestions(self, bmi):
        if bmi < 18.5:
            return "Your BMI is below normal. You may need to increase your calorie intake and focus on gaining weight. Consult with a nutritionist for a proper diet plan."
        elif 18.5 <= bmi < 25:
            return "Your BMI is within the normal range. Maintain a balanced diet and regular exercise routine to stay healthy."
        else:
            return "Your BMI is above normal. Consider reducing calorie intake and increasing physical activity. Consult with a healthcare professional for personalized advice."

    def get_message(self, bmi):
        if bmi < 18.5:
            return "Remember, your health journey is a marathon, not a sprint. Take it one step at a time and celebrate your progress along the way!"
        elif 18.5 <= bmi < 25:
            return "Great job! Your dedication to your health is paying off. Keep up the good work and enjoy the benefits of a healthy lifestyle!"
        else:
            return "It's never too late to prioritize your health. Small changes today can lead to big improvements tomorrow. You've got this!"

    def generate_graph(self):
        labels = ['Height', 'Weight', 'Calories Burned', 'BMI']
        values = [self.user_data['height'], self.user_data['weight'], self.user_data['calories_burned'], self.user_data['bmi']]

        plt.bar(labels, values, color=['blue', 'green', 'orange', 'red'])
        plt.xlabel('Metrics')
        plt.ylabel('Values')
        plt.title('User Metrics')
        plt.savefig('graph.png')
        plt.close()

# Define motivational messages
motivational_messages = {
    'Walking': [
        "Keep walking, every step counts!",
        "Walk your way to a healthier you!",
        "Walk as if you are kissing the Earth with your feet.",
        "Walking is the best possible exercise. Habituate yourself to walk very far.",
        "A journey of a thousand miles begins with a single step."
    ],
    'Cycling': [
        "Pedal your way to fitness!",
        "Life is like riding a bicycle. To keep your balance, you must keep moving.",
        "Enjoy the ride and feel the breeze!",
        "Keep calm and cycle on!",
        "Every pedal stroke gets you closer to your goal."
    ],
    'Swimming': [
        "Dive in and make a splash!",
        "Swim like nobody's watching!",
        "The water is your friend. You don't have to fight with water, just share the same spirit as the water, and it will help you move.",
        "Feel the rhythm of the strokes and glide through the water!",
        "Swimming is not just a sport, it's a way of life."
    ],
    'Running': [
        "Run like the wind!",
        "The only bad run is the one that didn't happen.",
        "Your body can stand almost anything. It's your mind that you have to convince.",
        "Run the day, don't let the day run you!",
        "Running is the greatest metaphor for life, because you get out of it what you put into it."
    ]
}

if __name__ == "__main__":
    app = FitnessChallengeApp()
    app.mainloop()
