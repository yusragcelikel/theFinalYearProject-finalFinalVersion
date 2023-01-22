import face_recognition
import os, sys
import cv2
import numpy as np
import math


# image recognition yüzdesi hesaplayıp ekrana yazdıracağız:
def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


class FaceRecognition:
    face_locations = [] #
    face_encodings = [] #yüzleri encode edip kullanabilmek için
    face_names = [] #kimin yüzü olduğunu recognise edebilmek için
    known_face_encodings = [] #yükleyeceğimiz yüzler için
    known_face_names = [] #girdiğimiz isimler için
    process_current_frame = True # bütün frameleri inceleyip bilgisayarı yormamak için

    def __init__(self): #encode_faces'i başlatmak için
        self.encode_faces()

    def encode_faces(self): #yukarıdaki encode_faces fonksiyonu oluşturulur
        for image in os.listdir('saved_subjects'):
            face_image = face_recognition.load_image_file(f"saved_subjects/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)

        print(self.known_face_names)#kontrol için resmin ismi yazdırılır

    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)

        while True:
            ret, frame = video_capture.read()
            cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)

            # bilgisayarı yormamak için her frame'in görüntüsünü almamak için kontrol yapılır
            if self.process_current_frame:
                # video görüntüsü boyutları değiştirilir
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # resim rbg'ye dönüştürülür
                rgb_small_frame = small_frame[:, :, ::-1]

                # tüm yüzlerin yeri bulunur:
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                for face_encoding in self.face_encodings:
                    # bilinen yüzler var mı diye kontrol edilir:
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"
                    confidence = '???'

                    # yüz uzaklıkları bulunur ve en iyi karşılaştırma resmi bulunur
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = face_confidence(face_distances[best_match_index])

                    self.face_names.append(f'{name} ({confidence})') #recognize edilen resmin ismi ve yüzde yazılır.

            self.process_current_frame = not self.process_current_frame

            # sonuçları göstermek için:
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                # görüntüyü yukarıda 4'te birine dönüştürmüştük, aşağıda bu durum tersine çevrilir:
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # yüz çevresindeki çerçeve görüntüsü düzenlenir:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

            # face recognition adlı pencerede gösterilir:
            cv2.imshow('Face Recognition', frame)

            # esc tuşuyla çıkmak için:
            if cv2.waitKey(1) % 256 == 27:
                break  # esc tuşuna basıldığında kamera penceresi kapanacak

        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    fr = FaceRecognition() #FaceRecognition sınıfı çağırılır
    fr.run_recognition() #tüm recognize kodlarımızın olduğu fonksiyon çağırılır