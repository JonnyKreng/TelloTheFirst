import tello
import time
import threading
import cv2

def picture(reader, tello):
    while True:
        cv2.imshow("Window", reader.frame)
        k = cv2.waitKey(1) & 0xFF
        # press 'q' to exit
        if k == ord(' '):
            tello.send_rc_control(round(0), round(0), round(0), round(0))
            print("Exiting")
            exit()


def telloInit(tello):
    if not tello.connect():
        print("Tello not connected")
        exit()
    if not tello.set_speed(100):
        print("Not set speed to lowest possible")
        exit()
    # In case streaming is on. This happens when we quit this program without the escape key.
    if not tello.streamoff():
        print("Could not stop video stream")
    if not tello.streamon():
        print("Could not start video stream")
        exit()
    time.sleep(0.5)


drone = tello.Tello()

telloInit(drone)

reader = drone.get_frame_read()

thread = threading.Thread(target=picture, args=(reader,drone,))
thread.start()

print(drone.get_battery())

drone.takeoff()
time.sleep(3)


#left_right_velocity, for_back_velocity, up_down_velocity, yaw_velocity
drone.send_rc_control(round(100), round(0), round(0), round(0))

time.sleep(1)

drone.land()

print('Flight time: %s' % drone.get_flight_time())

drone.end()