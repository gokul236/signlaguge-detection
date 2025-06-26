import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from ttkbootstrap import Style
from PIL import Image, ImageTk
from google.protobuf.json_format import MessageToDict

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
     # "I" Gesture: Index finger up, all other fingers down
    elif(index_tip.y < index_pip.y and middle_tip.y > middle_pip.y and ring_tip.y > ring_pip.y and pinky_tip.y > pinky_pip.y):
        return "I"
    elif (index_tip.y > index_pip.y and  middle_tip.y > middle_pip.y and ring_tip.y > ring_pip.y and pinky_tip.y > pinky_pip.y and  thumb_tip.y > index_pip.y):  # Ensure the thumb is also folded 
        return "Fist"
    elif (index_tip.y < index_pip.y and  middle_tip.y < middle_pip.y and ring_tip.y < ring_pip.y and pinky_tip.y < pinky_pip.y and thumb_tip.y < index_pip.y):  # Thumb is folded 
        return "Help"
    elif index_tip.y < index_pip.y and pinky_tip.y < pinky_pip.y and middle_tip.y > middle_pip.y and ring_tip.y > ring_pip.y:
        return "I Love You"
    elif index_tip.y > index_pip.y and middle_tip.y > middle_pip.y and ring_tip.y > ring_pip.y and pinky_tip.y > pinky_pip.y:
        return "Okay"
    elif thumb_tip.y < index_pip.y and pinky_tip.y < pinky_pip.y and index_tip.y > index_pip.y and middle_tip.y > middle_pip.y and ring_tip.y > ring_pip.y:
        return "Call"
    elif middle_tip.y < middle_pip.y and ring_tip.y < ring_pip.y and pinky_tip.y < pinky_pip.y and index_tip.y > index_pip.y and thumb_tip.y > index_pip.y:
        return "Super"
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
        
        # Hardcoded Credentials (Change as needed)
        if username == "admin" and password == "1234":
            self.root.destroy()  # Close login window
            main_app()  # Launch Gesture Recognition
        else:
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

        self.button_quit = tk.Button(root, text="Quit", command=self.quit_app, font=("Arial", 14), bg="red", fg="white")
        self.button_quit.pack(pady=10)

        self.cap = cv2.VideoCapture(0)
        self.update_video()

    def update_video(self):
        success, img = self.cap.read()
        if not success:
            return

        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        detected_gesture = "Unknown"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mpDraw.draw_landmarks(img, hand_landmarks, mpHands.HAND_CONNECTIONS,
                                      mpDraw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                                      mpDraw.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2))
                detected_gesture = recognize_gesture(hand_landmarks)

            for i in results.multi_handedness:
                label_dict = MessageToDict(i)
                label = label_dict['classification'][0]['label']
                if label == 'Left':
                    cv2.putText(img, 'Left Hand', (20, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)
                elif label == 'Right':
                    cv2.putText(img, 'Right Hand', (460, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)

        self.label_gesture.config(text=f"Gesture: {detected_gesture}")

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = img.resize((640, 480))
        img_tk = ImageTk.PhotoImage(image=img)

        self.label_video.img_tk = img_tk
        self.label_video.config(image=img_tk)
        self.root.after(10, self.update_video)

    def quit_app(self):
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
