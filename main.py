import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
import pyttsx3
from ttkbootstrap import Style
from PIL import Image, ImageTk
from google.protobuf.json_format import MessageToDict

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize MediaPipe Hands
mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75,
    max_num_hands=2
)

# Gesture Recognition Function
def recognize_gesture(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mpHands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mpHands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mpHands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mpHands.HandLandmark.PINKY_TIP]

    index_pip = hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_PIP]
    middle_pip = hand_landmarks.landmark[mpHands.HandLandmark.MIDDLE_FINGER_PIP]
    ring_pip = hand_landmarks.landmark[mpHands.HandLandmark.RING_FINGER_PIP]
    pinky_pip = hand_landmarks.landmark[mpHands.HandLandmark.PINKY_PIP]

    if index_tip.y < index_pip.y and middle_tip.y < middle_pip.y and ring_tip.y > ring_pip.y and pinky_tip.y > pinky_pip.y:
        return "Peace"
    elif index_tip.y < index_pip.y and middle_tip.y > middle_pip.y and ring_tip.y > ring_pip.y and pinky_tip.y > pinky_pip.y:
        return "I"
    elif index_tip.y > index_pip.y and middle_tip.y > middle_pip.y and ring_tip.y > ring_pip.y and pinky_tip.y > pinky_pip.y and thumb_tip.y > index_pip.y:
        return "Fist"
    elif index_tip.y < index_pip.y and pinky_tip.y < pinky_pip.y and middle_tip.y > middle_pip.y and ring_tip.y > ring_pip.y:
        return "I Love You"
    elif index_tip.y > index_pip.y and middle_tip.y > middle_pip.y and ring_tip.y > ring_pip.y and pinky_tip.y > pinky_pip.y:
        return "Okay"
    elif thumb_tip.y < index_pip.y and pinky_tip.y < pinky_pip.y and index_tip.y > index_pip.y and middle_tip.y > middle_pip.y and ring_tip.y > ring_pip.y:
        return "Call"
    elif middle_tip.y < middle_pip.y and ring_tip.y < ring_pip.y and pinky_tip.y < pinky_pip.y:
        return "Stop"
    else:
        return "Unknown"

# Login Window
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x300")
        self.root.configure(bg="black")

        self.label_username = tk.Label(root, text="Username:", font=("Arial", 14), fg="white", bg="black")
        self.label_username.pack(pady=10)
        self.entry_username = tk.Entry(root, font=("Arial", 14))
        self.entry_username.pack(pady=5)

        self.label_password = tk.Label(root, text="Password:", font=("Arial", 14), fg="white", bg="black")
        self.label_password.pack(pady=10)
        self.entry_password = tk.Entry(root, font=("Arial", 14), show="*")
        self.entry_password.pack(pady=5)

        self.button_login = tk.Button(root, text="Login", font=("Arial", 14), bg="green", fg="white", command=self.check_login)
        self.button_login.pack(pady=20)

    def check_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if username == "admin" and password == "1234":
            speak("Login successful")
            self.root.destroy()
            main_app()
        else:
            speak("Invalid credentials")
            tk.messagebox.showerror("Login Failed", "Invalid Username or Password")

# Gesture Recognition App
class GestureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Gesture Recognition")
        self.root.geometry("900x700")
        
        style = Style(theme="darkly")
        self.root.configure(bg="black")

        self.label_title = tk.Label(root, text="Hand Gesture Recognition", font=("Arial", 18, "bold"), fg="white", bg="black")
        self.label_title.pack(pady=10)

        self.label_video = tk.Label(root, bg="black")
        self.label_video.pack()

        self.label_gesture = tk.Label(root, text="Gesture: ", font=("Arial", 16), fg="white", bg="black")
        self.label_gesture.pack(pady=10)

        self.label_hand = tk.Label(root, text="", font=("Arial", 16), fg="white", bg="black")
        self.label_hand.pack(pady=10)

        self.button_quit = tk.Button(root, text="Quit", command=self.quit_app, font=("Arial", 14), bg="red", fg="white")
        self.button_quit.pack(pady=10)

        self.cap = cv2.VideoCapture(0)
        speak("Gesture recognition started")
        self.update_video()

    def update_video(self):
        success, img = self.cap.read()
        if not success:
            return

        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        detected_gesture = "Unknown"
        hand_side = ""

        hand_count = 0
        hand_labels = []

        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                mpDraw.draw_landmarks(img, hand_landmarks, mpHands.HAND_CONNECTIONS)
                detected_gesture = recognize_gesture(hand_landmarks)
                speak(detected_gesture)

                label_dict = MessageToDict(results.multi_handedness[idx])
                hand_side = label_dict['classification'][0]['label']
                hand_labels.append(hand_side)
                hand_count += 1

        if hand_count == 1:
            if "Left" in hand_labels:
                hand_side = "Left Hand"
            elif "Right" in hand_labels:
                hand_side = "Right Hand"
        elif hand_count == 2:
            if "Left" in hand_labels and "Right" in hand_labels:
                hand_side = "Both Hands"
            if "Left" in hand_labels and "Right" not in hand_labels:
                hand_side = "Left Hand"
            if "Right" in hand_labels and "Left" not in hand_labels:
                hand_side = "Right Hand"
            if "Left" in hand_labels and "Right" in hand_labels:
                # Detect Crossed Hands
                if results.multi_hand_landmarks[0].landmark[mpHands.HandLandmark.WRIST].x > results.multi_hand_landmarks[1].landmark[mpHands.HandLandmark.WRIST].x:
                    hand_side = "Crossed Hands"
                else:
                    hand_side = "Both Hands"

        self.label_gesture.config(text=f"Gesture: {detected_gesture}")
        self.label_hand.config(text=f"Hand: {hand_side}")

        img = Image.fromarray(img)
        img = img.resize((640, 480))
        img_tk = ImageTk.PhotoImage(image=img)
        self.label_video.img_tk = img_tk
        self.label_video.config(image=img_tk)
        self.root.after(10, self.update_video)

    def quit_app(self):
        speak("Application closed")
        self.cap.release()
        cv2.destroyAllWindows()
        self.root.quit()

# Start Login First, Then Main App
def main_app():
    root = tk.Tk()
    app = GestureApp(root)
    root.mainloop()

if __name__ == "__main__":
    login_root = tk.Tk()
    login_app = LoginWindow(login_root)
    login_root.mainloop()
