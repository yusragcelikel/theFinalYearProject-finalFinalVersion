from recognition import FaceRecognition
import cv2
import os.path
import numpy as np

print("Press 1 for the SAVE process.")
print("Press 2 for the RECOGNIZE process.")
process_choice = int(input())
#print(process_choice)

if process_choice == 1:
    print("Please enter the admin password to continue.")
    password_counter = 0

    while password_counter < 3: #password check
        password = int(input("Please enter the admin password: "))

        if password == 0000:
            print("Access Granted.")
            img_name = input("Please type the name: ").lower()

            cap = cv2.VideoCapture(0)  # video objectimizi oluşturduk
            print("press ESC to close")
            print("press SPACE to save image")
            img_counter = 0

            while True:
                success, img = cap.read()


                if img_counter == 1:
                    exit()  # 1 tane image capture edildiğinde programı kapatır.

                else:
                    cv2.imshow("Image", img)  # kamera görüntüsü image adlı pencerede gosterilir
                    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
                    k = cv2.waitKey(1)

                    if k % 256 == 27:
                        break  # esc tuşuna basıldığında kamera penceresi kapanacak

                    elif k % 256 == 32:
                        path = "C:/Users/oguz9/Documents/GitHub/theFinalYearProject-finalFinalVersion/saved_subjects"
                        cv2.imwrite(os.path.join(path, "{}.png".format(img_name)), img)

                        print("Image Successfully Captured and Saved.")
                        img_counter += 1

            break
        else:
            print("Access Denied!")
            password_counter += 1
            if password_counter == 3:
                print("You\'ve entered the wrong password three times. Programme shutting down.")

elif process_choice == 2:
    print("Please press esc button to exit.")
    # -------image recognition kısmı------
    if __name__ == '__main__':
        fr = FaceRecognition()
        fr.run_recognition()
    # -------image recognition kısmı------


else:
    print("You\'ve punched an invalid number.")
    exit()


