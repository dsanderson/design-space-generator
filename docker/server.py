import json
from multiprocessing.connection import Client
from flask import Flask
from flask import request
from flask import Response
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/space", methods = ['PUT'])
def create_space():
    reply = communicate(['create',request.data])
    if reply[0]=='ok':
        resp = Response('ok', status=200, mimetype='application/json')
        return resp
    else:
        resp = Response('ok', status=404, mimetype='application/json')
        return resp

@app.route("/design", methods = ['GET'])
def get_next_design():
    reply = communicate(['get_next_index'])
    if reply[0] == 'ok':
        index = reply[1]
        reply = communicate(['get_design',index])
        if reply[0] == 'ok':
            res = {'status':reply[0], 'id':index, 'design':reply[1]}
            js = json.dumps(res)
            resp = Response(js, status=200, mimetype='application/json')
            return resp
    #fall back to a 404
    resp = Response('404', status=404, mimetype='application/json')
    return resp

@app.route("/design/<int:index>", methods = ['GET'])
def get_design(index):
    reply = communicate(['get_design',index])
    if reply[0] == 'ok':
        res = {'status':reply[0], 'id':index, 'design':reply[1]}
        js = json.dumps(res)
        resp = Response(js, status=200, mimetype='application/json')
        return resp
    resp = Response('404', status=404, mimetype='application/json')
    return resp

@app.route("/stats", methods = ['GET'])
def get_stats():
    reply = communicate(['get_stats'])
    #convert the reply into a json blob
    res = {'status':reply[0],'size':reply[1][1],'position':reply[1][0]}
    js = json.dumps(res)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

def communicate(message):
    address = ('localhost',6345)
    conn = Client(address)
    conn.send(message)
    reply = conn.recv()
    conn.close()
    return reply

if __name__ == "__main__":
    app.run(host='0.0.0.0')
