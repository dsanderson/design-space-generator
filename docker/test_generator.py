import json
import generator

def test_range_node():
    blob = json.dumps({'type':'range','label':'test_range','data':[1,2,6]})
    dg = generator.Design_Generator(blob)
    #print len(dg)
    dg.print_tree()

def test_set_node():
    blob = json.dumps({'type':'set','label':'test_set','data':['a','b','c']})
    dg = generator.Design_Generator(blob)
    #print len(dg)
    dg.print_tree()

def test_sum():
    blob = json.dumps({'type':'sum','children':[
        {'type':'set','label':'test_set','data':['a','b','c']},
        {'type':'range','label':'test_range','data':[1,2,3]}]})
    dg = generator.Design_Generator(blob)
    #print len(dg)
    dg.print_tree()

def test_sum():
    blob = json.dumps({'type':'sum','children':[
        {'type':'set','label':'test_set','data':['a','b','c']},
        {'type':'range','label':'test_range','data':[1,2,3]}]})
    dg = generator.Design_Generator(blob)
    #print len(dg)
    dg.print_tree()

def test_product():
    blob = json.dumps({'type':'product','children':[
        {'type':'set','label':'test_set','data':['a','b','c']},
        {'type':'range','label':'test_range','data':[1,2,3]}]})
    dg = generator.Design_Generator(blob)
    #print len(dg)
    dg.print_tree()

def test_all():
    blob = json.dumps(
        {'type':'sum','children':[
            {'type':'product','children':[
                {'type':'set','label':'test_set','data':['a','b','c']},
                {'type':'range','label':'test_range','data':[1,2,3]}]},
            {'type':'range','label':'test_range','data':[4,5,6]}]})
    dg = generator.Design_Generator(blob)
    #print len(dg)
    # dg.print_tree()
    # print ''
    blob = json.dumps(
        {'type':'product','children':[
            {'type':'product','children':[
                {'type':'set','label':'test_set','data':['a','b','c']},
                {'type':'range','label':'test_range','data':[1,2,3]}]},
            {'type':'range','label':'test_range','data':[4,5,6]}]})
    dg = generator.Design_Generator(blob)
    print len(dg)
    #dg.print_tree()
    d = dg.get_design(0)
    print d
    d = dg.get_design(1)
    print d
    d = dg.get_design(2)
    print d
    d = dg.get_design(3)
    print d
    s=set()
    for i in xrange(0,len(dg)):
        d = dg.get_design(i)
        #print d, type(d)
        #t = tuple(d)
        j = json.dumps(d)
        s.add(j)
    print len(s), len(dg)
        

if __name__=='__main__':
    #test_range_node()
    #print '\n'
    #test_set_node()
    #print '\n'
    #test_sum()
    #print '\n'
    #test_product()
    #print '\n'
    test_all()
