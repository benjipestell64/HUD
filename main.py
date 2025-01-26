import obd
import tkinter as tk
from tkinter import Label

# Connect to OBD-II scanner
connection = obd.OBD()  # Auto-connects to Bluetooth OBD-II scanner

# Create the main window
root = tk.Tk()
root.title("Car HUD")
root.attributes('-fullscreen', False)
root.configure(bg='black')

# Labels to display speed and coolant temperature
speed_label = Label(root, text="Speed: -- km/h", font=("Arial", 48), fg="white", bg="black")
speed_label.pack(pady=50)

temp_label = Label(root, text="Coolant Temp: -- °C", font=("Arial", 48), fg="white", bg="black")
temp_label.pack(pady=50)


# Function to update speed and temperature
def update_values():
    if connection.is_connected():
        speed = connection.query(obd.commands.SPEED)
        temp = connection.query(obd.commands.COOLANT_TEMP)

        if speed.value:
            speed_label.config(text=f"Speed: {speed.value.to('km/h')}")

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
