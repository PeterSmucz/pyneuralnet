#!/usr/bin/python
"""
Program simulating a neural network.

Purpose: To experiment with neural networks to learn how they work and
         how they are connected, as well as to explore the idea of
         creating 'stacks' of neurons that can then themselves be
         interconnected.
"""

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
        self.log.info("Processing neuron: '" + self.name + "' with trigger: " + str(trigger))
        self.value = 0
        return self.output()

    def output(self):
        """
        Returns the most recently calculated value.  If no value has
        been calculated, returns None.
        """
        return self.value

class Layer(object):
    """
    Layer of neurons.  Each layer contains one or more neurons.  Every
    neuron in a layer accepts the same number and values of inputs.
    """
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
        """
        Register the layer to be triggered by the output of the
        neurons in the current layer.
        """
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
    LOGLEVEL = logging.DEBUG
    LOG = logging.getLogger()
    LOG.setLevel(level=LOGLEVEL)
    FMT = logging.Formatter(
        fmt=str('%(asctime)s | %(levelname)8s | %(filename)10s:%(lineno)3d | ' +
                '%(funcName)s | %(message)s'))
    CON = logging.StreamHandler()
    CON.setLevel(LOGLEVEL)
    CON.setFormatter(FMT)
    LOG.addHandler(CON)

    LOG.info("Starting...")

    # Create a new neural net
    L1 = Layer(
        name="Layer 1",
        neurons=[Neuron(name="Neuron " + str(x)) for x in range(1)])
    L2 = Layer(
        name="Layer 2", register=L1,
        neurons=[Neuron(name="Neuron " + str(x)) for x in range(2)])
    L3 = Layer(
        name="Layer 3", register=L2,
        neurons=[Neuron(name="Neuron " + str(x)) for x in range(3)])

    # Processing information through the neural net:
    L1.process([1])
