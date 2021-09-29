from datetime import date
import spacy
import spacy.attrs
from DatabaseConnector import DatabaseConnector
from collections import Counter

class AnalyticsConnector():
   stop_list = ['z.B.', 'z.', 'B.' '\n ', '\n\n', '\xa0', '\xa0\n', '|', '\xa0 \xa0', '\n\n ', '\xa0 ', '\n\n\n', '\n\xa0', 'm', 'w', 'd', '+49']
   nlp = None
   
   def __init__(self):
      self.nlp =  spacy.load("de_core_news_lg")
      for word in self.stop_list:
         self.nlp.vocab[word].is_stop = True

   def common_words(self, ok_list: list, job: str, city: str, radius: int, start_date: date, end_date: date) -> list:
      main_text = ""
      counter = 0
      datebase_connector = DatabaseConnector()
      for table_name in ok_list:
         for row in datebase_connector.get_filtered_data(table_name, job, city, radius, start_date, end_date):
            main_text += row["content"].replace('\n','')
            counter += 1

      if len(main_text) > 1000000:
         return {"nouns": [], "verbs": [], "propn": [], "nums": [], "counter": []}
      else:
         doc = self.nlp(main_text)

         nouns = Counter([token.text
                  for token in doc
                     if (not token.is_stop and
                     not token.is_punct and
                     token.pos_ == "NOUN")]).most_common(100)

         verbs = Counter([token.text
                  for token in doc
                  if (not token.is_stop and
                     not token.is_punct and
                     token.pos_ == "VERB")]).most_common(100)

         propn = Counter([token.text
                  for token in doc
                     if (not token.is_stop and
                        not token.is_punct and
                        token.pos_ == "PROPN")]).most_common(100)
         
         nums = Counter([token.text
                  for token in doc
                     if (not token.is_stop and
                        not token.is_punct and
                        token.pos_ == "NUM")]).most_common(100)

         return {"nouns": nouns, "verbs": verbs, "propn": propn, "nums": nums, "counter": counter}
      

if __name__ == '__main__':
   analytics_connector = AnalyticsConnector()
   analytics_connector.common_words()