import PyTrinamic, time
from PyTrinamic.connections.ConnectionManager import ConnectionManager
from TMCM_2631 import TMCM_2631

PyTrinamic.showInfo()

myInterface = ConnectionManager("--interface kvaser_tmcl").connect()

module = TMCM_2631(myInterface)
module.showModuleInfo()
motor = module.motor(0)

#Motor configuration
motor.setMaxTorque(2500)
motor.setMotorPolePairs(3)
motor.showConfiguration()

#open loop configuration
motor.openLoop.showConfiguration()

#Show motion settings
motor.linearRamp.showConfiguration()

#Set communication mode to OpenLoop
motor.commutationSelection.setMode(motor.ENUM.COMM_MODE_OPENLOOP)
motor.commutationSelection.showConfiguration()

#Launch wheel in OpenLoop
print("Starting motor...")
motor.rotate(2000)
time.sleep(3)

print("Changing motor direction...")
motor.rotate(-2000)
time.sleep(6)

print("Stopping motor...")
motor.rotate(2000)
time.sleep(3)

myInterface.close()
print("\nReady.")

#There is a problem in the program. The wheel turns well during the 'motor.rotate(2000)' line 30 but only as a short impulse. 
#Then the wheel does not turn anymore. 
