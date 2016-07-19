from __future__ import division
import json

def linspace(a,b,n):
    """return n points between a and b, inclusive"""
    xs = range(0,n)
    xs = [x*(b-a)/(n-1) for i, x in enumerate(xs)]
    xs = [x+a for x in xs]
    return xs

class Design_Generator():
    def __init__(self, json_blob, verbose=False):
        self.design_space_tree = json.loads(json_blob)
        self.verbose = verbose
        self.build_tree()

    def convert_leaf_to_list(self, leaf):
        """Given a leaf from the designs_descriptions, returns a list-like object to be the values at that leaf"""
        if leaf["type"]=='range':
            d = leaf["data"]
            vals = linspace(float(d[0]),float(d[1]),int(d[2]))
        elif leaf["type"]=='set':
            vals = leaf['data']
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
