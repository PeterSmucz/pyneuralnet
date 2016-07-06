#!/usr/bin/python

import logging

class Neuron(object):
    """
    Processing and training functionality for a single neuron.

    TODO: Add training functionality.
    TDOO: Add parameters.
    """
    def __init__(self, name="unnamed neuron"):
        self.log = logging.getLogger()
        self.value = None
        self.name = name
        self.params = None
        self.log.info("Initializing new Neuron: " + self.name)

    def process(self, trigger):
        """
        Trigger is a list.
        """
        # Modify to set value based on triggers
        self.log.info("Processing neuron: '" + self.name + "'")
        self.value = 0
        return self.value
    
class Layer(object):
    def __init__(self, name="unnamed layer", register=None, neurons=None):
        self.log = logging.getLogger()
        self.name = name
        self.next_layer = None
        self.log.info("Initializing new Layer: " + self.name)
        self.neurons = []
        if register:
            register.register(self)
        if neurons:
            for neuron in neurons:
                self.add_neuron(neuron)

    def register(self, layer):
        self.log.info("Registering layer: '" + self.name +
                      "' triggers '" + layer.name + "'")
        self.next_layer = layer

    def add_neuron(self, neuron):
        """
        Add a neuron to the neuron list for this layer.
        """
        self.log.info("Add Neuron '" + neuron.name +
                      "' to Layer '" + self.name + "'")
        self.neurons.append(neuron)

    def process(self, trigger):
        """
        Start is the input for the layer itself.  The trigger is a
        list of inputs from each neuron in the previous layer.
        """
        result = []
        self.log.info("Processing layer: '" + self.name +
                      "', inputs: " + str(trigger))
        for neuron in self.neurons:
            result.append(neuron.process(trigger))
        self.log.info("Finished processing layer: '" + self.name +
                      "', outputs: " + str(result))
        if self.next_layer:
            return self.next_layer.process(result)
        else:
            return result

if __name__ == '__main__':
    # Initialize logging
    mylevel = logging.DEBUG
    log = logging.getLogger()
    log.setLevel(level=mylevel)
    fmt = logging.Formatter(fmt='%(asctime)s | %(levelname)8s | %(filename)10s:%(lineno)3d | %(funcName)s | %(message)s')
    con = logging.StreamHandler()
    con.setLevel(mylevel)
    con.setFormatter(fmt)
    log.addHandler(con)

    log.info("Starting...")

    # Create a new neural net
    layer1 = Layer(
        name="Layer 1",
        neurons=[Neuron(name="Neuron " + str(x)) for x in range(1)])
    layer2 = Layer(
        name="Layer 2", register=layer1,
        neurons=[Neuron(name="Neuron " + str(x)) for x in range(2)])
    layer3 = Layer(
        name="Layer 3", register=layer2,
        neurons=[Neuron(name="Neuron " + str(x)) for x in range(3)])

    # Processing information through the neural net:
    layer1.process([1])
