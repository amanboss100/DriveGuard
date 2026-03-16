import os
import cv2
import mediapipe as mp
import pygame
import time
import numpy as np
import math
import winsound
import warnings
from datetime import datetime

# --- System Cleanup & Setup ---
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
warnings.filterwarnings("ignore")

if not os.path.exists("incidents"):
    os.makedirs("incidents")

# --- Audio Initialization ---
pygame.mixer.init()
try:
    danger_sound = pygame.mixer.Sound("danger.mp3")
except:
    danger_sound = None

# --- Mediapipe Face Mesh ---
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, min_detection_confidence=0.5)

# --- Helper Functions ---
def get_ear(landmarks, eye_indices):
    p = [np.array([landmarks[i].x, landmarks[i].y]) for i in eye_indices]
    return (np.linalg.norm(p[1]-p[5]) + np.linalg.norm(p[2]-p[4])) / (2.0 * np.linalg.norm(p[0]-p[3]))

def get_mar(landmarks):
    top_lip = np.array([landmarks[13].x, landmarks[13].y])
    bottom_lip = np.array([landmarks[14].x, landmarks[14].y])
    left_corner = np.array([landmarks[78].x, landmarks[78].y])
    right_corner = np.array([landmarks[308].x, landmarks[308].y])
    return np.linalg.norm(top_lip - bottom_lip) / np.linalg.norm(left_corner - right_corner)

def apply_night_mode(img):
    yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    avg_brightness = np.mean(yuv[:, :, 0])
    if avg_brightness < 75:
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        yuv[:, :, 0] = clahe.apply(yuv[:, :, 0])
        img = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
        cv2.putText(img, "NIGHT MODE ACTIVE", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    return img

# --- Parameters & Variables ---
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]
ALERT_THRESHOLD = 2.5  
EAR_LIMIT = 0.20       
MAR_LIMIT = 0.50       
YAW_LIMIT = 15         
PITCH_LIMIT = 15       

cap = cv2.VideoCapture(0)
alert_start_time = None
is_playing = False
screenshot_taken = False
welcome_timer = 0

print("Sentinel AI Start ho gaya hai. Band karne ke liye 'q' dabayein.")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break
    
    frame = cv2.flip(frame, 1)
    frame = apply_night_mode(frame)
    h, w, _ = frame.shape
    
    results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    danger_triggered = False
    status_msg = "MONITORING"

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark
            
            # --- Head Pose Math ---
            face_2d, face_3d = [], []
            for idx in [33, 263, 1, 61, 291, 199]:
                lm = landmarks[idx]
                face_2d.append([lm.x * w, lm.y * h])
                face_3d.append([lm.x * w, lm.y * h, lm.z * 100])
            
            _, rot_vec, _ = cv2.solvePnP(np.array(face_3d, dtype=np.float64), np.array(face_2d, dtype=np.float64), 
                                         np.array([[w, 0, w/2], [0, w, h/2], [0, 0, 1]]), np.zeros((4, 1)))
            rmat, _ = cv2.Rodrigues(rot_vec)
            pitch = math.asin(rmat[2,1]) * 180 / math.pi
            yaw = math.atan2(rmat[2,0], rmat[2,2]) * 180 / math.pi

            avg_ear = (get_ear(landmarks, LEFT_EYE) + get_ear(landmarks, RIGHT_EYE)) / 2
            mar = get_mar(landmarks)

            # Safety Logic
            if avg_ear < EAR_LIMIT:
                danger_triggered, status_msg = True, "EYES CLOSED"
            elif mar > MAR_LIMIT:
                danger_triggered, status_msg = True, "YAWNING"
            elif abs(yaw) > YAW_LIMIT or pitch < -PITCH_LIMIT:
                danger_triggered, status_msg = True, "DISTRACTED"

    # --- UI & Alert Logic ---
    curr_time = time.time()
    if danger_triggered:
        if alert_start_time is None: alert_start_time = curr_time
        duration = curr_time - alert_start_time
        
        # Bottom Progress Bar
        bar_w = int((duration / ALERT_THRESHOLD) * w)
        cv2.rectangle(frame, (0, h-10), (bar_w, h), (0, 0, 255), -1)
        cv2.putText(frame, f"{status_msg}: {round(duration, 1)}s", (20, 50), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0,0,255), 2)
        
        if duration >= ALERT_THRESHOLD:
            if not is_playing:
                if danger_sound: danger_sound.play(loops=-1)
                is_playing = True
            if not danger_sound: winsound.Beep(1000, 100)
            
            if not screenshot_taken:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                cv2.imwrite(f"incidents/alert_{ts}.jpg", frame)
                screenshot_taken = True
            cv2.putText(frame, "!!! ALERT !!!", (w//2-100, h//2), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0,0,255), 3)
    else:
        # Safe State
        cv2.rectangle(frame, (0, h-10), (w, h), (0, 255, 0), -1)
        if is_playing:
            if danger_sound: danger_sound.stop()
            is_playing = False
            welcome_timer = curr_time + 1.2
        alert_start_time = None
        screenshot_taken = False
        if curr_time < welcome_timer:
            cv2.putText(frame, "SAFE", (w//2-50, h//2), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Sentinel AI Safety Monitor', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()

# BY AMAN