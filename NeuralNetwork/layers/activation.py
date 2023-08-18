from . import Layer
from NeuralNetwork.tools import trace


class ActivationLayer(Layer):
    def __init__(self, activation_function):
        self.activation_function = activation_function
        super().__init__()

    @trace()
    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = self.activation_function(self.input)
        return self.output

    @trace()
    def backward_propagation(self, output_error, learning_rate, y_true):
        return self.activation_function(self.input, prime=True) * output_error