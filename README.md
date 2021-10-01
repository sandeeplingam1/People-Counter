
# People-Counter
What is it about:
+++++++++++++++++++++++++++++++++++++++++
A team project in the final year of my graduation which deals with the main concept of estimating the amount of people at a particular area at that instance of time.
+++++++++++++++++++++++++++++++++++++++++
Code:
+++++
import time
import threading 
import cv2
from gtts import gTTS 
import os
from pygame import mixer
// the above used import functions have their own significant role in the program.

def find_no_of_faces(face_cascade,image,grayImage,faces,output):// this method is used for calculating the number of faces appeared on the frame.//
	try:
		print(output)
		for (x,y,w,h) in faces:
			cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),5)
			cv2.putText(image, '*',(x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 5)

		rectangle_color = (0,0,255)
		rectangle_thickness = 5
		cv2.rectangle(image, ((0,image.shape[0] -25)),(270, image.shape[0]), rectangle_color, rectangle_thickness) 
		number_of_faces = str(faces.shape[0])
		text_color = (255,255,0)
		text_thickness = 3
		font_family = cv2.FONT_HERSHEY_TRIPLEX
		cv2.putText(image, "Number of faces detected: " + number_of_faces, (0,image.shape[0] -10), font_family,1,text_color, text_thickness)
		im = cv2.resize(image,(500, 500)) 
		cv2.imshow('Image with faces',im)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
	except:
		pass
	

def voice_output(output):
	try:
		myobj = gTTS(text = output, slow=False)  
		myobj.save("speak_count.mp3") 
		mixer.init()
		mixer.music.load('speak_count.mp3')
		mixer.music.play()
	except:
		pass

def start_counting(image):
	face_cascade = cv2.CascadeClassifier('dataset.xml')
	grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(grayImage)

	if len(faces) == 0:
		output = "No faces found"
		t2 = threading.Thread(target=voice_output, args=(output,)) 
		t2.start() 
		t2.join() 
	else:
		output = "Number of faces detected: " + str(faces.shape[0])
		t1 = threading.Thread(target=find_no_of_faces, args=(face_cascade,image,grayImage,faces,output)) 
		t2 = threading.Thread(target=voice_output, args=(output,)) 
		t1.start() 
		t2.start() 
		t1.join() 
		t2.join() 



print("1) Photo path")
print("2) Web Cam")

option = input()

if option == "1":
	print("please enter the path of image")
	path = input()
	image = cv2.imread(path)
	start_counting(image)
elif option == "2":
	video_capture = cv2.VideoCapture(0)
	anterior = 0
	faceCascade = cv2.CascadeClassifier('dataset.xml')
	#anterior = 0
	while True:
	    ret, frame = video_capture.read()
	    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	    faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30))
	
	    for (x, y, w, h) in faces:
	        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),5)
	        cv2.putText(frame, '*'+str(len(faces)),(x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 5)
	
	    if anterior != len(faces):
	        anterior = len(faces)
	        if str(len(faces)) != "0":
	        	voice_output("faces: "+str(len(faces)))
	        '''t = threading.Thread(target=voice_output, args=(str(len(faces)))) 
	        t.start()  
	        t.join() '''

	    cv2.imshow('Video', frame)
	
	    if cv2.waitKey(1) & 0xFF == ord('s'): 
	        check, frame = video_capture.read()
	        cv2.imshow("Capturing", frame)
	        cv2.imwrite(filename='saved_img.jpg', img=frame)
	        video_capture.release()
	        img_new = cv2.imread('saved_img.jpg', cv2.IMREAD_GRAYSCALE)
	        img_new = cv2.imshow("Captured Image", img_new)
	        cv2.waitKey(1650)
	        cv2.destroyAllWindows()
	        break
	
	    elif cv2.waitKey(1) & 0xFF == ord('q'):
	        voice_output("Turning off camera...")
	        voice_output(str(len(faces)))
	        video_capture.release()
	        cv2.destroyAllWindows()
	        voice_output("Camera off.")
	        break
	    cv2.imshow('Video', frame)
	
	video_capture.release()
	cv2.destroyAllWindows()
