from keras.models import model_from_json

from supervised_model import fit_model, evaluate_model

# Model reconstruction from JSON file
with open('model_architecture.json', 'r') as f:
    model = model_from_json(f.read())

# Load weights into the new model
model.load_weights('model_weights.h5')

glove_file = 'mittens_model.pkl'
json_file = '../QAdataset/questions_filtered_150_quizbot.json'

emb = fit_model(glove_file, json_file)

# test_pair_one = ['you are right', 'you are right', 'true', 'yes', 'right', 'a mathemematician found a solution to the problem']
# test_pair_two = ['you are correct', 'you are wrong', 'yes', 'yes', 'correct', 'A problem was solved by a young mathematician']
test_pair_one = ['kinetic energy', 'central nervous system', 'central nervous system', 'this is true']
test_pair_two = ['thermal energy', 'neural', 'nervous', 'true']

test_scores = evaluate_model(model, emb, test_pair_one, test_pair_two)
# transform test scores so that its on a 0-1 scale
test_scores = (test_scores - 1) / 4

print(type(test_scores[0]))
for i,j,k in zip(test_pair_one, test_pair_two, test_scores):
	print('{}, {}, score: {}'.format(i,j,k))
