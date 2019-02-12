import  FaceDetector
import cv2
import tello
import threading
import time
import imutils

test = False

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


def picture(reader, tello, det):
    while True:
        timer = time.time()

        if test:
            ret, img = reader.read()
            img = imutils.resize(img, int(1920 / 2), int(1080 / 2))
        else:
            img = reader.frame

        x, y, s, img = det.findTrackCenter(img)
        calcDroneMovement(x, y, s, tello)

        ##Display the Drones Picture witzh meta informations
        img = cv2.putText(img, str(round(1/(time.time()-timer)))+" fps", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
        cv2.imshow("Window", img)
        k = cv2.waitKey(1) & 0xFF
        # press 'q' to exit
        if k == ord(' '):
            tello.send_rc_control(0, 0, 0, 0)
            tello.land()
            tello.end()
            print("Exiting")
            exit()

def calcDroneMovement(x, y, s, tello):
    size = 8

    #left_right_velocity, for_back_velocity, up_down_velocity, yaw_velocity
    if s == -1:
        s = size

    print(round(x/10), -(round(s-size)*4), round(y/5), round(x/4))

    if not test:
        tello.send_rc_control(round(x/10), -(round(s-size)*4), round(y/5), round(x/4))


det = FaceDetector.CenterFace()
det.addBox = True

if test:
    picture(cv2.VideoCapture(0), None, det)
else:
    drone = tello.Tello()
    telloInit(drone)

    print(drone.get_battery())
    drone.takeoff()
    drone.move_up(100)
    time.sleep(4)
    drone.flip_forward()

    reader = drone.get_frame_read()
    thread = threading.Thread(target=picture, args=(reader, drone, det))
    thread.start()


