# for a 48mm wide tape, 
# for the right side of the tape connect the sensors  9, 10 and 11 (or 8, 10 and 12) of the QTRX to pins 4, 5 and 6 of the arduino
# for the left side of the tape connect the sensors  21, 22, and 23 (or 20, 22 and 24) of the QTRX to pins 7, 8 and 9 of the arduino
# connect the sensors 1 and 31 to pins 3 and 10 of the arduino


import serial
import serial.tools.list_ports  


line_loss_threshold = 1500 # depends on conditions (scotch/ground color)



Data = serial.Serial("/dev/ttyACM0", 9600)


def read_line():
    """
        returns an array containing the values returned by each of the 8 connected sensors
    """
    line = Data.readline().decode('utf-8')
    line = line.split()
       
    for i in range (len(line)) :
        line[i] = float(line[i])
    #print(line)
    return line

line_right = 0
line_left = 0
loose_right = 0
loose_left = 0

def intensity():
    """
        returns the average of the intensity measured by the sensors on the left and right of the tape, 
        as well as the intensity measured by the sensors on the left and right end of the sensor bar
    """
    line = read_line(line_left, line_right, loose_left, loose_right)
    if len(line) == 9 :       # allows to avoid some reading errors
        line_left = line[4]+2*line[5]+line[6]
        line_right = line[1]+2*line[2]+line[3]
        loose_left = line[7]
        loose_right = line[0]
    return line_left, line_right, loose_left, loose_right



def run():
    line_left, line_right, loose_left, loose_right = intensity(line_left, line_right, loose_left, loose_right)
    dif = line_right - line_left
    add = line_right + line_left

    if (add > line_loss_threshold) & (dif > 0) : # allows you to know if you have not lost the line of sight
        print ("Go right", dif, line_left, line_right, add)
    elif (add > line_loss_threshold) & (dif < 0) : 
        print ("Go left", dif, line_left, line_right, add)
    
    elif (add < line_loss_threshold) & (loose_left > loose_right): # if the line is lost
        print ("Lost line, go left")
    elif (add < line_loss_threshold) & (loose_left < loose_right):
        print ("Lost line, go right")



while True :
    run()


Data.close() 