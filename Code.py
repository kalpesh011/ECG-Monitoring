import serial
import matplotlib.pyplot as plt
import numpy as np

# Initialize UART communication with the STM32
ser = serial.Serial('/dev/serial_device', baudrate=9600)

# Number of data points to display in the window
window_size = 1000  # Adjust the size as needed

def analyzeECG(ecg_data):
    
    # If the ECG value is above a threshold, consider it abnormal
    threshold = 1000
    is_normal = all(value < threshold for value in ecg_data)

    return is_normal

plt.ion()  # Turn on interactive mode to continuously update the plot

# Initialize the plot
fig, ax = plt.subplots()
ax.set_ylim(0, 4096)  # Adjust the y-axis limits as needed
line, = ax.plot([])
ecg_x = np.arange(window_size)
ecg_y = np.zeros(window_size)
line.set_data(ecg_x, ecg_y)

while True:
    # Read ECG data from STM32
    data = ser.read(2)  # Read 2 bytes of ECG data
    ecg_value = int.from_bytes(data, byteorder='big')  # Convert bytes to integer

    # Add ECG data to the list
    ecg_y = np.append(ecg_y, ecg_value)
    ecg_y = ecg_y[-window_size:]  # Keep only the latest data points

    # Update the plot
    line.set_data(ecg_x, ecg_y)

    # Implement ECG analysis to determine if it's normal or not
    is_normal = analyzeECG(ecg_y)

    # Display the result
    if is_normal:
        print("ECG is normal")
    else:
        print("ECG is abnormal")

    # Pause to allow time for the graph to update (adjust the duration as needed)
    plt.pause(0.01)
