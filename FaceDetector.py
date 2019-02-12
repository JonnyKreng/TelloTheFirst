import cv2


class CenterFace:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
        #self.eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
        self.tracker = cv2.TrackerKCF_create()
        self.addBox = False
        self.lost = True
        self.cycle = 0
        self.cycles = 30


    def setCycles(self,num):
        self.cycles = num


    def findFaces(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        if self.addBox:
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        return faces, img


    def setupTracker(self, img, bbox):
        self.tracker = cv2.TrackerMedianFlow_create()
        ok = self.tracker.init(img, tuple(bbox[0]))
        if not ok:
            exit()


    def trackFaces(self, img):
        ok, bbox = self.tracker.update(img)
        if not ok:
            return (), img

        if self.addBox:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(img, p1, p2, (0, 0, 255), 2, 1)

        return bbox, img


    def findTrackCenter(self, img):

        if self.lost or self.cycle > self.cycles:
            bbox, img = self.findFaces(img)
            if bbox == ():
                if self.cycle > self.cycles:
                    self.lost = False
                    self.cycle = 0
                    return self.findTrackCenter(img)
                else:
                    return 0, 0, -1, img
            self.lost = False
            self.setupTracker(img, bbox)
            self.cycle = 0
            bbox = int(bbox[0][0]), int(bbox[0][1]), int(bbox[0][2]), int(bbox[0][3])
        else:
            bbox, img = self.trackFaces(img)
            if bbox == ():
                self.lost = True
                return 0, 0, -1, img
            self.cycle += 1
            bbox = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])

        hight, widge, something = img.shape

        x, y, w, h = bbox

        center_x = x + int(w/2)
        center_y = y + int(h/2)
        if self.addBox:
            cv2.rectangle(img, (center_x - 5, center_y - 5), (center_x + 10, center_y + 10), (0, 0, 255), 2)

        #Calc Distance from Center
        adjust_x = int(center_x - (widge / 2))
        adjust_y = int((hight / 2) - center_y)

        #Calc Percentage of picture
        size = (w * h) / (widge * hight) * 100

        if self.addBox:
            cv2.rectangle(img, (int(widge / 2)-5, int(hight / 2)-5), (int(widge / 2) + 10, int(hight / 2) + 10), (0, 255, 0), 2)

        return adjust_x, adjust_y, size, img

    def centerFaces(self, img):
        hight, widge, something = img.shape

        faces, img = self.findFaces(img)

        adjust_y = 0
        adjust_x = 0
        size = 15

        for (x, y, w, h) in faces:
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            if self.addBox:
                cv2.rectangle(img, (center_x - 5, center_y - 5), (center_x + 10, center_y + 10), (0, 0, 255), 2)

            #Calc Distance from Center
            adjust_x = int(center_x - (widge / 2))
            adjust_y = int((hight / 2) - center_y)

            #Calc Percentage of picture
            size = (w * h) / (widge * hight) * 100

            if self.addBox:
                cv2.rectangle(img, (int(widge / 2)-5, int(hight / 2)-5), (int(widge / 2) + 10, int(hight / 2) + 10), (0, 255, 0), 2)

        return adjust_x, adjust_y, size, img

