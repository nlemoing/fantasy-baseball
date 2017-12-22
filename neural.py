from baseball import initialize, getoutput, getinput
import numpy as np


class Network:
    def __init__(self, sizes):
        self.sizes = sizes
        self.numlayers = len(sizes)
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]
    def propagate(self, inp, out, lr):
        z = inp
        zs = [inp]
        for w, b in zip(self.weights, self.biases):
            z = np.dot(w, z) + b
            zs.append(z)
        deltab = [np.zeros(b.shape) for b in self.biases]
        deltaw = [np.zeros(w.shape) for w in self.weights]
        delta = z - out
        for l in range(1, self.numlayers):
            deltab[-l] = delta
            deltaw[-l] = np.dot(delta, zs[-l-1].transpose())
            delta = np.dot(self.weights[-l].transpose(), delta)
        self.weights = [w - (lr * nw) for w, nw in zip(self.weights, deltaw)]
        self.biases = [b - (lr * nb) for b, nb in zip(self.biases, deltab)]
    def mse(self, trainingdata):
        error = 0
        count = 0
        for data in trainingdata:
            inp = data[0]
            out = data[1]
            for i in range(self.numlayers - 1):
                w = self.weights[i]
                b = self.biases[i]
                inp = np.dot(w, inp) + b
            count += 1
            error += np.linalg.norm(inp - out)
        error /= count
        return error

def neural(targetyear, projectionyears, pitching, epoch):
    #aggregate training data
    initialize(targetyear - projectionyears, targetyear, pitching) #initialize baseball data
    targetdata = getoutput()
    projectiondata = getinput()
    trainingdata = []
    outputsize = 5
    inputsize = 15 * projectionyears
    hiddensize = (outputsize + inputsize)//2
    for name in targetdata.keys():
        inp = []
        try:
            for year in range(projectionyears):
                inp.extend(projectiondata[year][name])
            out = targetdata[name]
            data = (np.matrix(inp).transpose(), np.matrix(out).transpose())
            trainingdata.append(data)
        except KeyError:
            continue
    net = Network([inputsize, hiddensize, outputsize])
    for it in range(epoch):
        for data in trainingdata:
            net.propagate(data[0], data[1], 0.001)
        error = net.mse(trainingdata)
        print("Epoch {} error: {}".format(it + 1, error))

neural(2017, 3, False, 50)
