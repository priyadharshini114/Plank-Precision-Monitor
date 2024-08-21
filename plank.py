import cv2
import mediapipe as mp
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

cap = cv2.VideoCapture("plank2.mp4")  # Replace with your video path

# Plank position duration
start_time = None
plank_duration = 0
plank_started = False

# Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Resize window
        image = cv2.resize(image, (800, 600))

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates for plank detection
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            
            # Calculate angles
            left_angle = calculate_angle(left_shoulder, left_hip, left_ankle)
            right_angle = calculate_angle(right_shoulder, right_hip, right_ankle)
            
            # Plank detection logic (Adjust the angles for different plank variations)
            if 160 < left_angle < 180 and 160 < right_angle < 180:
                if not plank_started:
                    start_time = time.time()
                    plank_started = True
                    plank_start_text = "Plank started: 0s"
            else:
                if plank_started:
                    plank_duration += time.time() - start_time
                    plank_started = False

            # Display position and time with background
            position_text = "Position: Plank Position" if plank_started else "Position: Not Planking"
            cv2.rectangle(image, (10, 10), (400, 60), (0, 0, 0), -1)  # Background for position text
            cv2.putText(image, position_text, (20, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Display plank start time when plank is detected
            if plank_started:
                elapsed_time = time.time() - start_time
                plank_time_text = f'Plank started: {int(elapsed_time)}s'
                # cv2.rectangle(image, (10, 260), (500, 310), (0, 0, 0), -1)  # Background for plank start text, moved up
                cv2.putText(image, plank_time_text, (20, 290), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)  # Text location adjusted


            # Display real-time clock at the bottom of the video
            real_time = time.strftime('%H:%M:%S', time.localtime())
            cv2.rectangle(image, (10, 570), (300, 600), (0, 0, 0), -1)  # Background for real-time clock
            cv2.putText(image, f'Real Time: {real_time}', (20, 590), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        except:
            pass
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Final time calculation after the loop ends
    if plank_started:
        plank_duration += time.time() - start_time

    # Display the total plank time once the video ends
    while True:
        final_frame = np.zeros((800, 600, 3), np.uint8)
        total_minutes = int(plank_duration // 60)
        total_seconds = int(plank_duration % 60)
        total_plank_time_str1 = f'Total Plank Time: {total_minutes} minutes'
        total_plank_time_str2 = f'and {total_seconds} seconds'
        
        cv2.rectangle(final_frame, (50, 250), (750, 550), (0, 0, 0), -1)  # Background for final time text
        cv2.putText(final_frame, total_plank_time_str1, (100, 300), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(final_frame, total_plank_time_str2, (100, 350), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('Mediapipe Feed', final_frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

print(f'Total Plank Time: {total_minutes} minutes and {total_seconds} seconds')

