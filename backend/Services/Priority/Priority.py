import spacy
from tensorflow.keras.models import load_model

class PriorityModel:
  def __init__(self, model_path = "Services/Priority/nn_model.keras"):
    self.nlp = spacy.load('en_core_web_lg')
    self.model = load_model(model_path)
    self.power_up_word = 'my train'
    self.weights = {
      'sanitation': 1.1,
      'tickets and booking': 1,
      'electrical': 1.2,
      'security': 1.3,
      'medical': 1.4
  }

  def generate_embeddings(self, text):
    embeddings = self.nlp(text).vector

    return embeddings

  def get_score(self, text):
    inp = self.generate_embeddings(text)
    inp = inp.reshape(1, -1)

    return self.model.predict(inp)

  def calculate_priority(self, content, dept, age_of_complaint, number_of_similar_complaints):
    '''
    content: Details of the complaint
    dept: department into which the complaint has been categorized
    age_of_complaint: how old is the complaint in days
    number_of_similar_complaints: number of similar complaints in the department
    '''
    score = self.get_score(content)[0]
    out = self.weights[dept]*score + age_of_complaint + number_of_similar_complaints

    return out
