import serial_protocol

import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import queue

def serial_reader():
    ser = serial.Serial('/dev/ttyUSB0', 256000, timeout=1)

    while True:
        data = ser.read_until(serial_protocol.report_tail)
        data_queue.put(data)
   
def update_plot(frame):
    # Check if there is data in the queue
    while not data_queue.empty():
        serial_protocol_line = data_queue.get()

        # Check if the frame header and tail are present
        if serial_protocol.report_header in serial_protocol_line and serial_protocol.report_tail in serial_protocol_line:
            # Extract the target values
            all_target_values = serial_protocol.read_radar_data(serial_protocol_line)    
            
            if all_target_values is None:
                continue

            target1_x, target1_y, target1_speed, target1_distance_res, \
            target2_x, target2_y, target2_speed, target2_distance_res, \
            target3_x, target3_y, target3_speed, target3_distance_res \
                = all_target_values

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


