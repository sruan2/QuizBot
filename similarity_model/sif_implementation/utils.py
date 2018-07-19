import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def preprocess(sentences, tokenizer):
    return [tokenizer.tokenize(q.lower()) for q in sentences]

def cosine_similarity(v1, v2):
    similarity = (np.dot(v1, v2.T) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    return similarity
    #return int(((np.dot(v1, v2.T) / (np.linalg.norm(v1) * np.linalg.norm(v2)))+1)*5) # shape is (0,10)

def plot_similarity(labels, features, rotation, savefile):
  corr = np.inner(features, features)
  sns.set(font_scale=1.2)
  g = sns.heatmap(
      corr,
      xticklabels=labels,
      yticklabels=labels,
      vmin=0,
      vmax=1,
      cmap="YlOrRd")
  g.set_xticklabels(labels, rotation=rotation)
  g.set_title("Semantic Textual Similarity")
  plt.show()
  g.figure.savefig(savefile)
