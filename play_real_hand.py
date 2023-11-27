from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import keyboard
factory = PiGPIOFactory(host='10.10.4.161')

move_cloth = LED(4, pin_factory=factory)
# move_hand = LED(15, pin_factory=factory)
# catch = LED(14, pin_factory=factory)


#backwards
# move_hand.off()

#forward
# move_hand.on()

#open hand
# catch.on()

#close hand
# catch.off()

while True:
    move_cloth.on()
    sleep(1)
    move_cloth.off()
    sleep(10)
    # if keyboard.is_pressed('up'):
    #     #forward
    #     move_hand.on()    
    #     sleep(0.1)
    # elif keyboard.is_pressed('down'):
    #     move_hand.off()
    #     sleep(0.1)
    # elif keyboard.is_pressed('c'):
    #     catch.off()
    #     sleep(0.1)
    # elif keyboard.is_pressed('r'):
    #     catch.on()
    #     sleep(0.1)

