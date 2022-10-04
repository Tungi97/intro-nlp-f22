# from turtle import forward
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
        self.f = {}
        self.parent, self.operation, self.root = self.graph
        self.grad_cache = {("root", "root"): 1} # key: (from, to), value: ∂from/∂to

    ## forward execution____________________________

    def forward(self, ):
        self.output = self.forward_helper(self.root)

    def forward_helper(self, current):
        if not current in self.parent:
            self.f[str(current)] = current if isinstance(current, int) else self.in_vars[current]

        else:
            op = self.operation[current]
            if len(self.parent[current]) == 2:
                parent_1 = self.parent[current][0]
                parent_2 = self.parent[current][1]
                self.f[current] = self.fn_map[op].f(self.forward_helper(parent_1), self.forward_helper(parent_2))

            else:
                parent_1 = self.parent[current][0]
                self.f[current] = self.fn_map[op].f(self.forward_helper(parent_1))

        return self.f[current]

    ## backward execution____________________________

    def backward(self, ):
        self.derivative = self.backward(self.root)
    
    def backward_helper(self, current, prev=None):
        if prev is None:
            prev = self.root

        if current not in self.parent[current]:
            return
        
        op = self.operation[current]
        if len(self.parent[current]) == 2: # binary operation
            parent_1, parent_2 = self.parent[current]

            # TODO: check if leaf is a scalar
            f_parent_1 = 0 if isinstance(parent_1, int) else self.f[parent_1]
            f_parent_2 = 0 if isinstance(parent_2, int) else self.f[parent_2]

            prev_df = self.grad_cache[(self.root, prev)]
            df_list = self.fn_map[op].df(f_parent_1, f_parent_2)
            df_1, df_2 = [prev_df * df for df in df_list]

            self.update_grad_cache(current, parent_1, df_1)
            self.update_grad_cache(current, parent_2, df_2)

            self.backward_helper(parent_1, current)
            self.backward_helper(parent_2, current)
        else:
            parent_1 = self.parent[current]

            f_parent_1 = 0 if isinstance(parent_1, int) else self.f[parent_1]

            prev_df = self.grad_cache[(self.root, prev)]
            df_list = self.fn_map[op].df(f_parent_1)
            df_1 = [prev_df * df for df in df_list]

            self.update_grad_cache(current, parent_1, df_1)
            self.backward_helper(parent_1, current)



    def update_grad_cache(self, current, parent, df):
        if not (current, parent) in self.grad_cache:
            self.grad_cache[(current, parent)] = df
        else:
            self.grad_cache[(current, parent)] += df








if __name__ == '__main__':
    pass