# USAGE
# python yolo.py --yolo yolo-coco

# import the necessary packages
import numpy as np
import argparse
import time
import cv2
import os
from firebase import firebase
from tkinter import filedialog
from tkinter import *


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-y", "--yolo", required=True,
	help="base path to YOLO directory")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
	help="threshold when applyong non-maxima suppression")
args = vars(ap.parse_args())

# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# initialize a list of colors to represent each possible class label
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join([args["yolo"], "yolov3.weights"])
configPath = os.path.sep.join([args["yolo"], "yolov3.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes)
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

filename1 =  filedialog.askopenfilename(initialdir = "C:/Users/Sri Satya Sai/Documents/bytecamp/yolo-object-detection/videos", title = "Select file",filetypes = (("mp4 files","*.mp4"),("all files","*.*")))
fne = os.path.basename(filename1)
fn = os.path.splitext(fne)[0]
vidcap = cv2.VideoCapture(filename1)
def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        a = cv2.imwrite(fn+"_frame_"+str(sec)+"sec.jpg", image)     # save frame as JPG file
    return hasFrames
sec = 0
frameRate = 10 #it will capture image in each * second
success = getFrame(sec)
while success:
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)
# load our input image and grab its spatial dimensions
filename =  filedialog.askopenfilename(initialdir = "C:/Users/Sri Satya Sai/Documents/bytecamp/yolo-object-detection", title = "Select file",filetypes = (("jpg files","*.jpg"),("all files","*.*")))
image = cv2.imread(filename)
(H, W) = image.shape[:2]

# determine only the *output* layer names that we need from YOLO
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# construct a blob from the input image and then perform a forward
# pass of the YOLO object detector, giving us our bounding boxes and
# associated probabilities
blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
	swapRB=True, crop=False)
net.setInput(blob)
start = time.time()
layerOutputs = net.forward(ln)
end = time.time()

# show timing information on YOLO
print("[INFO] YOLO took {:.6f} seconds".format(end - start))

# initialize our lists of detected bounding boxes, confidences, and
# class IDs, respectively
boxes = []
confidences = []
classIDs = []
count1,count2 = 0,0
xi=[]
yi=[]
# loop over each of the layer outputs
for output in layerOutputs:
	# loop over each of the detections
	for detection in output:
		# extract the class ID and confidence (i.e., probability) of
		# the current object detection
		scores = detection[5:]
		classID = np.argmax(scores)
		confidence = scores[classID]

		# filter out weak predictions by ensuring the detected
		# probability is greater than the minimum probability
		if confidence > args["confidence"]:
			# scale the bounding box coordinates back relative to the
			# size of the image, keeping in mind that YOLO actually
			# returns the center (x, y)-coordinates of the bounding
			# box followed by the boxes' width and height
			box = detection[0:4] * np.array([W, H, W, H])
			(centerX, centerY, width, height) = box.astype("int")

			# use the center (x, y)-coordinates to derive the top and
			# and left corner of the bounding box
			x = int(centerX - (width / 2))
			y = int(centerY - (height / 2))

			# update our list of bounding box coordinates, confidences,
			# and class IDs
			boxes.append([x, y, int(width), int(height)])
			confidences.append(float(confidence))
			classIDs.append(classID)

# apply non-maxima suppression to suppress weak, overlapping bounding
# boxes
idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
	args["threshold"])

# ensure at least one detection exists
if len(idxs) > 0:
	# loop over the indexes we are keeping
	for i in idxs.flatten():
		# extract the bounding box coordinates
		(x, y) = (boxes[i][0], boxes[i][1])
		(w, h) = (boxes[i][2], boxes[i][3])

		# draw a bounding box rectangle and label on the image
		color = [int(c) for c in COLORS[classIDs[i]]]
		if(classIDs[i] == 1 or classIDs[i] == 2 or classIDs[i] == 3 or classIDs[i] == 5 or classIDs[i] == 7):
			cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
			text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
			cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
				0.5, color, 2)
			print(x,y,classIDs[i],confidences[i])
			xi.append(x)
			yi.append(y)
		
		
	for i in range(1,len(xi)):
		if (((xi[i] - xi[i-1]) <= 100) and ((yi[i] - yi[i-1]) <= 100)):
			count1 = count1 + 1
		else:
			count2 = count2 + 1
# show the output image
print(count1)
print(count2)
cv2.putText(image, "count of side having maximum traffic:"+str(count1), (0, 15), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 2)
cv2.putText(image, "count of side having lesser traffic:"+str(count2), (0, 30), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 2)
cv2.imshow("Image", image)
cv2.waitKey(0)

firebase = firebase.FirebaseApplication('https://smarttraffic-c88f7.firebaseio.com', None)
timer = int(input("Enter timer to be set:"))
firebase.put('/LED_Status','timer',timer)
firebase.put('/LED_Status','count1',count1)
firebase.put('/LED_Status','count2',count2)
print("timer passed to database")