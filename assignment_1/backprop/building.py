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

        is_parent_from: dict = {}
        has_operation: dict = {}
        self.graph = self.build_graph(infix)


    def build_graph(self, infix):
        var_name = self.avail_vars.pop()
        if len(self.infix) == 3:
            arg_1, operator, arg_2 = self.infix
            self.has_operation[var_name] = operator

            # Perform recursion
            child_1 = self.build_graph(arg_1)
            child_2 = self.build_graph(arg_2)
            self.is_parent_from[var_name] += [child_1, child_2]

        elif len(self.infix) == 2:
            arg_1, operator = self.infix
            self.has_operation[var_name] = operator
            
            # Perform recursion
            child_1 = self.build_graph(arg_1)
            self.is_parent_from[var_name] 
            self.is_parent_from[var_name] += [child_1]
            
        else:
            return self.infix

        return var_name
        







if __name__ == '__main__':
   pass