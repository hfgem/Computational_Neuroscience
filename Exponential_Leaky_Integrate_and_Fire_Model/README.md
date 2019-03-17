# Exponential Leaky Integrate-and-Fire Model

Author: Hannah Germaine

Summary: This model updates the LIF model (https://github.com/hfgem/Computational_Neuroscience/tree/master/Leaky_Integrate_and_Fire_Model) to include a better representation of how a neuron behaves as it approaches a spike. The LIF model shows a slowing down of the change in membrane potential as it approaches threshold and then artificially spikes when, in reality, the closer a neuron is to threshold, the faster it approaches it until it spikes. The Exponential Leaky Integrate-and-Fire Model (ELIF) better displays the behavior of a neuron as it approaches a spike. Building on the ELIF Model, the Adaptive Exponential Leaky Integrate-and-Fire Model (AELIF) better represents the behavior of a neuron following a spike by expressing spike rate adaptation (SRA) in which the spiking of a neuron in response to a constant applied current decreases over time.

Detail: If the results of the LIF model were to be plotted as membrane potential vs. time, one would notice that before a "spike", the membrane change in membrane potential slows down. In reality, as a neuron approaches threshold (and passes), the rate at which it's membrane potential changes increases. To better model this situation, one can modify the LIF model to include an exponential term that causes the membrane potential to increase more the greater it is than the threshold potential, and decrease more the less it is than the threshold potential. To accomplish this, we modify the LIF equation as follows:

![ELIF_equation](https://github.com/hfgem/Computational_Neuroscience/blob/master/Exponential_Leaky_Integrate_and_Fire_Model/Images/ELIF_equation.png)

You'll see that the exponential term approaches infinity as the membrane potential grows much larger than the threshold potential, and approaches 0 as the the membrane potential grows much smaller than the threshold potential. Notice there is a delta_th term that influences the strength of this change and is used to denote when this term becomes much larger than the terms of E_L and V_m.

To improve the model further, and reduce the response of the neuron over time to a constant applied current, we implement spike rate adaptation (SRA) in which a hyperpolarizing current is added to the dynamical equation that decreases in strength over time and increases in maximum strength following each spike of the neuron:

![AELIF_SRA_equation](https://github.com/hfgem/Computational_Neuroscience/blob/master/Exponential_Leaky_Integrate_and_Fire_Model/Images/AELIF_equation.png)

The SRA current decreases in strength over time as follows:

![SRA_current](https://github.com/hfgem/Computational_Neuroscience/blob/master/Exponential_Leaky_Integrate_and_Fire_Model/Images/SRA_current.png)

Where after each spike, the SRA current is increased by a factor of b (I_{SRA} = I_{SRA} + b). The factors a and b modify the magnitude of the adaptation current where a is in units of conductance and b is in units of current. The factor of tau_{SRA} is a time constant that dictates the rate of decay of the SRA current and is generally a fairly large value (a few hundred ms) to ensure that the spike rate adaptation current has a notable effect on the neuron's spiking behavior as a current continues to be applied. This results in the new AELIF model that more realistically depicts the behavior of a simple LIF neuron before and after a spike.
