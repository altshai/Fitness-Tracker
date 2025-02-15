import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import os

# Workout Class
class Workout:
    def __init__(self, date, exercise_type, duration, calories_burned):
        self.date = date
        self.exercise_type = exercise_type
        self.duration = duration
        self.calories_burned = calories_burned

    def __str__(self):
        return f"{self.date} | {self.exercise_type} | {self.duration} min | {self.calories_burned} cal"

# User Class
class User:
    def __init__(self):
        self.workouts = []
        self.load_data()  # Auto-load on start

    def add_workout(self, workout):
        self.workouts.append(workout)

    def delete_workout(self, index):
        if 0 <= index < len(self.workouts):
            del self.workouts[index]

    def save_data(self, filename="workouts.txt"):
        with open(filename, "w") as file:
            for workout in self.workouts:
                file.write(f"{workout.date},{workout.exercise_type},{workout.duration},{workout.calories_burned}\n")

    def load_data(self, filename="workouts.txt"):
        if os.path.exists(filename):
            with open(filename, "r") as file:
                self.workouts.clear()
                for line in file:
                    date, exercise_type, duration, calories_burned = line.strip().split(',')
                    self.workouts.append(Workout(date, exercise_type, int(duration), int(calories_burned)))

# GUI Application
class FitnessTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏋️‍♂️ Personal Fitness Tracker")
        self.root.geometry("500x500")
        self.root.configure(bg="#e3f2fd")

        self.user = User()

        # Title
        ttk.Label(root, text="🏋️ Personal Fitness Tracker", font=("Arial", 16, "bold"), background="#e3f2fd").pack(pady=10)

        # Workout Entry Frame
        frame = ttk.Frame(root)
        frame.pack(pady=10)

        ttk.Label(frame, text="Date:").grid(row=0, column=0)
        self.date_entry = DateEntry(frame, width=12, background="blue", foreground="white", borderwidth=2)
        self.date_entry.grid(row=0, column=1, padx=5)

        ttk.Label(frame, text="Exercise Type:").grid(row=1, column=0)
        self.exercise_entry = ttk.Entry(frame, width=20)
        self.exercise_entry.grid(row=1, column=1, padx=5)

        ttk.Label(frame, text="Duration (min):").grid(row=2, column=0)
        self.duration_entry = ttk.Entry(frame, width=5)
        self.duration_entry.grid(row=2, column=1, padx=5)

        ttk.Label(frame, text="Calories Burned:").grid(row=3, column=0)
        self.calories_entry = ttk.Entry(frame, width=5)
        self.calories_entry.grid(row=3, column=1, padx=5)

        ttk.Button(frame, text="Add Workout", command=self.add_workout).grid(row=4, columnspan=2, pady=10)

        # Workout List
        self.workout_listbox = tk.Listbox(root, width=50, height=10)
        self.workout_listbox.pack(pady=10)

        # Buttons
        ttk.Button(root, text="Delete Workout", command=self.delete_workout).pack(pady=5)
        ttk.Button(root, text="Save Workouts", command=self.save_workouts).pack(pady=5)

        # Statistics
        self.stats_label = ttk.Label(root, text="", font=("Arial", 10, "bold"), background="#e3f2fd")
        self.stats_label.pack(pady=5)

        self.update_workout_list()
        self.update_statistics()

    def add_workout(self):
        date = self.date_entry.get()
        exercise_type = self.exercise_entry.get()
        duration = self.duration_entry.get()
        calories_burned = self.calories_entry.get()

        if not exercise_type or not duration.isdigit() or not calories_burned.isdigit():
            messagebox.showerror("Error", "Please enter valid workout details.")
            return

        workout = Workout(date, exercise_type, int(duration), int(calories_burned))
        self.user.add_workout(workout)
        self.update_workout_list()
        self.update_statistics()
        messagebox.showinfo("Success", "Workout added successfully!")

    def delete_workout(self):
        selected_index = self.workout_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a workout to delete.")
            return

        self.user.delete_workout(selected_index[0])
        self.update_workout_list()
        self.update_statistics()
        messagebox.showinfo("Success", "Workout deleted successfully!")

    def save_workouts(self):
        self.user.save_data()
        messagebox.showinfo("Success", "Workouts saved successfully!")

    def update_workout_list(self):
        self.workout_listbox.delete(0, tk.END)
        for workout in self.user.workouts:
            self.workout_listbox.insert(tk.END, str(workout))

    def update_statistics(self):
        total_workouts = len(self.user.workouts)
        total_duration = sum(w.duration for w in self.user.workouts)
        total_calories = sum(w.calories_burned for w in self.user.workouts)
        avg_duration = total_duration // total_workouts if total_workouts else 0

        stats_text = f"📊 Workouts: {total_workouts} | Avg Duration: {avg_duration} min | Total Calories: {total_calories} cal"
        self.stats_label.config(text=stats_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessTrackerApp(root)
    root.mainloop()
