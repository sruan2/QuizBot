from gensim.models import Doc2Vec

class qa_model():

    def __init__(self, PreTrainedModel):
    	self.MODEL = Doc2Vec.load(PreTrainedModel) # load model in the very beginning
