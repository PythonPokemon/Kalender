import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import calendar
import json

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

        self.add_button = ttk.Button(self.frame, text="Termin hinzufügen", command=self.add_event)
        self.add_button.pack()

        self.view_button = ttk.Button(self.frame, text="Alle Termine anzeigen", command=self.view_all_events)
        self.view_button.pack()

        self.events = {}
        self.load_events()

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
        self.highlight_events()

    def load_events(self):
        try:
            with open("events.json", "r") as file:
                self.events = json.load(file)
        except FileNotFoundError:
            self.events = {}

    def save_events(self):
        with open("events.json", "w") as file:
            json.dump(self.events, file)

    def add_event(self):
        event_date = self.get_selected_date()
        if event_date:
            EventEditor(self.root, self.events, event_date, self.save_events, self.highlight_events)
    
    def get_selected_date(self):
        selected_date = f"{self.year}-{self.month:02d}"
        return selected_date

    def highlight_events(self):
        for child in self.label.winfo_children():
            child.destroy()

        self.label = ttk.Label(self.frame, text=f"{self.cal.formatmonth(self.year, self.month)}")
        self.label.pack()

        for event_date, events in self.events.items():
            year, month = map(int, event_date.split("-"))
            if year == self.year and month == self.month:
                day = int(events[0].split("-")[2])
                self.label.config(state="normal")
                self.label.tag_configure("highlight", background="red")
                self.label.tag_add("highlight", f"{day}.0", f"{day + 1}.0")
                self.label.config(state="disabled")

    def view_all_events(self):
        AllEventsViewer(self.events, self.save_events, self.highlight_events)


class EventEditor:
    def __init__(self, root, events, event_date, save_callback, highlight_callback):
        self.root = root
        self.events = events
        self.event_date = event_date
        self.save_callback = save_callback
        self.highlight_callback = highlight_callback

        self.event_window = tk.Toplevel(root)
        self.event_window.title("Termin hinzufügen")

        self.event_label = ttk.Label(self.event_window, text="Termin:")
        self.event_label.pack(padx=10, pady=5)

        self.event_entry = ttk.Entry(self.event_window)
        self.event_entry.pack(padx=10, pady=5)

        self.save_button = ttk.Button(self.event_window, text="Speichern", command=self.save_event)
        self.save_button.pack(padx=10, pady=5)

    def save_event(self):
        event = self.event_entry.get()
        if event:
            if self.event_date in self.events:
                self.events[self.event_date].append(event)
            else:
                self.events[self.event_date] = [event]
            self.save_callback()
            self.highlight_callback()
            self.event_window.destroy()
            messagebox.showinfo("Erfolg", "Termin hinzugefügt.")
        else:
            messagebox.showerror("Fehler", "Bitte geben Sie einen Termin ein.")


class AllEventsViewer:
    def __init__(self, events, save_callback, highlight_callback):
        self.events = events
        self.save_callback = save_callback
        self.highlight_callback = highlight_callback

        self.viewer_window = tk.Toplevel()
        self.viewer_window.title("Alle Termine anzeigen")

        self.notebook = ttk.Notebook(self.viewer_window)
        self.notebook.pack(fill="both", expand=True)

        for event_date, events_list in self.events.items():
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=event_date)

            self.listbox = tk.Listbox(tab)
            self.listbox.pack(padx=10, pady=10, fill="both", expand=True)
            for event in events_list:
                self.listbox.insert(tk.END, event)

            edit_button = ttk.Button(tab, text="Bearbeiten", command=lambda date=event_date: self.edit_event(date))
            edit_button.pack(padx=10, pady=5)

            delete_button = ttk.Button(tab, text="Löschen", command=lambda date=event_date: self.delete_event(date))
            delete_button.pack(padx=10, pady=5)

        self.viewer_window.protocol("WM_DELETE_WINDOW", self.close_viewer)

    def edit_event(self, date):
        EditEventEditor(self.viewer_window, date, self.events, self.save_callback, self.highlight_callback)

    def delete_event(self, date):
        del self.events[date]
        self.save_callback()
        self.highlight_callback()
        self.notebook.forget(self.notebook.select())

    def close_viewer(self):
        self.viewer_window.destroy()


class EditEventEditor:
    def __init__(self, root, event_date, events, save_callback, highlight_callback):
        self.root = root
        self.event_date = event_date
        self.events = events
        self.save_callback = save_callback
        self.highlight_callback = highlight_callback

        self.edit_window = tk.Toplevel(root)
        self.edit_window.title("Termin bearbeiten")

        self.edit_label = ttk.Label(self.edit_window, text="Termin bearbeiten:")
        self.edit_label.pack(padx=10, pady=5)

        self.edit_entry = ttk.Entry(self.edit_window)
        self.edit_entry.pack(padx=10, pady=5)

        save_button = ttk.Button(self.edit_window, text="Speichern", command=self.save_edited_event)
        save_button.pack(padx=10, pady=5)

    def save_edited_event(self):
        new_event = self.edit_entry.get()
        if new_event:
            self.events[self.event_date] = [new_event]
            self.save_callback()
            self.highlight_callback()
            self.edit_window.destroy()
            messagebox.showinfo("Erfolg", "Termin bearbeitet.")
        else:
            messagebox.showerror("Fehler", "Bitte geben Sie den bearbeiteten Termin ein.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.protocol("WM_DELETE_WINDOW", app.save_events)
    root.mainloop()
