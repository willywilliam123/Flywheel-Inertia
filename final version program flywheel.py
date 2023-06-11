import csv
from decimal import Decimal, DecimalException
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
import pyperclip

calculate_window = None
# Global variables to store the input values
time_of_lift_value = ""
radius_of_shaft_value = ""
inertia_value = ""

# Function to handle the "Browse file" button click event
def browse_file():
    filename = filedialog.askopenfilename(title="Select a CSV file", filetypes=[("CSV Files", "*.csv")])
    if filename:
        entry_filepath.delete(0, tk.END)
        entry_filepath.insert(tk.END, filename)

# Function to handle the "Calculate Min Max Average" button click event
def calculate_stats():
    # Get the file path from the entry field
    filepath = entry_filepath.get()
    global calculate_window  # Access the global calculate_window variable
    calculate_window = tk.Toplevel(window)
    calculate_window.title("Calculate")
    calculate_window.geometry("300x100")
    
    def copy_min_to_clipboard():
        pyperclip.copy(str(min_value))

    def copy_max_to_clipboard():
        pyperclip.copy(str(max_value))

    def copy_avg_to_clipboard():
        pyperclip.copy(str(average))

    button_copy_min = tk.Button(calculate_window, text="Copy Min to Clipboard", command=copy_min_to_clipboard)
    button_copy_min.pack()

    button_copy_max = tk.Button(calculate_window, text="Copy Max to Clipboard", command=copy_max_to_clipboard)
    button_copy_max.pack()

    button_copy_avg = tk.Button(calculate_window, text="Copy Average to Clipboard", command=copy_avg_to_clipboard)
    button_copy_avg.pack()

    try:
        # Open the CSV file
        with open(filepath, 'r') as file:
            # Read the CSV data
            csv_data = csv.reader(file)

            # Convert the CSV data to a list
            rows = list(csv_data)

        # Check if the first row contains text or letters
        if any(any(c.isalpha() for c in row) for row in rows[:1]):
            # Remove the first row
            rows = rows[1:]

        # Initialize the minimum, maximum, and sum variables with appropriate initial values
        min_value = Decimal('Infinity')
        max_value = Decimal('-Infinity')
        sum_values = Decimal(0)
        count = 0

        # Search for the minimum, maximum, and sum of values in the second column (index 1)
        for row in rows:
            try:
                value = Decimal(row[1])
                min_value = min(min_value, value)
                max_value = max(max_value, value)
                sum_values += value
                count += 1
            except (ValueError, DecimalException):
                continue

        # Calculate the average value
        if count > 0:
            average = sum_values / count
        else:
            average = Decimal(0)

        # Display the minimum, maximum, and average values
        messagebox.showinfo("CSV Statistics", f"Minimum value: {min_value}\nMaximum value: {max_value}\nAverage value: {average}")

    except FileNotFoundError:
        messagebox.showerror("Error", "File not found. Please select a valid CSV file.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to handle the "Set Parameters" button click event
def open_forces_window():
    forces_window = tk.Toplevel(window)
    forces_window.title("Set Parameters")

    def open_time_of_lift_window():
        time_of_lift_window = tk.Toplevel(forces_window)
        time_of_lift_window.title("Time of the Lift")

        def save_time_of_lift():
            global time_of_lift_value
            time_of_lift_value = entry_time_of_lift.get()
            time_of_lift_window.destroy()
            update_button_colors()

        entry_time_of_lift = tk.Entry(time_of_lift_window, width=20)
        entry_time_of_lift.pack()

        button_save = tk.Button(time_of_lift_window, text="Save", command=save_time_of_lift)
        button_save.pack()

    def open_radius_of_shaft_window():
        radius_of_shaft_window = tk.Toplevel(forces_window)
        radius_of_shaft_window.title("Radius of the Shaft")

        def save_radius_of_shaft():
            global radius_of_shaft_value
            radius_of_shaft_value = entry_radius_of_shaft.get()
            radius_of_shaft_window.destroy()
            update_button_colors()

        entry_radius_of_shaft = tk.Entry(radius_of_shaft_window, width=20)
        entry_radius_of_shaft.pack()

        button_save = tk.Button(radius_of_shaft_window, text="Save", command=save_radius_of_shaft)
        button_save.pack()

    def update_button_colors():
        if time_of_lift_value:
            button_time_of_lift.config(text=f"Time of the Lift: {time_of_lift_value}", bg="green")
        if radius_of_shaft_value:
            button_radius_of_shaft.config(text=f"Radius of the Shaft: {radius_of_shaft_value}", bg="green")
        if time_of_lift_value and radius_of_shaft_value:
            button_forces.config(bg="green")

    button_time_of_lift = tk.Button(forces_window, text="Time of the Lift", command=open_time_of_lift_window)
    button_time_of_lift.pack(side=tk.LEFT)

    button_radius_of_shaft = tk.Button(forces_window, text="Radius of the Shaft", command=open_radius_of_shaft_window)
    button_radius_of_shaft.pack(side=tk.LEFT)

    update_button_colors()



# Function to handle the "Select Inertia" button click event
def open_inertia_window():
    inertia_window = tk.Toplevel(window)
    inertia_window.title("Select Inertia")

    def save_inertia():
        global inertia_value
        inertia_value = entry_inertia.get()
        inertia_window.destroy()
        button_inertia.config(text=f"Inertia: {inertia_value}", bg="green")

    entry_inertia = tk.Entry(inertia_window, width=20)
    entry_inertia.pack()

    button_save = tk.Button(inertia_window, text="Save", command=save_inertia)
    button_save.pack()

def open_rope_linear_speed_window():
    # Function to open the Select Rope Linear Speed window
    def save_rope_linear_speed():
        global rope_linear_speed_value
        rope_linear_speed_value = entry_rope_linear_speed.get()
        rope_linear_speed_window.destroy()
        button_rope_linear_speed.config(text=f"Rope Linear Speed: {rope_linear_speed_value}", bg="green")

    rope_linear_speed_window = tk.Toplevel(window)
    rope_linear_speed_window.title("Select Rope Linear Speed")

    entry_rope_linear_speed = tk.Entry(rope_linear_speed_window, width=20)
    entry_rope_linear_speed.pack()

    button_save = tk.Button(rope_linear_speed_window, text="Save", command=save_rope_linear_speed)
    button_save.pack()

def open_calculate_window():
    try:
        inertia = float(inertia_value)
        rope_linear_speed = float(rope_linear_speed_value)
        radius_of_shaft = float(radius_of_shaft_value)
        time_of_lift = float(time_of_lift_value)

        force = (inertia * (rope_linear_speed / (radius_of_shaft * time_of_lift))) / radius_of_shaft
        weightload = force / 9.81

        calculate_window = tk.Toplevel(window)
        calculate_window.title("Calculate")
        calculate_window.geometry("300x100")

        label_force = tk.Label(calculate_window, text=f"Force = {force}")
        label_force.pack()

        label_weightload = tk.Label(calculate_window, text=f"Weightload = {weightload} kg")
        label_weightload.pack()
    except ValueError:
        pass

# Create the main window
window = tk.Tk()
window.title("Flywheel force and load calculator")
window.geometry("400x200")

# Create the file path entry field
label_filepath = tk.Label(window, text="CSV File Path:")
label_filepath.pack()

entry_filepath = tk.Entry(window, width=40)
entry_filepath.pack()

# Create the Browse file button
button_browse = tk.Button(window, text="Browse file", command=browse_file)
button_browse.pack()

# Create the Calculate Min Max Average button
button_calculate = tk.Button(window, text="Calculate Min Max Average", command=calculate_stats)
button_calculate.pack()

# Create the Set Parameters button
button_forces = tk.Button(window, text="Set Parameters", command=open_forces_window)
button_forces.pack()

# Store the initial color of the "Set Parameters" button
button_forces_initial_color = button_forces.cget('bg')
# Create the Select Inertia button
button_inertia = tk.Button(window, text="Select Inertia", command=open_inertia_window)
button_inertia.pack()

rope_linear_speed_value = ""
button_rope_linear_speed = tk.Button(window, text="Select Rope Linear Speed", command=open_rope_linear_speed_window)
button_rope_linear_speed.pack()


# Create the Calculate button
button_calculate_final = tk.Button(window, text="Calculate", command=open_calculate_window)
button_calculate_final.pack()

# Start the GUI event loop
window.mainloop()

# After the GUI event loop exits, display the values
print("Time of the Lift:", time_of_lift_value)
print("Radius of the Shaft:", radius_of_shaft_value)
print("Inertia:", inertia_value)
