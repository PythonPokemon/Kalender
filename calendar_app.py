import tkinter as tk
from tkinter import ttk
import calendar

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalender-App")

        self.cal = calendar.TextCalendar(calendar.SUNDAY)
        self.year = 2023
        self.month = 8

        self.frame = ttk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.label = ttk.Label(self.frame, text=f"{self.cal.formatmonth(self.year, self.month)}")
        self.label.pack()

        self.prev_button = ttk.Button(self.frame, text="Vorheriger Monat", command=self.prev_month)
        self.prev_button.pack(side="left")

        self.next_button = ttk.Button(self.frame, text="Nächster Monat", command=self.next_month)
        self.next_button.pack(side="right")

    def prev_month(self):
        self.month -= 1
        if self.month < 1:
            self.month = 12
            self.year -= 1
        self.update_calendar()

    def next_month(self):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        self.update_calendar()

    def update_calendar(self):
        self.label.config(text=f"{self.cal.formatmonth(self.year, self.month)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
