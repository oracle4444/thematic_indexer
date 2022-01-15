import torch
import cv2
import sys
import numpy

from .sort import *
from .models import Classes, Instances, Videos

class Detector:
    def __init__(self, repo_or_dir='yolov5', model='yolov5s', source='local'):
        self.model = torch.hub.load(repo_or_dir=repo_or_dir, model=model, source=source)  # if already downloaded
        self.mot_tracker = Sort()
        self.updateNameIds()

    def updateNameIds(self):
        counter = 0
        for name in self.model.names:
            cl = Classes(pk=counter, name=name)
            cl.save()
            counter += 1

    def drawBox(self, img, x1, y1, x2, y2, text, color):
        start = x1, y1
        end = x2, y2
        width = 4
        img = cv2.rectangle(img, start, end, color, width)

        start = x1, y1 - 10
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 1
        img = cv2.putText(img, text, start, font, font_size, color, width)
        return img

    def processFrame(self, frame, currentVideoPos, input_file):
        result = self.model(frame)
        dets = result.xyxy[0]
        for d in dets:
            d[4] = d[4] * 100

        trackers = self.mot_tracker.update(dets)

        video = input_file.split('/')[-1]
        video = Videos.objects.get(name=video)

        color = (0, 255, 0)

        for d in trackers:
            d = d.astype(np.int32)
            track_number = d[4]
            class_id = d[5]
            name = result.names[class_id]


            try:
                instance = Instances.objects.get(video_id=video.id, class_id=class_id, track_number=track_number)

            except Instances.DoesNotExist:
                instance = Instances(video_id=video.id, class_id=class_id, first_frame=currentVideoPos,
                                     last_frame=currentVideoPos, track_number=track_number)
                instance.save()
                poster_name = 'detector/static/detector/posters/{}.png'.format(instance.pk)
                poster = self.drawBox(numpy.copy(frame), d[0], d[1], d[2], d[3], name, color)
                new_size = (poster.shape[1] // 4, poster.shape[0] // 4)
                poster = cv2.resize(poster, new_size)
                cv2.imwrite(poster_name, poster)

            else:
                instance.last_frame = currentVideoPos
                instance.save()

    def detect(self, input_file):
        cap = cv2.VideoCapture(input_file)

        counter = 0
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                counter += 1
                # currentVideoPos = int(cap.get(cv2.CAP_PROP_POS_MSEC))
                currentVideoPos = counter
                self.processFrame(frame, currentVideoPos, input_file)

            # Важен порядок освобождения
        except:
            print('Exception: %s', sys.exc_info()[0])
        cap.release()

