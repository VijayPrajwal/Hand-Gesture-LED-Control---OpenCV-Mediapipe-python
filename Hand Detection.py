# Importing Libraries needed
import cv2
import mediapipe as mp
import time
#import pyautogui
import LEDControl
import datetime

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

#Detects the webcam
cap = cv2.VideoCapture(0)

#Webcam Video Frame Size
cap.set(3, 960)
cap.set(4, 540)

#For FPS
pre_timeframe = 0
new_timeframe = 0
prev_total = -1

#Hand Landmark IDs from Mediapipe
tips  = [8, 12, 16, 20] # ID: 8(INDEX_FINGER_TIP), 12(MIDDLE_FINGER_TIP), 16(RING_FINGER_TIP), 20(PINKY_TIP)
pips = [6, 10, 14, 18]  # ID: 6(INDEX_FINGER_PIP), 10(MIDDLE_FINGER_PIP), 14(RING_FINGER_PIP), 18(PINKY_PIP)
finger_name = ["Thumb", "Index", "Middle", "Ring", "Pinky"]

#To save the recorded video as .mp4 file format
recording = False
record_start_time = 0
writer = cv2.VideoWriter("Recording.mp4", cv2.VideoWriter_fourcc(*'DIVX'), 30, (960, 540))

# Mediapipe Hand Landmarks. This section detects the hand landmarks and updates the fingers list accordingly. 
with mp_hand.Hands(max_num_hands = 1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:

    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break

        #Mirroring the Live Webcam video
        frame = cv2.flip(frame, 1)

        #A note saying the user about how to quit the program and if he wants to record it.
        cv2.rectangle(frame, (5, 500), (558, 535), (40, 40, 40), -1)
        cv2.rectangle(frame, (5, 500), (558, 535), (0, 255, 255), 2)
        cv2.putText(frame, "Press 'R' to Record (10s) | Press 'Q' to Quit", (12, 523), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 1)

        #Adding FPS to the Live Video
        new_timeframe = time.time()
        fps = 1 / (new_timeframe - pre_timeframe)
        pre_timeframe = new_timeframe
        fps = int(fps) #convert from float to int
        cv2.putText(frame, f"FPS = {str(fps)}", (10, 65), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 1)

        #This is to convert BGR to RGB format for Mediapipe
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Converting from BGR to RGB for Mediapipe
        frame.flags.writeable = False #Keeps the video frame read-only
        results = hands.process(frame) #Mediapipe will look and detect hands in the live video from webcam
        frame.flags.writeable = True 
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) #Converting RGB to BGR again, because CV2 library uses BGR format to display each frame   

        #To Display Date & TIme in the live video
        font = cv2.FONT_HERSHEY_TRIPLEX
        dt = str(datetime.datetime.now()).split('.')[0] #Using datetime library to caputre current date & Time while webcam is on
        frame = cv2.putText(frame, dt, (10, 25), font, 0.875, (255, 255, 255), 1, cv2.LINE_AA) #Allows to write a message on each frame of live webcam feed

        #Detecting Hand Landmarks
        if results.multi_hand_landmarks: #This means If result.multi_hand_landmarks is True then excecutes the command
            for hand_landmark in results.multi_hand_landmarks:
                fingers = []
                mp_draw.draw_landmarks(frame, 
                                       hand_landmark, 
                                       mp_hand.HAND_CONNECTIONS,
                                       mp_draw.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=5),
                                       mp_draw.DrawingSpec(color=(0, 0, 0), thickness=3)) #Connect the dots with lines
                
                #Check for Thumb Position and update the fingers list
                thumb_tip = hand_landmark.landmark[4]
                thumb_pip = hand_landmark.landmark[3]
                if thumb_tip.x < thumb_pip.x:
                    fingers.append(1)
                else:
                    fingers.append(0)
                #Check for other Fingers: Index, Middle, Ring, Pinky 
                for i in range(4):
                    tip = hand_landmark.landmark[tips[i]] #tips = [8, 12, 16, 20]
                    pip = hand_landmark.landmark[pips[i]] #pips = [6, 10, 14, 18]
                    if tip.y < pip.y:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                total = sum(fingers) #To indicate number of fingers pointing that moment   

                #Displays the output on the terminal window
                if total != prev_total:
                    print(f"Fingers: {fingers}, Total Count: {total}")
                    prev_total = total
                
                #Goes to the LEDControl Module and runs the LED function defined
                LEDControl.LED(fingers)             
                
                #To write on the live webcam video frame how many LEDs glow with repect which finger is pointing upward
                cv2.rectangle(frame, (740, 20), (940, 120), (10, 10, 10), -1)
                cv2.rectangle(frame, (740, 20), (940, 120), (255, 255, 255), 3)
                cv2.putText(frame, str(total), (750, 90), cv2.FONT_HERSHEY_TRIPLEX, 2, (0,0,255), 3)
                cv2.putText(frame, "LED", (810, 90), cv2.FONT_HERSHEY_TRIPLEX, 2, (255,255,255), 3)
                
                #Displays which finger is lifted in the Live webcam video
                if total == 0:
                    cv2.putText(frame, "Finger(s): Folded", (10, 97), cv2.FONT_HERSHEY_TRIPLEX, 1, (50,50,50), 1)
                elif total == 5:
                    cv2.putText(frame, "Finger(s): All Open", (10, 97), cv2.FONT_HERSHEY_TRIPLEX, 1, (50,50,50), 1)
                else:
                    lifted_finger = []
                    for i in range(5):
                        if fingers[i] == 1:
                            lifted_finger.append(finger_name[i])
                            cv2.putText(frame, f"Finger(s): {', '.join(lifted_finger)}", (10, 97), cv2.FONT_HERSHEY_TRIPLEX, 1, (50,50,50), 1)
        
        #Condition to record the video when 'R' is pressed
        if recording == True:
            elapsed_time = time.time() - record_start_time
            print(f"Recording Time: {elapsed_time:.1f}")
            cv2.putText(frame, f"REC {elapsed_time:.0f}s", (10, 126), cv2.FONT_HERSHEY_TRIPLEX, 1, (0,0,255), 1)
            writer.write(frame)
            #To stop recording if elapsed time is greater than 12s. This timing can be changed accordingly
            if elapsed_time >= 10:
                recording = False
                cv2.putText(frame, f"REC SAVED", (10, 126), cv2.FONT_HERSHEY_TRIPLEX, 1, (0,0,255), 1)
                writer.release()
                print("Recording Stopped")
                
        cv2.imshow('Hand Gesture to Control LEDs', frame)

        #If condition used to check the user input
        key = cv2.waitKey(1)
        if key == ord('r'):
            recording = True
            record_start_time = time.time()         
            print("Recording started")
            print(record_start_time)
        elif key == ord('q'):
            break
        
cap.release()
writer.release()
cv2.destroyAllWindows()