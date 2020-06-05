# Import the necessary packages which will be used in the program
import argparse
import os
import time
import math
import tkinter as Tk
from datetime import datetime
from pathlib import Path
from threading import Thread

import imutils
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import playsound
from cv2 import cv2
from imutils import face_utils
from imutils.video import VideoStream
from PIL import Image, ImageTk
from plyer import notification
from scipy.spatial import distance as dist

import dlib

LARGE_FONT = ("Verdana", 12)
PARENT_PATH = Path(__file__).parent.resolve()


class EyeTinker(Tk.Tk):

    def __init__(self, *args, **kwargs):
        Tk.Tk.__init__(self, *args, **kwargs)
        main_container = Tk.Frame(self)

        main_container.pack(side="top", fill="both", expand=True)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        displayFrame = ImageFrame(main_container, self)
        displayFrame.grid(row=0, column=0, sticky="nsew", padx=10, pady=2)
        self.frames[ImageFrame] = displayFrame

        sliderFrame = SettingsFrame(
            main_container, self, width=600, height=100)
        sliderFrame.grid(row=600, column=0, padx=10, pady=2)
        sliderFrame.submit_btn.configure(
            text="Start", command=lambda: sliderFrame.get_values(displayFrame.start_classifier))
        self.frames[SettingsFrame] = sliderFrame
        self.show_frame(ImageFrame)
        displayFrame.show_cv_frame(self.on_close)

        self.protocol("WM_DELETE_WINDOW", displayFrame.stop_streaming)
    def on_close(self):
        try:
            self.destroy()
            self.quit()
        except Exception as e:
            print(e)
            exit()
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class SettingsFrame(Tk.Frame):

    def __init__(self, parent, controller, width, height):
        Tk.Frame.__init__(self, parent, width=width, height=height)
        Tk.Label(self, text='Strain Time (seconds)').grid(row=0)
        Tk.Label(self, text='Strain Interval').grid(row=1)
        Tk.Label(self, text='Drowsiness Time (seconds)').grid(row=2)
        Tk.Label(self, text='Countdown Time (mins)').grid(row=3)
        self.submit_btn = Tk.Button(self, text='Okay')
        self.submit_btn.grid(row=6, column=1)
        # eyeFrames
        self.eye_values = Tk.Entry(self)
        self.eye_values.grid(row=0, column=1)
        self.eye_values.insert(0, '1')
        # straincountervalue
        self.strain_value = Tk.Entry(self)
        self.strain_value.grid(row=1, column=1)
        self.strain_value.insert(0, '1')
        # drowsyframes
        self.drowsy_value = Tk.Entry(self)
        self.drowsy_value.grid(row=2, column=1)
        self.drowsy_value.insert(0, '1')
        # timercount
        self.timer_value = Tk.Entry(self)
        self.timer_value.grid(row=3, column=1)
        self.timer_value.insert(0, '1')

        self.settings = CounterSettings()
        self.tracker = Tracker()

    def get_values(self, callback):
        self.settings.update_settings(
            eye_frames=self.eye_values.get(),
            strain_value=self.strain_value.get(),
            drowsy_frames=self.drowsy_value.get(),
            timer_count=self.timer_value.get())
        self.tracker.set_strain_threshold(self.strain_value.get())
        self.tracker.store_timer(self.timer_value.get())
        callback(self.settings, self.tracker)


class ImageFrame(Tk.Frame):
    font = cv2.FONT_HERSHEY_SIMPLEX

    def __init__(self, parent, controller):
        Tk.Frame.__init__(self, parent)
        label = Tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.parent = parent
        self.parent_path = Path(__file__).parent.resolve()
        self.path_to_shape_predictor = os.path.join(
            self.parent_path, "shape_predictor_68_face_landmarks.dat")
        # Graphics window
        self.cap = cv2.VideoCapture(0)
        # Capture video frames
        self.lmain = Tk.Label(self)
        self.lmain.pack(side="left", fill="both", expand=True)

        self.classify = False

        self.settings = CounterSettings()
        self.tracker = Tracker()
        self.stop = False
        self.fps = 20

    def stop_streaming(self):
        self.stop = True

    def show_cv_frame(self, callback):
        if self.stop:
            self.tracker.save_arrays()
            self.cap.release()
            print("[INFO] Shutting down...")
            try:
                callback()
            except Exception as e:
                print(e)
                exit()
        else:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                height, width, channels = frame.shape
                if not self.classify:
                    cv2.putText(frame, '{}'.format("CLASSIFIER OFF"),
                                (25, height-25), self.font, 1, (255, 0, 255), 2, cv2.LINE_AA)
                else:
                    frame = self.process_frame(frame, height)
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.lmain.imgtk = imgtk
                self.lmain.configure(image=imgtk)
                # self.after(30, self.show_cv_frame(cap))
                self.lmain.after(10, self.show_cv_frame, callback)

    def process_frame(self, frame, height):
        cv2.putText(frame, '{}'.format("CLASSIFIER ON"),
                    (25, height-25), self.font, 1, (255, 0, 255), 2, cv2.LINE_AA)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = self.detector(gray, 0)
        if not self.detect_away(rects):
            for rect in rects:
                shape = self.predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
                ear = self.draw_eyes_loc_ear(shape, frame)
                if ear > self.settings.EYES_OPEN_THRESHOLD:
                    cv2.putText(frame, "Eyes are open", (200, 390),
                                self.font, 0.7, (0, 0, 255), 2)
                else:
                    cv2.putText(frame, "Eyes are close", (200, 390),
                                self.font, 0.7, (0, 0, 255), 2)
                self.determine_strain(ear)
                self.determine_drowsy(ear)
        self.add_info(frame)
        return frame

    def detect_away(self, rects):
        if len(rects) == 0:
            if self.tracker.AWAY:
                self.tracker.AWAY_COUNT += 1
                if self.tracker.AWAY_COUNT == self.tracker.AWAY_CONSEC_FRAMES:
                    self.tracker.TIMER_RESET = True
                    if not self.stop:
                        try:
                            readable_time = self.convert_frames_to_minutes_seconds(self.tracker.AWAY_CONSEC_FRAMES)
                            notification.notify(
                                message=f'No face detected for {readable_time}',
                                title='No face detected',
                                app_icon=None)

                        except Exception as e:
                            print(str(e))
            else:
                self.tracker.AWAY = True
                self.tracker.AWAY_COUNT += 1
            return True
        else:
            self.tracker.AWAY = False
            self.tracker.reset_away_count()
            if self.tracker.TIMER_RESET == True:
                self.tracker.reset_timer
            return False

    def add_info(self, frame):
        self.settings.TIMER_COUNTDOWN -= 1  # 100 = 10secs
        if self.settings.TIMER_COUNTDOWN == 0:
            notification.notify(
                title='ALERT', message='Please take a break', app_icon=None, timeout=10,)
        now = datetime.now()
        time_now = f'Time: {now.strftime("%H:%M:%S")}'
        # Display the time on the screen
        cv2.putText(frame, time_now, (0, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Display the drowsiness counter on the screen
        cv2.putText(frame, "DROWSINESS COUNTER: {:d}".format(
            self.tracker.TOTAL_DROWSY), (225, 20), self.font, 0.7, (0, 0, 255), 2)

        # Display the strain counter on the screen
        cv2.putText(frame, "STRAIN LIMIT: {:d}".format(
            self.tracker.TOTAL_STRAIN), (290, 40), self.font, 0.7, (0, 0, 255), 2)

        readable_time = self.convert_frames_to_minutes_seconds(
            self.settings.TIMER_COUNTDOWN)
        # Display the EAR on the screen
        cv2.putText(frame, f"TIMER: {readable_time}",
                    (100, 60), self.font, 0.7, (0, 0, 255), 2)

    def convert_frames_to_minutes_seconds(self, frames):
        """[summary]

        Args:
            frames (integer): frames to convert

        Returns:
            [str]: [readable time in min and seconds]
        """
        total_seconds = math.ceil(frames/self.fps)
        minute, seconds = divmod(total_seconds, 60)
        return (f'{minute:02d}min {seconds:02d}s')

    def draw_eyes_loc_ear(self, shape, frame):
        leftEye = shape[self.left_eye['Start']:self.left_eye['End']]
        rightEye = shape[self.right_eye['Start']:self.right_eye['End']]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        ear = (leftEAR + rightEAR) / 2.0

        # Display the EAR on the screen
        cv2.putText(frame, "EAR: {:.2f}".format(
            ear), (435, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        return ear

    def start_classifier(self, settings, tracker):
        self.settings = settings
        self.tracker = tracker
        self.classify = self.init_classifier()

    def init_classifier(self):
        print("[INFO] loading facial landmark predictor...")
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.path_to_shape_predictor)

        # Grab the indexes of the facial landmarks for the left and right eye respectively
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
        self.left_eye = {'Start': lStart, 'End': lEnd}
        self.right_eye = {'Start': rStart, 'End': rEnd}

        return True

    def determine_strain(self, ear):
        # print(f'{ear} {self.settings.EYE_AR_THRESH}')
        if ear > self.settings.EYE_AR_THRESH:
            self.tracker.STRAIN_COUNT += 1
            if self.tracker.STRAIN_COUNT == self.settings.EYE_AR_CONSEC_FRAMES:
                # rest strain count
                self.tracker.reset_strain_count()
                # PUSH DICT TO STRAINARRAY
                current_datetime = datetime.now()
                self.tracker.strain_array.append(
                    {'timestamp': current_datetime, 'count': 1})

                self.tracker.TOTAL_STRAIN += 1
                print(self.tracker.TOTAL_STRAIN)
                if (self.tracker.TOTAL_STRAIN == self.tracker.STRAIN_THRESHOLD):
                    if not self.stop:
                        try:
                            notification.notify(
                                    title='Eyes Straining Warning!', 
                                    message='Stop Work and Rest',
                                    app_icon=None, 
                                    timeout=3,)
                        except Exception as e:
                            print(str(e))
                            self.tracker.increment_strain_threshold(self.settings.STRAIN_COUNTER_VALUE)
                            print(self.tracker.STRAIN_THRESHOLD)
        else:
            self.tracker.reset_strain_count

    def determine_drowsy(self, ear):
        # Check to see if the EAR is below the threshold value
        if ear < self.settings.EYE_AR_THRESH:
            self.tracker.DROWSY_COUNT += 1

            # If the eyes were closed for a sufficient number of times, then sound the alarm
            if self.tracker.DROWSY_COUNT == self.settings.DROWSINESS_FRAMES:
                self.tracker.reset_drowsy_count()
                current_datetime = datetime.now()
                current_datetime.strftime('%x %X')
                self.tracker.drowsy_array.append(
                    {'timestamp': current_datetime, 'count': 1})
                self.tracker.TOTAL_DROWSY += 1
                # If the alarm is not on, turn it on
                try:
                    notification.notify(
                        title='DROWSINESS WARNING!', 
                        message='Stop Work and Rest', 
                        app_icon=None, 
                        timeout=10,)
                except Exception as e:
                    print(str(e))

        else:
            self.tracker.reset_drowsy_count()


class CounterSettings():
    def __init__(self):
        # Threshold value for EAR,
        # move up/down the value if unable to detect strain or drowsiness accurately
        self.EYE_AR_THRESH = 0.5
        # 20 frames is approximately equals to 1 second,
        # move up/down the value if unable to detect accurately in seconds
        self.EYE_AR_CONSEC_FRAMES = 0
        self.DROWSINESS_FRAMES = 0  # Same as EAR_AR_CONSEC_FRAMES
        self.STRAIN_COUNTER_VALUE = 0
        self.TIMER_COUNTDOWN = 0
        self.EYES_OPEN_THRESHOLD = 0.18

    def update_settings(self, eye_frames, strain_value, drowsy_frames, timer_count):
        self.EYE_AR_CONSEC_FRAMES = int(eye_frames)*20
        self.STRAIN_COUNTER_VALUE = int(strain_value)
        self.DROWSINESS_FRAMES = int(drowsy_frames)*20
        self.TIMER_COUNTDOWN = int(timer_count) * (1200)


class Tracker():
    def __init__(self):
        self.STRAIN_COUNT = 0
        self.TOTAL_STRAIN = 0
        self.DROWSY_COUNT = 0
        self.TOTAL_DROWSY = 0
        self.STRAIN_THRESHOLD = 0
        self.strain_array = []
        self.drowsy_array = []
        self.parent_path = Path(__file__).parent.resolve()

        self.AWAY_COUNT = 0
        self.AWAY_CONSEC_FRAMES = 200
        self.AWAY = False

        self.TIMER_VALUE = 0
        self.TIMER_COUNTDOWN = 0
        self.TIMER_RESET = False

    def store_timer(self, timer_value):
        self.TIMER_VALUE = int(timer_value) * (1200)
        self.TIMER_COUNTDOWN = int(timer_value) * (1200)

    def reset_timer(self):
        self.TIMER_COUNTDOWN = self.TIMER_VALUE
        self.TIMER_RESET = False

    def reset_away_count(self):
        self.AWAY_COUNT = 0

    def reset_strain_count(self):
        self.STRAIN_COUNT = 0

    def reset_drowsy_count(self):
        self.DROWSY_COUNT = 0

    def set_strain_threshold(self, strain_value):
        self.STRAIN_THRESHOLD = int(strain_value)

    def increment_strain_threshold(self, strain_value):
        self.STRAIN_THRESHOLD += strain_value

    def save_arrays(self):
        self.save_array_plot(self.strain_array, 'strain')
        self.save_array_plot(self.drowsy_array, 'drowsy')

    def save_array_plot(self, in_array, name):
        if len(in_array) == 0:
            return 0
        df = pd.DataFrame(in_array)
        timestamp = datetime.now()
        save_time = timestamp.strftime("%d%B%Y%S")
        df['clean_time'] = df['timestamp'].dt.strftime('%m/%d/%Y %H:%M:%S')
        save_path = os.path.join(
            PARENT_PATH, f'excel/History-{name}-{save_time}.csv')
        df.to_csv(save_path)
        plt.figure()
        plt.scatter(x=df['clean_time'], y=df['count'], marker='o')
        plt.xlabel('Time stamp')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.title(f"History-{name}-{save_time}")

        plt.savefig(os.path.join(
            self.parent_path, f'excel/History-{name}-{save_time}.png'), bbox_inches='tight', dpi=150)
        return 1


def eye_aspect_ratio(eye):

    # Compute the euclidean distances between the two sets of vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # Compute the euclidean distance between the horizontal eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # Compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # Return the eye aspect ratio
    return ear


app = EyeTinker()
app.mainloop()
#exit()