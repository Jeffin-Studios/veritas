# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse

import numpy as np
import cv2
import tensorflow as tf
import os
import json



def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph


def read_tensor_from_image_file(file_name,
                                input_height=299,
                                input_width=299,
                                input_mean=0,
                                input_std=255):
  input_name = "file_reader"
  output_name = "normalized"

  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(
        file_reader, channels=3, name="png_reader")
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(
        tf.image.decode_gif(file_reader, name="gif_reader"))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
  else:
    image_reader = tf.image.decode_jpeg(file_reader, channels=3, name="jpeg_reader")

  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0)
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)

  return result



def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label


#For models retrained with retrain.py, input and output nodes are named "input" and "final_result"
# input_layer = #name of input node, usually called "input"
# output_layer = #name of output node, called "final_result" in models retrained with retrain.py
# # It is called "InceptionV3/Predictions/Reshape_1" in inception model, and "MobilenetV1/Predictions/Reshape_1" in mobilenet model

def identify(image, modelDir = "classifier/models", model = "inception_v3_2016_08_28", raw = False):
  old_pwd = os.getcwd()
  os.chdir(modelDir)
  
  with open('models.json') as json_data:
    model_data = json.load(json_data)

  
  model_file = model_data[model]['model_file']
  label_file = model_data[model]['label_file']

  input_mean = 0
  input_std = 255
  input_height = model_data[model]['input_height']
  input_width = model_data[model]['input_width']
  input_layer = model_data[model]['input_node']
  output_layer = model_data[model]['output_node']

  graph = load_graph(model_file)
  labels = load_labels(label_file)

  os.chdir(old_pwd)

  if raw:
    new_img = image
    new_img.flatten()
    new_img= cv2.resize(new_img,dsize=(299,299), interpolation = cv2.INTER_CUBIC)
    img_final = np.asarray(new_img)
    img_final=cv2.normalize(img_final.astype('float'), None, -0.5, .5, cv2.NORM_MINMAX)
    t = np.expand_dims(img,axis=0)

  else:
    file_name = image
    t = read_tensor_from_image_file(
        file_name,
        input_height=input_height,
        input_width=input_width,
        input_mean=input_mean,
        input_std=input_std)

  input_name = "import/" + input_layer
  output_name = "import/" + output_layer
  input_operation = graph.get_operation_by_name(input_name)
  output_operation = graph.get_operation_by_name(output_name)

  with tf.Session(graph=graph) as sess:
    results = sess.run(output_operation.outputs[0], {
        input_operation.outputs[0]: t
    })
  results = np.squeeze(results)
  top_k = results.argsort()[-5:][::-1]
  
  classification = []
  for i in top_k:
    classification.append((labels[i], results[i]))

  return classification



if __name__ == "__main__":

  file_name = "imagedata/grace_hopper.jpg"
  model = "inception_v3_2016_08_28"

  parser = argparse.ArgumentParser()
  parser.add_argument("--image", help="image to be processed")
  parser.add_argument("--graph", help="graph/model to be executed")

  args = parser.parse_args()

  if args.image:
    file_name = args.image
  if args.graph:
    model = args.graph

  classification = identify(image = file_name, modelDir = "models", model = model)
  for guess in classification:
    print(guess)

