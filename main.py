#Importing the dependencies
import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

#Function for calculating the angle
def calculate_angle(a,b,c):
    a = np.array(a) #Shoulder
    b = np.array(b) #Elbow
    c = np.array(c) #Wrist
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])    #getting the angles between different joints using the x-y coordinates extracting by the webcam
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

#Video Feed
cap = cv2.VideoCapture(0)

#Curl Counter Variables
counter = 0
stage = None

#Setup Mediapipe Instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence = 0.5) as pose: 
    while cap.isOpened():
        ret, frame = cap.read()

        #Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        #Make Detections
        results = pose.process(image)

        #Recolor back to BGR
        image.flags.writeable =True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        #Extract Landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            #Get Landmarks
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]


            #Calculate Angle
            angle = calculate_angle(shoulder, elbow, wrist)

            #Visualize the angle
            cv2.putText(image, str(angle),
                        tuple(np.multiply(elbow, [640,480]).astype(int)),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA
                                      
                        )

            #Curl Counter Logic
            if angle > 160:
                stage = "down"
            if angle < 35 and stage == "down":
                stage = "up"
                counter += 1
                print(counter)

        except:
            pass
        
        #Render curl container
        #Setup Status Box
        cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)

        #Rep Data
        cv2.putText(image, 'REPS', (15,12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), (10,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

        #Stage Data
        cv2.putText(image, 'Stage', (65,12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, stage , (60,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)


        print(results)

        #Render Detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                  )

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

