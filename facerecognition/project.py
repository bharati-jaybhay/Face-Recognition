import face_recognition
import cv2
import tkinter as tk
from PIL import Image, ImageTk

def load_known_faces(image_paths, names):
    known_face_encodings = []
    known_names = []

    for image_path, name in zip(image_paths, names):
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        known_face_encodings.extend(face_encodings)
        known_names.extend([name] * len(face_encodings))

    return known_face_encodings, known_names

def recognize_faces(known_face_encodings, known_names):
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        face_locations = face_recognition.face_locations(frame)

        for face_location in face_locations:
            top, right, bottom, left = face_location

            face_encoding = face_recognition.face_encodings(frame, [face_location])[0]

            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

            print("Recognized Name:", name)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

def start_recognition():
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    recognize_faces(known_face_encodings, known_names)

def stop_recognition():
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    cv2.destroyAllWindows()

image_paths = ["Shubman Gill.jpg","samantha.jpg", "MESSI.jpg"]
names = ["Shubman", "samantha", "Messi"]

known_face_encodings, known_names = load_known_faces(image_paths, names)

# Create GUI
root = tk.Tk()
root.title("Face Recognition")

bg_image = Image.open("imgbg.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

start_button = tk.Button(root, text="Start Recognition", command=start_recognition, bg='#4CAF50', fg='white', padx=50, pady=20, font=("Helvetica", 12))  # Increase text size by changing font size
start_button.place(x=290, y=350)

stop_button = tk.Button(root, text="Stop Recognition", command=stop_recognition, state=tk.DISABLED, bg='#FC2F03', fg='white', padx=50, pady=20, font=("Helvetica", 12))  # Increase text size by changing font size
stop_button.place(x=1050, y=350)

root.mainloop()
