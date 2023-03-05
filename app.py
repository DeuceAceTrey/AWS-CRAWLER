from flask import *
from flask_cors import CORS
import json
from getFromDB import getAllTargets
from getFromDB import removeTargetUrl
from getFromDB import insertTargetUrl
from getFromDB import updateTargetUrl
app = Flask(__name__,
static_folder='./templates/static')
app.debug = True
CORS(app)

@app.route('/' , methods = ['GET','POST'])
def index():
    targets = getAllTargets()
    print(targets)
    return render_template('index.html',targets = targets)

@app.route('/addTarget',methods=['GET','POST'])
def addTarget():
    data = json.loads(request.data)
    target_url = data['target_url']
    insertTargetUrl(target_url)
    targets = getAllTargets()
    return  jsonify(data={'success':True,'targets':targets}), 201

@app.route('/updateTarget',methods=['GET','POST'])
def updateTarget():
    data = json.loads(request.data)
    target_url = data['target_url']
    origin_url = data['origin_url']
    updateTargetUrl(target_url , origin_url)
    targets = getAllTargets()
    return  jsonify(data={'success':True,'targets':targets}), 201

@app.route('/removeTarget',methods=['GET','POST'])
def removeTarget():
    data = json.loads(request.data)
    target_url = data['target_url']
    removeTargetUrl(target_url)
    targets = getAllTargets()
    return  jsonify(data={'success':True,'targets':targets}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)