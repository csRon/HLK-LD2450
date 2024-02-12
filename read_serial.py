import serial

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

# test communication with example from documentation

# hex_string = "AA FF 03 00 0E 03 B1 86 10 00 68 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 55 CC"

# # Remove spaces from the hex string
# hex_string = hex_string.replace(" ", "")

# # Convert the hex string to bytes
# data = bytes.fromhex(hex_string)

# print(data)# Check if the frame header and tail are present

# if b'\xAA\xFF\x03\x00' in data and b'\x55\xCC' in data:
#     # Extract the objective information
#     objective_data = data.split(b'\xAA\xFF\x03\x00')[1].split(b'\x55\xCC')[0]
#     print(objective_data)
#     # Interpret all three objectives
#     target1_data = objective_data[0:8]
#     target2_data = objective_data[8:16]
#     target3_data = objective_data[16:24]

#     # Interpret information for each target
#     target1_x, target1_y, target1_speed, target1_distance_resolution = interpret_target(target1_data)

#     # Print the interpreted information for all targets
#     print(f'Target 1 x-coordinate: {target1_x} mm')
#     print(f'Target 1 y-coordinate: {target1_y} mm')
#     print(f'Target 1 speed: {target1_speed} cm/s')
#     print(f'Target 1 distance: {target1_distance_resolution} mm')

# Open the serial port
ser = serial.Serial('/dev/ttyUSB0', 256000, timeout=1)

try:
    while True:
        # Read a line from the serial port
        data = ser.read_until(b'\xCC')

        # print(data)

        # Check if the frame header and tail are present
        if b'\xAA\xFF\x03\x00' in data and b'\x55\xCC' in data:
            # Extract the objective information
            objective_data = data.split(b'\xAA\xFF\x03\x00')[1].split(b'\x55\xCC')[0]
            
            # Interpret all three objectives
            target1_data = objective_data[0:8]
            target2_data = objective_data[8:16]
            target3_data = objective_data[16:24]

            print(target1_data)

            # convert objective data to bitstream string
            bits_objective_data = ''.join(format(byte, '08b') for byte in target1_data) 
            print(bits_objective_data)

            # Interpret information for each target
            target1_x, target1_y, target1_speed, target1_distance_res = interpret_target(target1_data)
            target2_x, target2_y, target2_speed, _ = interpret_target(target2_data)
            target3_x, target3_y, target3_speed, _ = interpret_target(target3_data)

            # Print the interpreted information for all targets
            print(f'Target 1 x-coordinate: {target1_x} mm')
            print(f'Target 1 y-coordinate: {target1_y} mm')
            print(f'Target 1 speed: {target1_speed} cm/s')
            print(f'Target 1 distance: {target1_distance_res} mm')

            print(f'Target 2 x-coordinate: {target2_x} mm')
            print(f'Target 2 y-coordinate: {target2_y} mm')
            print(f'Target 2 speed: {target2_speed} cm/s')

            print(f'Target 3 x-coordinate: {target3_x} mm')
            print(f'Target 3 y-coordinate: {target3_y} mm')
            print(f'Target 3 speed: {target3_speed} cm/s')

            print('-' * 30)

except KeyboardInterrupt:
    # Close the serial port on keyboard interrupt
    ser.close()
    print("Serial port closed.")