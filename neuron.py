#!/usr/bin/python
"""
Program simulating a neural network.

Purpose: To experiment with neural networks to learn how they work and
         how they are connected, as well as to explore the idea of
         creating 'stacks' of neurons that can then themselves be
         interconnected.
"""

#todo: add the ability for each neuron to know what layer it belongs to

import logging

class Neuron(object):
    """
    Processing and training functionality for a single neuron.
    Parameters initiate as 1
    TODO: Add training functionality.
    TDOO: Add parameters. DONE?
    """
    def __init__(self, paramnum, name="unnamed neuron"):
        self.log = logging.getLogger()
        self.value = None
        self.name = name
        self.owner = None
        self.paramnum = paramnum
        self.params = []
        for x in range(self.paramnum):
            self.params.append(1)
        self.log.info("Initializing new Neuron " + self.name + " with parameters:")
        self.log.info(self.params)

    def imprint(self, owner):
        self.owner = owner

    def soundoff(self):
        self.log.info(self.name + " sounding off. Parent: " + self.owner.name)
        
    def process(self, trigger):
        """
        Trigger is a list.
        """
        # Modify to set value based on triggers
        self.log.info("Processing neuron: '" + self.name + "' with trigger: " + str(trigger))
        self.precalc = 0
        if len(self.params) == len(trigger):
            for x,y in zip(self.params, trigger): #zip should be replaced when lists get long
                self.precalc = self.precalc + x*y
        else:
            return TypeError
            #disabled so that i can move on
#            self.log.info(self.name + ' has insificent paramiters to process the input.')
#            self.resolvelimit(trigger)
#        self.value = self.precalc
        self.value = self.precalc
        return self.value()
        self.value = None

#issue with the trigger to be preserved being threated as more than one argument is unresolved
'''
    def resolvelimit(preserve):
        """
        Preserve is used to preserve the previos triger.
        """
        #just added this
        self.newparams = len(preserve) - self.paramnum
        for x in range(0, self.newparams):
            self.params.append(1)
        self.paramnum = len(self.params)
        self.log.info('Added ' + self.newparams + 'new parameters to ' + self.name + '. Reruning...')
        self.process(preserve)

    def output(self):
        """
        Returns the most recently calculated value.  If no value has
        been calculated, returns None.
        """
        return self.value
'''

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

    def claimdependants(self):
        for neuron in self.neurons:
            self.claim(neuron)
            self.log.info(self.name + " claims " + neuron.name + " as a dependent.")

    def claim(self, neuron):
        neuron.owner = self

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
        self.claim(neuron)

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

    def soundoff(self):
        if self.next_layer == None:
            self.log.info(self.name + " sounding off. Next layer: None Neurons:")
        else:
            self.log.info(self.name + " sounding off. Next layer: " + self.next_layer.name + " Neurons:")
        for neuron in self.neurons:
            neuron.soundoff()

#class Stack(object):
#    def __init__(self, name="unnamed layer", register=None, neurons=None):
#        self.log = logging.getLogger()
#        self.layers()
#            for layer in layers:
#                self.generate_layer(layer)
#    def generate_layer(self, layer, name=None, register=None, owner=self        

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
        neurons=[Neuron(1, name="Neuron " + str(x)) for x in range(1)])
    
    L2 = Layer(
        name="Layer 2", register=L1,
        neurons=[Neuron(1, name="Neuron " + str(x)) for x in range(2)])
    L3 = Layer(
        name="Layer 3", register=L2,
        neurons=[Neuron(1, name="Neuron " + str(x)) for x in range(3)])

    #sound off
    L1.soundoff()
    L2.soundoff()
    L3.soundoff()
    
    
    # Processing information through the neural net:
    L1.process([1])
