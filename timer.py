import tkinter as tk
import json
import time
import datetime
import calendar


class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracker")
        self.root.iconphoto(False, tk.PhotoImage(file="sand-clock.png"))
        self.root.geometry("400x400")
        self.elapsed_time = 0
        self.running = False

        # Create a frame to hold the GUI components
        self.frame = tk.Frame(self.root, bg="#f0f0f0")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Create GUI components
        self.project_label = tk.Label(self.frame, text="Time Tracker", font=("Helvetica", 24, "bold"), anchor="center",
                                      bg="#f0f0f0")
        self.project_label.pack(pady=10)

        self.project_label = tk.Label(self.frame, text="Task Name", font=("Helvetica", 12), bg="#f0f0f0")
        self.project_label.pack(pady=5)

        self.project_entry = tk.Entry(self.frame, font=("Helvetica", 12))
        self.project_entry.pack(pady=5)

        self.button_frame = tk.Frame(self.frame, bg="#f0f0f0")
        self.button_frame.pack(pady=10)

        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start_timer, font=("Helvetica", 12),
                                      bg="#4CAF50", fg="#ffffff")
        self.start_button.pack(side="left", padx=5)

        self.stop_button = tk.Button(self.button_frame, text="Pause", command=self.pause_timer, font=("Helvetica", 12),
                                     bg="#9b59b6", fg="#ffffff")
        self.stop_button.pack(side="left", padx=5)

        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset_timer, font=("Helvetica", 12),
                                      bg="#e74c3c", fg="#ffffff")
        self.reset_button.pack(side="left", padx=5)

        self.elapsed_time_label = tk.Label(self.frame, text="00:00:00", font=("Helvetica", 24, "bold"), bg="#f0f0f0")
        self.elapsed_time_label.pack(pady=10)

        self.save_button = tk.Button(self.frame, text="Save", command=self.save_timer_data, font=("Helvetica", 12),
                                     bg="#4CAF50", fg="#ffffff")
        self.save_button.pack(pady=5)

    def reset_timer(self):
        self.pause_timer()
        self.elapsed_time_label.config(text="00:00:00")
        self.elapsed_time = 0

    def pause_timer(self):
        self.running = False

    def start_timer(self):
        self.running = True
        self.update_timer()

    def update_timer(self):
        if self.running:
            self.elapsed_time += 1
            self.elapsed_time_label.config(text=time.strftime("%H:%M:%S", time.gmtime(self.elapsed_time)))
            self.root.after(1000, self.update_timer)

    def save_timer_data(self):
        try:
            with open("data.json", "r") as file:  # read the data from file if it is already there
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        # access current monty, date(day of the month), project, time 
        curr_month = calendar.month_name[datetime.date.today().month]
        curr_date = datetime.date.today().strftime("%d").lstrip("0")
        curr_task = self.project_entry.get()
        curr_time = time.strftime("%H:%M:%S", time.gmtime(self.elapsed_time))

        # add the current project and time to data
        if curr_month in data:
            if curr_date in data[curr_month]:
                if curr_task in data[curr_month][curr_date]:
                    hrs, minutes, sec = data[curr_month][curr_date][curr_task].split(":")
                    c_hrs, c_min, c_sec = curr_time.split(":")
                    t_hrs = int(hrs) + int(c_hrs)
                    t_min = int(minutes) + int(c_min)
                    t_sec = int(sec) + int(c_sec)
                    curr_time = str(t_hrs) + ":" + str(t_min) + ":" + str(t_sec)
                    data[curr_month][curr_date][curr_task] = curr_time
                else:
                    data[curr_month][curr_date][curr_task] = curr_time
            else:
                data[curr_month][curr_date] = {
                    curr_task: curr_time
                }
        else:
            data[curr_month] = {
                curr_date: {
                    curr_task: curr_time
                }
            }

        # add the data to the file in write mode
        # it will create a new file if it's not present
        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)

        self.reset_timer()  # reset the timer


timer_window = tk.Tk()
app = TimerApp(timer_window)
timer_window.mainloop()
