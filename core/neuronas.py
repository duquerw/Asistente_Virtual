# core/neuronas.py
import math
import random
import json

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def derivada_sigmoid(x):
    s = sigmoid(x)
    return s * (1 - s)

class Neurona:
    def __init__(self, n_in, n_hidden, n_out, lr=0.2):
        self.lr = lr
        self.w_ih = [[random.uniform(-1,1) for _ in range(n_in)] for _ in range(n_hidden)]
        self.b_h  = [random.uniform(-1,1) for _ in range(n_hidden)]
        self.w_ho = [[random.uniform(-1,1) for _ in range(n_hidden)] for _ in range(n_out)]
        self.b_o  = [random.uniform(-1,1) for _ in range(n_out)]

    def forward(self, x):
        # calcular activaciones de capa oculta
        self.x = x[:]  
        self.z_h = []
        self.a_h = []
        for i in range(len(self.w_ih)):
            z = sum(self.x[j] * self.w_ih[i][j] for j in range(len(self.x))) + self.b_h[i]
            self.z_h.append(z)
            self.a_h.append(sigmoid(z))
        
        # calcular activaciones de capa de salida
        self.z_o = []
        self.a_o = []
        for i in range(len(self.w_ho)):
            z = sum(self.a_h[j] * self.w_ho[i][j] for j in range(len(self.a_h))) + self.b_o[i]
            self.z_o.append(z)
            self.a_o.append(sigmoid(z))
        
        return self.a_o[:]

    def backward(self, y_true):
        # gradiente de salida (error * derivada)
        delta_o = [(self.a_o[i] - y_true[i]) * derivada_sigmoid(self.z_o[i])
                   for i in range(len(self.a_o))]

        # gradientes para w_ho y b_o
        dw_ho = [[delta_o[i] * self.a_h[j] 
                  for j in range(len(self.a_h))] 
                 for i in range(len(delta_o))]
        db_o  = delta_o[:]

        # propagar al nivel oculto
        delta_h = []
        for j in range(len(self.a_h)):
            error = sum(delta_o[i] * self.w_ho[i][j] for i in range(len(delta_o)))
            delta_h.append(error * derivada_sigmoid(self.z_h[j]))

        # gradientes para w_ih y b_h
        dw_ih = [[delta_h[j] * self.x[i] 
                  for i in range(len(self.x))] 
                 for j in range(len(delta_h))]
        db_h  = delta_h[:]

        return dw_ih, db_h, dw_ho, db_o

    def update_params(self, dw_ih, db_h, dw_ho, db_o):
        # actualizar pesos entrada→oculta
        for i in range(len(self.w_ih)):
            for j in range(len(self.w_ih[0])):
                self.w_ih[i][j] -= self.lr * dw_ih[i][j]
        
        # actualizar bias oculto
        for i in range(len(self.b_h)):
            self.b_h[i] -= self.lr * db_h[i]
        
        # actualizar pesos oculta→salida
        for i in range(len(self.w_ho)):
            for j in range(len(self.w_ho[0])):
                self.w_ho[i][j] -= self.lr * dw_ho[i][j]
        
        # actualizar bias salida
        for i in range(len(self.b_o)):
            self.b_o[i] -= self.lr * db_o[i]

    def train(self, X, Y, epochs=1000):
        for epoch in range(epochs):
            total_loss = 0
            for x, y in zip(X, Y):
                y_pred = self.forward(x)
                # MSE como ejemplo de función de pérdida
                loss = sum((y_pred[i] - y[i])**2 for i in range(len(y))) / len(y)
                total_loss += loss
                grads = self.backward(y)
                self.update_params(*grads)
            if epoch % 100 == 0:
                print(f"Epoch {epoch:4d}  Loss: {total_loss/len(X):.4f}")

    def save(self, path):
        data = {
            "w_ih": self.w_ih, "b_h": self.b_h,
            "w_ho": self.w_ho, "b_o": self.b_o,
            "lr": self.lr
        }
        with open(path, "w") as f:
            json.dump(data, f)

    @classmethod
    def load(cls, path):
        with open(path) as f:
            data = json.load(f)
        n_in  = len(data["w_ih"][0])
        n_h   = len(data["w_ih"])
        n_out = len(data["w_ho"])
        nn = cls(n_in, n_h, n_out, lr=data["lr"])
        nn.w_ih, nn.b_h = data["w_ih"], data["b_h"]
        nn.w_ho, nn.b_o = data["w_ho"], data["b_o"]
        return nn
