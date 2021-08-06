''' video recording using deep learning face blurring  '''

import cv2
import numpy as np

# https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt
prototxt_path = "weights/deploy.prototxt.txt"
# https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20180205_fp16/res10_300x300_ssd_iter_140000_fp16.caffemodel 
model_path = "weights/res10_300x300_ssd_iter_140000_fp16.caffemodel"

# load Caffe model
model = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)




# read the desired image
image = cv2.imread("output.avi")
# get width and height of the image
h, w = image.shape[:2]
# gaussian blur kernel size depends on width and height of original image
kernel_width = (w // 7) | 1
kernel_height = (h // 7) | 1

''' Now to pass this image into the neural network, we need to prepare it. More specifically,
 we need to resize the image to the shape of (300, 300)
 and performs mean subtraction as it's trained that way:'''

# preprocess the image: resize and performs mean subtraction
blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))

# set the image into the input of the neural network
model.setInput(blob)
# perform inference and get the result
output = np.squeeze(model.forward())
 
## Now output object is a numpy array that has all faces detected,
## let's iterate over this array and only blur portions where we're confident that it's a face:
while True:
    for i in range(0, output.shape[0]):
        confidence = output[i, 2]
        # get the confidence
        # if confidence is above 40%, then blur the bounding box (face)
        if confidence > 0.4:
            # get the surrounding box cordinates and upscale them to original image
            box = output[i, 3:7] * np.array([w, h, w, h])
            # convert to integers
            start_x, start_y, end_x, end_y = box.astype(np.int)
            # get the face image
            face = image[start_y: end_y, start_x: end_x]
            # apply gaussian blur to this face
            face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)
            # put the blurred face into the original image
            image[start_y: end_y, start_x: end_x] = face

 # Write the frame into the file 'output.avi'
    # out.write(frame)



    cv2.imshow('faceblur',frame)
    key=cv2.waitKey(1)

    if key==ord('q'):
         break

video.release()
cv2.destroyAllWindows





