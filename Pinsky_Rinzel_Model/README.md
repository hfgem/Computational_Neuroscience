# Pinsky-Rinzel Model

Author: Hannah Germaine

Summary: This model is a two-compartment model of a bursting neuron. In previous models, we have focused on the neuron as a single/whole being. The Pinsky-Rinzel model gives a baseline for identifying and modeling the interaction of multiple compartments in a neuron. In particular, this model will show how differing properties in two compartments can result in a bursting behavior.

Detail: The Pinsky-Rinzel model revolves about two compartments: one for the dendrites of a neuron, the second for the soma. The soma has similar components to the Hodgkin-Huxley model (see <https://github.com/hfgem/Computational_Neuroscience/blob/master/Hodgkin_Huxley_Model/> ): an inward fast sodium current I_Na, an outward potassium current I_K, and a small leak current I_Leak that is mostly outward. The soma is connected to the dendritic component by a link current I_Link, that will flow by the gradient from higher membrane potential to lower membrane potential. Finally, the dendritic compartment receives an inward calcium current I_Ca, has an outward calcium-dependent potassium current I_KCa, an after-hyperpolarization outward current I_KAHP, and a small leak current I_Leak. To summarize, the two compartments have the following currents:
* I_Na - an inward fast sodium current to the soma
* I_K - an outward potassium current from the soma
* I_Leak_S - a small outward leak current from the soma
* I_Link - a current between the two compartments that flows from high membrane potential to low
* I_Ca - an inward calcium current to the dendrite
* I_KCa - an outward calcium-dependent potassium current from the dendrite
* I_KAHP - an after-hyperpolarization outward current from the dendrite
* I_Leak_D - a small outward leak current from the dendrite

Here we have an image of the two compartments and their currents:

![PR_Model](https://github.com/hfgem/Computational_Neuroscience/blob/master/Pinsky_Rinzel_Model/Images/PR_Model.png)

To simulate the behavior of a two-compartmental neuron, we write two dynamical equations, one for each compartment, as follows:

![PR_Equations](https://github.com/hfgem/Computational_Neuroscience/blob/master/Pinsky_Rinzel_Model/Images/PR_Equations.png)

The variables in the equations are as follows:
* C_S is the membrane capacitance for the soma
* C_D is the membrane capacitance for the dendrite
* dV_S/dt is the change in the membrane potential of the soma over time
* dV_D/dt is the change in the membrane potential of the dendrite over time
* V_S is the membrane potential of the soma at the point in time in question
* V_D is the membrane potential of the dendrite at the point in time in question
* G_Leak^S is the leak conductance for the soma
* G_Leak^D is the leak conductance for the dendrite
* G_Na^(max) is the maximum sodium conductance
* m, h, and n are gating variables that depend on the somatic membrane potential (see below)
* m_Ca and m_KCA are gating variables that depend on the dendritic membrane potential
* X and m_KAHP are gating variables that depend on the calcium concentration
* E_L is the leak reversal potential (assumed the same for both compartments)
* E_Na is the sodium reversal potential
* E_Ca is the calcium reversal potential
* E_K is the potassium reversal potential
* I_app^S is the somatic applied current
* I_app^D is the dendritic applied current

The gating variables m, h, n, m_Ca, m_KCa, and m_KAHP are described by the following set of dynamical equations (the explanation can be found at <https://github.com/hfgem/Computational_Neuroscience/blob/master/Hodgkin_Huxley_Model/> in the explanation of a two-state system):

![gating_eqns](https://github.com/hfgem/Computational_Neuroscience/blob/master/Pinsky_Rinzel_Model/Images/gating_eqns.png)

The alpha and beta values differ for each value and are slightly exhaustive to write out in this file, but can be found in the PR_dend_gating.py and PR_soma_gating.py files.

The gating variable X is a calcium-dependent term that contributes to I_KCa and responds instantaneously, unlike the other gating variables, as follows:

![gating_eqns](https://github.com/hfgem/Computational_Neuroscience/blob/master/Pinsky_Rinzel_Model/Images/chi_dynamics.png)

Here we take the minimum of 4000 time the concentration of calcium and 1.

# pinskysupport.py

All of the above is combined in the pinskysupport.py file in the form of multiple functions. In order to run a Pinsky-Rinzel model, you can simply import the functions from pinskysupport.py (ex. import pinskysupport as ps) and supply the following variables:
* k = the conversion from charge to concentration in units MC^(-1) (if you take the fractional area of the dendrite (ex. 2/3) as the variable a_d, you can find k as follows: k = (5*10**6)/a_d).
* t_step = the duration of each timestep (ex. 2*10**(-6) for 2 microseconds)
* time_vec = a vector of length determined by the amount of time you would like to simulate the model for, in steps 't_step' (ex. time_vec = numpy.arange(0,time,t_step))
* i_app_d = applied dendritic current
* i_app_s = applied somatic current
* v_s = zeros vector of length time_vec with only the first value set if an initial somatic membrane potential is desired (numpy.zeros(len(time_vec), dtype=float))
* e_leak = leak reversal potential in mV
* e_h = hyperpolarization current reversal potential in mV
* e_na = sodium current reversal potential in mV
* e_k = potassium current reversal potential in mV
* v_d = zeros vector of length time_vec with only the first value set if an initial dendritic membrane potential is desired (numpy.zeros(len(time_vec), dtype=float))
* e_ca = calcium current reversal potential in mV
* g_leak_s = somatic leak conductance in nS
* g_leak_d = dendritic leak conductance in nS
* g_na_max = maximum sodium conductance in microS
* g_k_max = maximum delayed rectifier conductance in microS
* g_link = link conductance in nS
* g_ca_max = maximum calcium conductance in microS
* g_kca_max = maximum calcium-dependent potassium conductance in microS
* g_kahp_max = maximum after-hyperpolarization conductance in nS
* g_h_max = maximum hyperpolarization conductance in nS
* c_s = capacitance of soma in Farads
* c_d = capacitance of dendrite in Farads
* tau_ca = time constant for decay of calcium (ms)

# pinskyexample.py

An example of how to use pinskysupport.py is given in the file pinskyexample.py.

# PR_dend_gating.py

The calculations for the dendritic gating variables can be found in PR_dend_gating.py. Here, you will also find the values for the alpha and beta variables described above.

# PR_soma_gating.py

The calculations for the somatic gating variables can be found in PR_soma_gating.py. Here, you will also find the values for the alpha and beta variables described above.

# pinskygatingexample.py

If you are interested in only gaining the gating variable information, you can do so using the PR_dend_gating.py and PR_soma_gating.py programs as in the example file pinskygatingexample.py.