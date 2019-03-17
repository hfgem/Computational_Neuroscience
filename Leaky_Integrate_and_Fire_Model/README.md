# Leaky Integrate-and-Fire Model

Author: Hannah Germaine

Summary: This model simulates a neuron with only a leak current and an externally applied current contributing to the change in its membrane potential. The neuron will "fire" at an explicitly defined threshold, and will then "reset" to a starting membrane potential.

Detail: The Leaky Integrate-and-Fire (LIF) model is one of the simplest ways of modeling the behavior of a neuron. What the model says is that the neuron can:
* "Leak" current (in the sense that, over time, current can flow out of the neuron)
* React to an externally applied current
* "Spike" after passing a certain threshold for membrane potential
* "Reset" to a starting membrane potential after spiking

The way the model implements this behavior is through the following dynamical equation:

![LIF_dyn_eqn](https://github.com/hfgem/Computational_Neuroscience/blob/master/Leaky_Integrate_and_Fire_Model/Images/LIF_dyn_eqn.png)

In the above equation, the term G*(E-V) is a means of calculating the leak current of a neuron. This comes from the equation in physics "V=IR", in which you can calculate the potential difference (V) by multiplying the current (I) and the resistance (R) together. Instead, the equation is rearranged to be I = VG where G is the conductance (1/R).

![Charge_Eqn](https://github.com/hfgem/Computational_Neuroscience/blob/master/Leaky_Integrate_and_Fire_Model/Images/Charge_Eqn.png)

You'll also note that instead of simply multiplying by V, here we have the difference between the membrane potential and the leak reversal potential. This is because the strength with which the current flows depends on this difference: the further the neuron is from the leak reversal potential, the more current flows into or out of the cell to bring it to that reversal potential (a balance point). The reason we don't subtract the reversal potential from the membrane potential stems from the equation "Q=CV" where Q is the charge stored on a capacitor given its capacitance and the membrane potential. When the derivative of this equation is taken, we get "the rate of change in charge = capacitance * the rate of change in membrane potential".

![Current_Eqn](https://github.com/hfgem/Computational_Neuroscience/blob/master/Leaky_Integrate_and_Fire_Model/Images/Current_Eqn.png)

Because of the nature of currents with neurons, when the current flows out of the cell, we define it as positive and when it flows into the cell, we define it as negative. So the rate of change in charge on the inside of the cell's membrane is the negative of the total membrane current

![Charge_Change_Eqn](https://github.com/hfgem/Computational_Neuroscience/blob/master/Leaky_Integrate_and_Fire_Model/Images/Charge_Change_Eqn.png)

Putting this all together, we get the left side and first term on the right side of the LIF dynamical equation. The final piece, I_{app} is the externally applied current, contributing to the total current flowing through the neuron at any point in time. Now we have our full equation and can use it to determine the change in membrane potential at any point in time given the known information.

Note, there is an additional term at the end of the equation that states that if the membrane potential goes past the threshold potential, return it back to the reset threshold. This is a basic way of mimicing a "spiking-behavior" in a neuron where, once a neuron has fired, before it fires again, it returns to a "reset" state. In reality, the time to return to reset depends on a number of factors and does not go back instantaneously, but again, for the sake of a simple model, this will do.

The two python scripts: LIF_function.py and LIF_Noise_function.py utilize this equation to update a vector containing a neuron's membrane potential at every point in time. The difference between the two is in a "noise term". The LIF_Noise_function.py script also updates the membrane potential with an added noise term pulled from a normal distribution and scaled by a factor of "sigma" defined by the user. This simply gives the end user the understanding of how noise can change the outcomes of a neuron's membrane potential / behavior. It is better applied in more rigorous models to account for external noise, but in this model gives an easy introduction to the concept.

If we wanted to calculate the time between spikes or the firing rate of a LIF neuron, we wouldn't need to calculate all the spikes as in LIF_function.py and LIF_Noise_function.py. An easier way to calculate this is to use information about the neuron's steady state and decay rate as in fICurve_LIF.py. When an applied current is held constant, we can use the dynamical equation from above by setting dV_m/dt (the change in membrane potential) to 0 (indicating a steady state for the neuron as the membrane potential is not changing) to get the steady-state membrane potential:

![LIF_Steady_State](https://github.com/hfgem/Computational_Neuroscience/blob/master/Leaky_Integrate_and_Fire_Model/Images/LIF_Steady_State.png)

We can calculate the decay rate using the information about the cell's membrane capacitance and leak conductance by noting that, in the neuron's dynamical equation, dividing the leak conductance over onto the left side gives a constant term before the term for change in membrane potential, dV_m/dt. We will rename that term to "tau" denoting it as a decay rate constant, and use it to calculate the time it takes to get to the threshold, and thus fire, as follows:

![LIF_ISI_Part1](https://github.com/hfgem/Computational_Neuroscience/blob/master/Leaky_Integrate_and_Fire_Model/Images/LIF_ISI_Part1.png)

We can continue by swapping the membrane potential at time 0 for the reset membrane potential (as after a spike, that is the "time zero" membrane potential:

![LIF_ISI_Part2](https://github.com/hfgem/Computational_Neuroscience/blob/master/Leaky_Integrate_and_Fire_Model/Images/LIF_ISI_Part2.png)

Now, if we set our spike time to be "T", and set that as equal to the threshold membrane potential, we can rearrange to have an equation that solves for the time it takes to get to the threshold, giving the inter-spike interval (ISI):

![LIF_ISI_Part3](https://github.com/hfgem/Computational_Neuroscience/blob/master/Leaky_Integrate_and_Fire_Model/Images/LIF_ISI_Part3.png)

From the ISI, we can get the frequency of spikes by simply taking 1/ISI.

At this point, we can modify the functions in any way to account for other scenarios or "extensions" of the LIF model. For example, if we wanted to have a more realistic spiking behavior, we could add what's called a refractory period, or a period of time after a spike during which a neuron cannot produce another spike. There are many ways of going about this such as:
* fixing the membrane potential at the reset value for a certain amount of time (known as a voltage clamp) after a spike before using the dynamical equations above
* adding a hyperpolarizing current (one that decreases the membrane potential) after a spike such as a potassium current modeled by: ![LIF_Ref_Current](https://github.com/hfgem/Computational_Neuroscience/blob/master/Leaky_Integrate_and_Fire_Model/Images/LIF_Ref_Current.png)
* raising the spiking threshold value with each spike so it takes longer to reach it: ![LIF_Raised_Threshold](https://github.com/hfgem/Computational_Neuroscience/blob/master/Leaky_Integrate_and_Fire_Model/Images/LIF_Raised_Threshold.png)
