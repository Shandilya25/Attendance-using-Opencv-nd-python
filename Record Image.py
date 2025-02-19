import csv
import os, cv2
import numpy as np

def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech):
    if not l1 and not l2:
        text_to_speech("Please enter your Enrollment Number and Name.")
        return
    if not l1:
        text_to_speech("Please enter your Enrollment Number.")
        return
    if not l2:
        text_to_speech("Please enter your Name.")
        return

    try:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            message.configure(text="Error: Camera not accessible")
            text_to_speech("Error: Camera not accessible")
            return
        
        detector = cv2.CascadeClassifier(haarcasecade_path)
        Enrollment, Name = l1, l2
        sampleNum = 0
        directory = f"{Enrollment}_{Name}"
        path = os.path.join(trainimage_path, directory)
        
        os.makedirs(path, exist_ok=True)  # Safe directory creation

        while True:
            ret, img = cam.read()
            if not ret:
                message.configure(text="Error: Failed to capture image")
                text_to_speech("Error: Failed to capture image")
                break

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum += 1
                cv2.imwrite(os.path.join(path, f"{Name}_{Enrollment}_{sampleNum}.jpg"),
                            gray[y:y+h, x:x+w])
                cv2.imshow("Frame", img)

            if cv2.waitKey(1) & 0xFF == ord("q") or sampleNum >= 50:
                break

        cam.release()
        cv2.destroyAllWindows()

        with open("StudentDetails/studentdetails.csv", "a+", newline="") as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([Enrollment, Name])

        res = f"Images Saved for ER No: {Enrollment}, Name: {Name}"
        message.configure(text=res)
        text_to_speech(res)

    except Exception as e:
        err_msg = f"Error: {str(e)}"
        message.configure(text=err_msg)
        text_to_speech(err_msg)
