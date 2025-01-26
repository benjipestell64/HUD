import obd
import tkinter as tk
from tkinter import Label, Canvas
import math

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

temp_label = Label(root, text="Coolant Temp: -- °C", font=("Arial", 48), fg="white", bg="black")
temp_label.pack(pady=20)

gear_label = Label(root, text="Gear: --", font=("Arial", 48), fg="white", bg="black")
gear_label.pack(pady=20)

# Create RPM dial gauge
canvas = Canvas(root, width=400, height=400, bg='black', highlightthickness=0)
canvas.pack()


# Function to draw the RPM dial
def draw_rpm_dial(rpm):
    canvas.delete("all")
    center_x, center_y = 200, 200
    radius = 150
    angle = (rpm / 8000.0) * 180  # Scale RPM (assuming max 8000 RPM)
    angle_rad = math.radians(180 - angle)
    needle_x = center_x + radius * math.cos(angle_rad)
    needle_y = center_y - radius * math.sin(angle_rad)
    canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, outline="white",
                       width=5)
    canvas.create_line(center_x, center_y, needle_x, needle_y, fill="red", width=5)
    canvas.create_text(center_x, center_y + radius + 20, text=f"RPM: {rpm}", font=("Arial", 24), fill="white")


# Function to update speed, temperature, RPM, and gear
def update_values():
    if connection.is_connected():
        speed = connection.query(obd.commands.SPEED)
        temp = connection.query(obd.commands.COOLANT_TEMP)
        rpm = connection.query(obd.commands.RPM)
        gear = connection.query(obd.commands.GEAR)

        if speed.value:
            speed_label.config(text=f"Speed: {speed.value.to('mph')}")

        if temp.value:
            temp_label.config(text=f"Coolant Temp: {temp.value.to('celsius')} °C")

        if rpm.value:
            draw_rpm_dial(int(rpm.value.magnitude))

        if gear.value:
            gear_label.config(text=f"Gear: {int(gear.value.magnitude)}")

    root.after(50, update_values)  # Update every second


# Exit on keypress
def exit_fullscreen(event):
    root.attributes('-fullscreen', False)
    root.quit()


root.bind("<Escape>", exit_fullscreen)

update_values()
root.mainloop()
