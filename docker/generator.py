from __future__ import division
from multiprocessing.connection import Listener
import json

def linspace(a,b,n):
    """return n points between a and b, inclusive"""
    xs = range(0,n)
    xs = [x*(b-a)/(n-1) for i, x in enumerate(xs)]
    xs = [x+a for x in xs]
    return xs

class Design_Generator():
    def __init__(self, verbose=False):
        self.address = ('localhost',6345)
        self.verbose = verbose
        self.status = 'uninitialized'
        self.design_counter = 0
        self.run_server()

    def run_server(self):
        """function that loops forever, running a socket-based server that communicates to a flask script allowing a REST API"""
        listener = Listener(self.address)
        print "Listening at {}:{}...".format(self.address[0],self.address[1])
        while True:
            conn = listener.accept()
            if self.verbose:
                print "New connection from {}".format(listener.last_accepted)
            command = conn.recv()
            if command[0] == 'create':
                json_blob = command[1]
                self.design_space_tree = json.loads(json_blob)
                self.build_tree()
                self.design_counter = 0
                self.status = 'ok'
                conn.send(['ok',None])
                conn.close()
            elif command[0] == 'get_next_index':
                if self.status == 'ok' and self.__len__()>self.design_counter:
                    conn.send(['ok',self.design_counter])
                    self.design_counter += 1
                    if not self.__len__()>self.design_counter:
                        self.status = 'exhausted'
                else:
                    conn.send([self.status,None])
                conn.close()
            elif command[0] == 'get_design':
                if self.status != 'uninitialized' and self.__len__()>command[1]:
                    conn.send(['ok',self.get_design(command[1])])
                else:
                    conn.send(['fail',None])
                conn.close()
            elif command[0] == 'get_stats':
                if self.status != 'unitialized':
                    payload = (self.design_counter, self.__len__())
                conn.send([self.status,payload])
                conn.close()
            else:
                conn.close()

    def convert_leaf_to_list(self, leaf):
        """Given a leaf from the designs_descriptions, returns a list-like object to be the values at that leaf"""
        if leaf['type']=='range':
            d = leaf['data']
            vals = linspace(float(d[0]),float(d[1]),int(d[2]))
        elif leaf['type']=='set':
            vals = leaf['data']
        elif leaf['type']=='search':
            raise NotImplementedError
        else:
            raise NotImplementedError
        return vals

    def convert_leafs(self, node):
        if 'children' in node.keys():
            for c in node['children']:
                self.convert_leafs(c)
        else:
            vals = self.convert_leaf_to_list(node)
            node['values'] = vals
            node['size'] = len(vals)

    def calc_sizes(self, node):
        if 'size' in node.keys():
            return node['size']
        else:
            if node['type']=='sum':
                size = 0
                for c in node['children']:
                    size+=self.calc_sizes(c)
                node['size']=size
                return size
            elif node['type']=='product':
                size = 1
                for c in node['children']:
                    size = size*self.calc_sizes(c)
                node['size']=size
                return size

    def build_tree(self):
        #pass 1: identify leaf nodes, and get the value object and size of that node
        self.convert_leafs(self.design_space_tree)
        #pass 2: calculate the sizes of nodes through the tree
        self.calc_sizes(self.design_space_tree)

    def __len__(self):
        return self.design_space_tree['size']

    def print_tree(self):
        self.print_tree_rec(self.design_space_tree,0)

    def print_tree_rec(self, node, depth):
        tabs = '\t'*depth
        ks = node.keys()
        ks.sort()
        for k in ks:
            if k!='children':
                print tabs+'{}: {}'.format(k,node[k])
        if 'children' in node.keys():
            for c in node['children']:
                self.print_tree_rec(c,depth+1)
                print ''

    def get_design(self, index):
        return self.get_design_rec(self.design_space_tree, index)

    def get_design_rec(self, node, index):
        if node['type']=='range' or node['type']=='set':
            return [{'label':node['label'],'data':node['values'][index]}]
        if node['type']=='sum':
            # based on the length of the
            total = 0
            i = 0
            while total<index and i<len(node['children']):
                total += node['children'][i]['size']
                i += 1
            new_i = i-1
            new_index = index - total + node['children'][new_i]['size']
            new_node = node['children'][new_i]
            return self.get_design_rec(new_node, new_index)
        if node['type']=='product':
            ret = []
            temp_index = index
            for c in node['children']:
                i = temp_index%c['size']
                ret = ret+self.get_design_rec(c, i)
                temp_index = int(temp_index/c['size'])
            return ret

if __name__ == '__main__':
    dg = Design_Generator(verbose=True)
