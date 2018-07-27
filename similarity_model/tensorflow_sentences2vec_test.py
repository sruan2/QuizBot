import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re

from sif_implementation.utils import *
from messages import MESSAGES

print('imports done')
module_url = "https://tfhub.dev/google/universal-sentence-encoder/2"

# Universal Sentence Encoder'sentence TF Hub model
embed = hub.Module(module_url)
print('loaded module')

def run_and_plot(session_, input_tensor_, messages_, encoding_tensor):
	message_embeddings_ = session_.run(
	  encoding_tensor, feed_dict={input_tensor_: messages_})
	corr = np.inner(message_embeddings_, message_embeddings_)
	plot_similarity(MESSAGES, corr, 90, 'heatmaps/tensorflow_heatmap.png')

similarity_input_placeholder = tf.placeholder(tf.string, shape=(None))
similarity_message_encodings = embed(similarity_input_placeholder)

with tf.Session() as session:
	session.run([tf.global_variables_initializer(), tf.tables_initializer()])
	run_and_plot(session, similarity_input_placeholder, MESSAGES, 
		   similarity_message_encodings)
	print('plotted this')

