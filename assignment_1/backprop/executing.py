from turtle import forward
from numpy import isin
from operations import *

class Executor():

    def __init__(self, graph: dict, in_vars: dict = {}):
        """
        graph: computation graph in a data structure of your choosing
        in_vars: dict of input variables, e.g. {"x": 2.0, "y": -1.0}
        """
        self.graph = graph
        self.in_vars = in_vars
        self.fn_map = {"log": Log(), "exp": Exp(), "+": Add(), "-": Sub(), "^": Pow(), "sin": Sin(), "*": Mult(), "/": Div()}
        self.output = -1
        self.derivative = {}

        self.f = {} # Contains values of forward propagation
        self.parent, self.operation, self.root = self.graph
        self.grad_cache = {} # key: (from, to), value: ∂from/∂to

    ## forward execution____________________________

    def forward(self, ):
        self.output = self.forward_helper(self.root)

    def forward_helper(self, current):
        if not current in self.parent:

            # Stop recursion if current has no parents
            self.f[str(current)] = current if isinstance(current, int) else self.in_vars[current]

        else:
            op = self.operation[current]
            if len(self.parent[current]) == 2:
                parent_1 = self.parent[current][0]
                parent_2 = self.parent[current][1]

                # Recurse
                self.f[current] = self.get_f(op, self.forward_helper(parent_1), self.forward_helper(parent_2))

            else:
                parent_1 = self.parent[current][0]

                # Recurse
                self.f[current] = self.get_f(op, self.forward_helper(parent_1))

        return self.f[str(current)]

    ## backward execution____________________________

    def backward(self, ):
        self.backward_helper(self.root)
        for var in self.in_vars.keys():
            self.derivative[var] = self.grad_cache[(self.root, var)]
    
    def backward_helper(self, current, prev=None):
        if current not in self.parent:
            return
        
        op = self.operation[current]
        if len(self.parent[current]) == 2: # binary operation

            parent_1, parent_2 = self.parent[current]

            f_parent_1 = self.f[str(parent_1)]
            f_parent_2 = self.f[str(parent_2)]

            prev_df = self.get_prev_df(current, prev)
            df_1, df_2 = [prev_df * df for df in self.get_df(op, f_parent_1, f_parent_2)]

            self.update_grad_cache(self.root, parent_1, df_1)
            self.update_grad_cache(self.root, parent_2, df_2)

            self.backward_helper(parent_1, current)
            self.backward_helper(parent_2, current)
        else:

            parent_1 = self.parent[current][0]
            f_parent_1 = self.f[parent_1]

            prev_df = self.get_prev_df(current, prev)
            df_list = self.get_df(op, f_parent_1)
            df_1 = [prev_df * df for df in df_list][0]

            self.update_grad_cache(self.root, parent_1, df_1)
            self.backward_helper(parent_1, current)

    def update_grad_cache(self, root, parent, df):
        if not (root, parent) in self.grad_cache:
            self.grad_cache[(root, parent)] = df
        else:
            self.grad_cache[(root, parent)] += df
    
    def get_f(self, op, arg_1, arg_2=None):
        if arg_2 is None:
            return self.fn_map[op].f(arg_1)
        else:
            return self.fn_map[op].f(arg_1, arg_2)

    def get_df(self, op, arg_1, arg_2=None):
        if arg_2 is None:
            return self.fn_map[op].df(arg_1)
        else:
            return self.fn_map[op].df(arg_1, arg_2)

    def get_prev_df(self, current, prev):
        return 1 if prev is None else self.grad_cache[(self.root, current)]

        

if __name__ == '__main__':
    pass