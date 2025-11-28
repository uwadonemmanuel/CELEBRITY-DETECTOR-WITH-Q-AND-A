import cv2
from io import BytesIO
import numpy as np

def process_image(image_file):
    in_memory_file = BytesIO()
    image_file.save(in_memory_file)

    image_bytes = in_memory_file.getvalue()
    nparr = np.frombuffer(image_bytes,np.uint8)

    img = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_cascade =cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    faces =face_cascade.detectMultiScale(gray,1.1,5)

    if len(faces)==0:
        return image_bytes,None

    largest_face = max(faces,key=lambda r:r[2] *r[3])

    (x,y,w,h) = largest_face

    cv2.rectangle(img, (x,y),(x+w , y+h) , (0,255,0),3 )

    is_sucess , buffer = cv2.imencode(".jpg" , img)

    return buffer.tobytes(), largest_face