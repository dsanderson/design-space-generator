import requests, json

## Ensure both the generator and server are running before executing

def test_server_ideal():
    print "Creating design space..."
    blob = json.dumps(
        {'type':'product','children':[
            {'type':'product','children':[
                {'type':'set','label':'test_set','data':['a','b','c']},
                {'type':'range','label':'test_range','data':[1,2,3]}]},
            {'type':'range','label':'test_range','data':[4,5,6]}]})
    r = requests.put('http://localhost:5000/space',data=blob)
    assert r.status_code == 200
    print "Design space creation OK!"
    print "Testing stats function..."
    r = requests.get('http://localhost:5000/stats')
    data = json.loads(r.text)
    size = data['size']
    print "Server status {}, {} designs".format(data['status'],data['size'])
    print "Stats OK!"
    print "Testing direct indexing..."
    s=set()
    r = requests.get('http://localhost:5000/design')
    d0 = r.text
    r = requests.get('http://localhost:5000/design/0')
    d0_direct = r.text
    assert d0 == d0_direct
    print "Direct indexing OK!"
    s.add(d0)
    print "Testing full design space..."
    while r.status_code == 200:
        r = requests.get('http://localhost:5000/design')
        s.add(r.text)
    print size, len(s)
    print "Design space OK!"

if __name__=='__main__':
    test_server_ideal()
