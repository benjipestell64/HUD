import obd
import tkinter as tk
from tkinter import Label, Canvas

# Connect to OBD-II scanner
connection = obd.OBD()  # Auto-connects to Bluetooth OBD-II scanner

# Create the main window
root = tk.Tk()
root.title("Car HUD")
root.attributes('-fullscreen', False)
root.configure(bg='black')

# Labels to display speed, coolant temperature, and gear
speed_label = Label(root, text="Speed: -- MPH", font=("Arial", 48), fg="white", bg="black")
speed_label.pack(pady=20)

rpm_label = Label(root, text="RPM: --", font=("Arial", 48), fg="white", bg="black")
rpm_label.pack(pady=20)

gear_label = Label(root, text="Gear: --", font=("Arial", 48), fg="white", bg="black")
gear_label.pack(pady=20)

temp_label = Label(root, text="Coolant Temp: -- °C", font=("Arial", 24), fg="white", bg="black")
temp_label.pack(pady=20)

# Create RPM dial gauge
canvas = Canvas(root, width=400, height=400, bg='black', highlightthickness=0)
canvas.pack()

# Function to update speed, temperature, RPM, and gear
def update_values():
    if connection.is_connected():
        speed = connection.query(obd.commands.SPEED)
        temp = connection.query(obd.commands.COOLANT_TEMP)
        rpm = connection.query(obd.commands.RPM)
        gear = connection.query(obd.commands.GEAR)

        if speed.value:
            speed_label.config(text=f"Speed: {speed.value.to('mph')}")

        if rpm.value:
            rpm_label.config(text=f"RPM: {int(rpm.value.magnitude)}")

        if gear.value:
            gear_label.config(text=f"Gear: {int(gear.value.magnitude)}")

        if temp.value:
            temp_label.config(text=f"Coolant Temp: {temp.value.to('celsius')} °C")

    root.after(50, update_values)  # Update every second


# Exit on keypress
def exit_fullscreen(event):
    root.attributes('-fullscreen', False)
    root.quit()


root.bind("<Escape>", exit_fullscreen)

update_values()
root.mainloop()
