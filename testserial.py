# Import the library
import serial

# Try to connect to the port
try:
    fabkit = serial.Serial('/dev/ttyAMA0', 9600)
except:
    print "Failed to connect"
    exit()

# Read data and print it to terminal... until you stop the program
while 1:
    line = fabkit.readline()
    print line

# We should close the connection... but since there's a while 1 loop before, we never reach this
fabkit.close()
