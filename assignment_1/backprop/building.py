from collections import defaultdict

class Builder():
    
    def __init__(self, infix: list, in_vars: dict = {}):
        """
        infix: list of infix notation parse, e.g. [['exp', 2], '-', 3]
        in_vars: dict of input variables to ensure they are not used as intermediate or output variables
        RETURN: computation graph in a data structure of your choosing
        """

        ## some alphabetical vars to use as intermediate and output variables minus the input vars to avoid duplicates
        avail_vars = list(map(chr, range(97, 123))) + list(map(chr, range(945, 969)))
        if len(in_vars.keys()) > 0:
            avail_vars = set(avail_vars) - set(in_vars)
        self.avail_vars = sorted(list(set(avail_vars)), reverse=True)

        self.infix = infix

        self.parent: dict = {} # key: node, value: parent(s)
        self.operation: dict = {}
        self.root = self.build_graph(infix)
        self.graph = (self.parent, self.operation, self.root)



    def build_graph(self, infix):
        if not isinstance(infix, list):

            # Stop recursion 
            return infix

        var_name = self.avail_vars.pop()
        
        if len(infix) == 3: # binary operation
            arg_1, operator, arg_2 = infix
            self.operation[var_name] = operator

            # Perform recursion
            parent_1 = self.build_graph(arg_1)
            parent_2 = self.build_graph(arg_2)

            # Update parent list
            self.parent[var_name] = [parent_1, parent_2]

        elif len(infix) == 2: # binary operation
            operator, arg_1 = infix
            self.operation[var_name] = operator

            # Perform recursion
            parent_1 = self.build_graph(arg_1)

            # Update parent list
            self.parent[var_name] = [parent_1]

        return var_name
        

if __name__ == '__main__':
   pass