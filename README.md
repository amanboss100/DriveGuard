# 🛡️ Drivegaurd AI: Ultimate Driver & Focus Safety System

**Drivegaurd AI** ek advanced Computer Vision tool hai jo real-time mein user ka focus aur fatigue (thakaan) track karta hai. Ise Mediapipe aur OpenCV ka use karke accidents ko rokne aur productivity badhane ke liye design kiya gaya hai.

---

## ✨ Key Features

* **👁️ Drowsiness Detection (EAR):** Eye Aspect Ratio calculate karke check karta hai ki aankhein kitni der se band hain.
* **🥱 Yawning Detection (MAR):** Mouth Aspect Ratio se jamhai (yawn) detect karta hai.
* **📐 Head Pose Estimation:** User agar screen se left, right, ya niche dekhta hai, toh ye distraction alert deta hai.
* **🌙 Adaptive Night Mode:** Low light mein image contrast ko automatically enhance karta hai (CLAHE Algorithm).
* **🚨 Smart Alert System:** 2.5 seconds se zyada distraction hone par looping alarm bajata hai.
* **📸 Incident Logging:** Har alert par automatically `incidents/` folder mein timestamp ke saath screenshot save karta hai.
* **📊 Visual Analytics:** Screen par live angles (Pitch/Yaw) aur focus progress bar dikhata hai.

---

## 🛠️ Tech Stack

* **Language:** Python 3.12
* **Libraries:** * `OpenCV`: Image Processing
    * `Mediapipe`: Face Mesh & Landmarks
    * `Pygame`: Audio Alert System
    * `NumPy`: Mathematical operations

---

## 🚀 Setup & Installation

1.  **Repository ko download karein.**
2.  **Virtual Environment create aur activate karein:**
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Zaroori libraries install karein:**
    ```powershell
    pip install opencv-python mediapipe pygame numpy
    ```
4.  **Files check karein:**
    * Ensure karein ki `danger.mp3` main folder mein hai.
    * `incidents/` folder pehli baar alert aane par apne aap ban jayega.

---

## 🖥️ How to Use

1.  **Code run karein:** `python eye_open_alert.py`
2.  **Calibration:** Start hote hi 2 second screen ki taraf seedha dekhein taaki system aapka center position samajh sake.
3.  **Alert:** Agar aap distract hote hain ya aankhein band karte hain, toh progress bar fill hoga aur alert bajega.
4.  **Exit:** Band karne ke liye keyboard par **'q'** dabayein.

---

## 📁 Folder Structure
```text
eye-opener/
├── eye_open_alert.py   # Main Python Script
├── danger.mp3          # Alert Sound File
├── README.md           # Documentation
└── incidents/          # Saved Screenshots (Auto-generated)


---
## 📞 Connect with Me
Agar aapko is project se related koi sawal hai ya aap collab karna chahte hain, toh mujhe Instagram par follow karein:

[![Instagram](https://img.shields.io/badge/Instagram-%23E4405F.svg?style=for-the-badge&logo=Instagram&logoColor=white)](https://www.instagram.com/Amanboss_100)

email ------ amankkumar551@gmail.com

**Developed with ❤️ by Aman**