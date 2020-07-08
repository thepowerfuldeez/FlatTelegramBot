import onnxruntime
import cv2
import numpy as np

import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
sess = onnxruntime.InferenceSession(f"{dir_path}/flats_optimized.onnx")
input_name = sess.get_inputs()[0].name
output_name = sess.get_outputs()[0].name

def get_prediction(image):
    blob = cv2.dnn.blobFromImage(image, mean=(123, 116, 103), scalefactor=1/57, size=(360, 360))

    out = sess.run([output_name], {input_name: blob})[0].reshape(-1)
    preds = np.exp(out)/np.sum(np.exp(out))
    return preds

if __name__ == "__main__":
    image = cv2.imread(sys.argv[1])
    preds = get_prediction(image)
    
    print(['bad', 'good'])
    print(preds)
