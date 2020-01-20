from flask import Flask, json
from random import randint
import sys

app=Flask(__name__)

@app.route("/diceroll/<num>/<sides>")
def diceroll(num, sides):
  total=0
  for count in range(0,int(num)):
    die=randint(1,int(sides))
    total=die+total
    print(count,die)
  return app.response_class(response=json.dumps(total), status=200, mimetype='application/json')
  
  
app.run(host=sys.argv[1])