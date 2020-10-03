import numpy as np

# TODO: Save activations
# TODO: Implement back propagation
# TODO: Implement gradient decent
# TODO: Implement training
# TODO: Train with some dummy data
# TODO: Make some predictions


class MLP:
    """Multilayer Perceptron Class"""
    def __init__(self, num_inputs=4, num_hidden_layers=[3, 5], num_outputs=2):
        """Constructor for MLP. Takes the number of inputs, hidden layers and outputs
           :param int num_inputs: Number of inputs to neural net
           :param list num_hidden_layers: Each entry is the number of neurons in a layer,total is size of array
           :param int num_outputs: Number of outputs to neural net
        """
        self.num_inputs = num_inputs
        self.num_hidden_layers = num_hidden_layers
        self.num_outputs = num_outputs

        # Cast inputs and outputs to list the join to single list
        layers = [self.num_inputs] + self.num_hidden_layers + [self.num_outputs]
        # print("num inputs: ", [self.num_inputs])
        # print("Layers: ", layers)

        # Initiate random weights
        self.weights = []
        # Iterate through all the layers and create weights
        # print("layers length: ", len(layers))
        for i in range(len(layers)-1):
            # Build weight matrices "w" of shape [x,y] with values between 0 and 1
            # Number of rows = current layer
            # Number of columns = number of neurons in next layer
            w = np.random.rand(layers[i], layers[i+1])
            print("weight matrix: ", w)
            self.weights.append(w)  # Add newly created data to weights list (creates list of arrays)
        print("\n")

        activations = []
        for i in range(len(layers)):
            a = np.zeros(layers[i])
            activations.append(a)
        self.activations = activations

        derivatives = []
        for i in range(len(layers)-1):
            d = np.zeros((layers[i], layers[i+1]))
            derivatives.append(d)
        self.derivatives = derivatives

    def forward_propagation(self, inputs):
        """Computes the forward propagation of the network based on inputs
        :param array inputs: inputs signals
        :returns array activations: output values
        """
        # The first layer number of activation = number of inputs
        activations = inputs
        self.activations[0] = inputs
        for i, w in enumerate(self.weights):
            # Calculate net inputs
            # Net inputs are activation of the previous layer multiplied by the weights
            net_inputs = np.dot(activations, w)

            # Apply sigmoid activation function
            activations = self._sigmoid(net_inputs)
            print("Activations: ", activations)
            self.activations[i+1] = activations
        print("\n")
        return activations

    def back_propagation(self, error, verbose=False):
        # dE/dW_i = (y - a_[i+1]) s'(h_[i+1])) a_i
        # s'(h_[i+1]) = s(h_[i+1])(1 - s(h_[i+1])
        # s(h_[i+1]) = a_[i+1]

        # dE/dW_[i-1] = (y - a_[i+1] s'(h_[i+1])) w_i s'(h_i) a_[i-1]

        for i in reversed(range(len(self.derivatives))):
            activations = self.activations[i+1]

            delta = error * self._sigmoid_derivative(activations)  # ndarray([0.1, 0.2]) --> ndarray([[0.1, 0.2]])
            delta_reshaped = delta.reshape(delta.shape[0], -1).T

            current_activations = self.activations[i]  # ndarray([0.1, 0.2]) --> ndarray([[0.1], [0.2]])
            # change activations to column vector
            current_activations_reshaped = current_activations.reshape(current_activations.shape[0], -1)

            self.derivatives[i] = np.dot(current_activations_reshaped, delta)
            error = np.dot(delta_reshaped, self.weights[i].T)

            if verbose:
                print("Derivatives for W{}: {}".format(i, self.derivatives[i]))
        return error

    @staticmethod
    def _sigmoid_derivative(x):
        return x * (1.0 - x)

    @staticmethod
    def _sigmoid(x):
        """Sigmoid activation function
        :param float x: Value to be processed
        :returns float y: Output
        """
        y = 1 / (1 + np.exp(-x))
        return y


if __name__ == '__main__':
    # Create MLP
    mlp = MLP(2, [5], 1)

    # Create dummy data
    inputs = np.array([0.1, 0.2])
    target = np.array([0.3])

    # Perform forward propagation
    outputs = mlp.forward_propagation(inputs)

    # Calculate error
    error = target - outputs

    # Back propagation
    mlp.back_propagation(error, verbose=True)

    ''''# Print the results
    print("mlp weights: ", mlp.weights)
    print("\n")
    print("The network input is: {}".format(inputs))
    print("The network output is: {}".format(outputs))'''
