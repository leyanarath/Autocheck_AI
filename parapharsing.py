from sentence_transformers import SentenceTransformer
from sentence_transformers import SentenceTransformer, util
import sqlite3
import re

def Para(user):
  conn =sqlite3.connect('autocheck.db')
  c=conn.cursor()   
  if(conn):
      print("sucess")
      #cur.execute ("CREATE TABLE IF NOT EXISTS res ({column_name} TEXT);")
  c.execute("""SELECT questionp.answer,ans.answer,questionp.mark,questionp.qno
FROM questionp
INNER JOIN ans ON questionp.qno=ans.qusid;
""")
  data=c.fetchall()
  for row in data:
    answerkey=row[0]
    answer=row[1]
    qno=row[3]
    def extract_enclosed_strings(paragraph):
      pattern = r'\*(.*?)\*'
      matches = re.findall(pattern, paragraph)
      return matches
    enclosed_strings = extract_enclosed_strings(answerkey)
    print(enclosed_strings)
    if (element in answer for element in enclosed_strings):
      print(answer)
      model = SentenceTransformer('distilbert-base-nli-mean-tokens')
      sentences = [answerkey,answer]
      sentence_embeddings = model.encode(sentences)
      tensor = util.pytorch_cos_sim(sentence_embeddings[0], sentence_embeddings[1])
      value=tensor.item()
      print(value)
      print(row[2])
      if (value>0.75):
        mark=round(value*row[2],2)
        print(mark)
        print(qno)
        c.execute("insert into mark values(?,?,?,?)",(qno,mark,row[2],user))
        conn.commit()
    #mark=c.fetchone()[0]
  conn.close()
  
  #return value
#Para(101)