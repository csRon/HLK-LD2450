import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import queue

def interpret_target(target_data):
    x = int.from_bytes(target_data[0:2], byteorder='little', signed=True)
    y = int.from_bytes(target_data[2:4], byteorder='little', signed=True)     
    speed = int.from_bytes(target_data[4:6], byteorder='little', signed=True)
    distance_resolution = int.from_bytes(target_data[6:8], byteorder='little', signed=False)
    
    # substract 2^15 depending if negative or positive
    x = x if x >= 0 else -2**15 - x
    y = y if y >= 0 else -2**15 - y
    speed = speed if speed >= 0 else -2**15 - speed

    return x, y, speed, distance_resolution

def serial_reader():
    ser = serial.Serial('/dev/ttyUSB0', 256000, timeout=1)
    while True:
        data = ser.read_until(b'\xCC')
        data_queue.put(data)
   
def update_plot(frame):
    # Check if there is data in the queue
    while not data_queue.empty():
        data = data_queue.get()

        # Check if the frame header and tail are present
        if b'\xAA\xFF\x03\x00' in data and b'\x55\xCC' in data:
            # Extract the objective information
            objective_data = data.split(b'\xAA\xFF\x03\x00')[1].split(b'\x55\xCC')[0]

            # Interpret information for each target
            target1_data = objective_data[0:8]
            target2_data = objective_data[8:16]
            target3_data = objective_data[16:24]

            # Interpret information for each target
            target1_x, target1_y, target1_speed, _ = interpret_target(target1_data)
            target2_x, target2_y, target2_speed, _ = interpret_target(target2_data)
            target3_x, target3_y, target3_speed, _ = interpret_target(target3_data)      

            # current targets
            current_targets_x = [target1_x, target2_x, target3_x]
            current_targets_y = [target1_y, target2_y, target3_y]

            # Update target lists with current targets --> all timesteps are stored
            # targets_x.extend(current_targets_x)
            # targets_y.extend(current_targets_y)

            # Update the scatter plot
            sc.set_offsets(list(zip(current_targets_x, current_targets_y)))

    return sc,

# Create a thread-safe queue to communicate between threads
data_queue = queue.Queue()

# Create and start the serial reader thread
serial_thread = threading.Thread(target=serial_reader)
serial_thread.daemon = True
serial_thread.start()

# Initialize empty lists to store all target information 
targets_x = []
targets_y = []

# Set up the plot
fig, ax = plt.subplots()
sc = ax.scatter(targets_x, targets_y)
ax.set_xlim(-1000, 1000)  # Adjust the limits based on your scenario
ax.set_ylim(-6000, 0)

# Create an animation
ani = FuncAnimation(fig, update_plot, blit=True)

plt.xlabel('x [mm]')
plt.ylabel('y [mm]')
plt.grid()
plt.show()


