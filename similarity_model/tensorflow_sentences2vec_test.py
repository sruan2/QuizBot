import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
from sif_implementation.utils import *

print('done')
module_url = "https://tfhub.dev/google/universal-sentence-encoder/2"

# Universal Sentence Encoder'sentence TF Hub model
embed = hub.Module(module_url)
print('got here')
# word = "Elephant"
# sentence = "I am a sentence for which I would like to get its embedding."
# paragraph = (
# 	"Universal Sentence Encoder embeddings also support short paragraphs. "
# 	"There is no hard limit on how long the paragraph is. Roughly, the longer "
# 	"the more 'diluted' the embedding will be.")
# messages = [word, sentence, paragraph]

# with tf.Session() as session:
# 	session.run([tf.global_variables_initializer(), tf.tables_initializer()])
# 	message_embeddings = session.run(embed(messages))

# 	for i, message_embedding in enumerate(np.array(message_embeddings).tolist()):
# 		print("Message: {}".format(messages[i]))
# 		print("Embedding size: {}".format(len(message_embedding)))
# 		message_embedding_snippet = ", ".join(
# 			(str(x) for x in message_embedding[:3]))
# 		print("Embedding: [{}, ...]\n".format(message_embedding_snippet))

messages = [
		# numbers
		'5', 'five', '4','four',
		# true/false
		'true', 'yes', 'no', 'false',
		#capitalization
		'Hydrogen', 'hydrogen', 'Carbon', 'carbon',
		# A, B, A and B
		'carbon', 'carbon and hydrogen', 'hydrogen and carbon',
		# bonds
		'bond', 'covalent bonds',
		# human activity
		'human activity', 'careless human activity',
		# heat
		'heat', 'thermal energy',
		# atom nucleus
		'atom nucleus', 'the nucleus',
		# nuclear
		'nuclear', 'medulla',
		# A and B
		'reproduce asexually and sexually', 'reproduce sexually and asexually',
		# plural
		'2 hour', '2 hours']

def run_and_plot(session_, input_tensor_, messages_, encoding_tensor):
  	message_embeddings_ = session_.run(
      encoding_tensor, feed_dict={input_tensor_: messages_})
  	plot_similarity(messages_, message_embeddings_, 90, 'tensorflow_heatmap.png')

similarity_input_placeholder = tf.placeholder(tf.string, shape=(None))
similarity_message_encodings = embed(similarity_input_placeholder)

with tf.Session() as session:
	session.run([tf.global_variables_initializer(), tf.tables_initializer()])
	run_and_plot(session, similarity_input_placeholder, messages, 
           similarity_message_encodings)
	print('plotted this')

	# message_embeddings = session.run(embed(message))

	# for i, message_embedding in enumerate(np.array(message_embeddings).tolist()):
	# 	print("Message: {}".format(message[i]))
	# 	print("Embedding size: {}".format(len(message_embedding)))
	# 	message_embedding_snippet = ", ".join(
	# 		(str(x) for x in message_embedding[:3]))
	# 	print("Embedding: [{}, ...]\n".format(message_embedding_snippet))


