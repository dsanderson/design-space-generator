import json
import server

def test_range_node():
    blob = json.dumps({'type':'range','label':'test_range','data':[1,2,6]})
    dg = server.Design_Generator(blob)
    #print len(dg)
    dg.print_tree()

def test_set_node():
    blob = json.dumps({'type':'set','label':'test_set','data':['a','b','c']})
    dg = server.Design_Generator(blob)
    #print len(dg)
    dg.print_tree()

def test_sum():
    blob = json.dumps({'type':'sum','children':[
        {'type':'set','label':'test_set','data':['a','b','c']},
        {'type':'range','label':'test_range','data':[1,2,3]}]})
    dg = server.Design_Generator(blob)
    #print len(dg)
    dg.print_tree()

def test_sum():
    blob = json.dumps({'type':'sum','children':[
        {'type':'set','label':'test_set','data':['a','b','c']},
        {'type':'range','label':'test_range','data':[1,2,3]}]})
    dg = server.Design_Generator(blob)
    #print len(dg)
    dg.print_tree()

def test_product():
    blob = json.dumps({'type':'product','children':[
        {'type':'set','label':'test_set','data':['a','b','c']},
        {'type':'range','label':'test_range','data':[1,2,3]}]})
    dg = server.Design_Generator(blob)
    #print len(dg)
    dg.print_tree()

def test_all():
    blob = json.dumps(
        {'type':'sum','children':[
            {'type':'product','children':[
                {'type':'set','label':'test_set','data':['a','b','c']},
                {'type':'range','label':'test_range','data':[1,2,3]}]},
            {'type':'range','label':'test_range','data':[4,5,6]}]})
    dg = server.Design_Generator(blob)
    #print len(dg)
    dg.print_tree()
    print ''
    blob = json.dumps(
        {'type':'product','children':[
            {'type':'product','children':[
                {'type':'set','label':'test_set','data':['a','b','c']},
                {'type':'range','label':'test_range','data':[1,2,3]}]},
            {'type':'range','label':'test_range','data':[4,5,6]}]})
    dg = server.Design_Generator(blob)
    #print len(dg)
    dg.print_tree()

if __name__=='__main__':
    test_range_node()
    print '\n'
    test_set_node()
    print '\n'
    test_sum()
    print '\n'
    test_product()
    print '\n'
    test_all()
