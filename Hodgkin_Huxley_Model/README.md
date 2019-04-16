# Hodgkin-Huxley Model (HH)

Author: Hannah Germaine

Summary: This model describes the generation and propagation of action potentials (APs) through sodium and potassium channels. This model was published by Alan Hodgkin and Andrew Huxley in the 1950s, and was the result of analysis of electrophysiological data from the giant squid axon. It serves as a basis for all complex conductance-based models in computational neuroscience.

Detail: The HH model revolves about four variables: membrane potential (v_m), sodium activation (m), sodium inactivation (h), and potassium activation (n). The three variables m, h, and n, are together known as gating variables because they describe the open or closed nature (like a gate) of the channels they reference.

The dynamical equation that describes the change in membrane potential over time is as follows:

![HH_equation](https://github.com/hfgem/Computational_Neuroscience/blob/master/Hodgkin_Huxley_Model/Images/HH_equation.png)

Where the variables are as follows:
* C_m is membrane capacitance
* dV_m/dt is the change in the membrane potential over time
* G_L is the leak conductance
* E_L is the leak reversal potential
* V_m is the membrane potential at the point in time in question
* G_Na^(max) is the maximum sodium conductance
* E_Na is the sodium reversal potential
* G_K^(max) is the maximum potassium conductance (also called the maximum delayed rectifier conductance)
* E_K is the potassium reversal potential
* and I_app is the applied current at the point in time in question

The gating variables are described by the following set of equations:

![gating_eqns](https://github.com/hfgem/Computational_Neuroscience/blob/master/Hodgkin_Huxley_Model/Images/gating_eqns.png)

The steady states of the gating variables can be calculated as follows:

![ss_gating](https://github.com/hfgem/Computational_Neuroscience/blob/master/Hodgkin_Huxley_Model/Images/ss_gating.png)

and the time constants as follows:

![time_constants](https://github.com/hfgem/Computational_Neuroscience/blob/master/Hodgkin_Huxley_Model/Images/time_constants.png)

All of the above equations can be derived generally from a two-state system (here we'll have the states be A and B) model. k_B represents the rate at which things in state A change to state B, and k_A represents the rate at which things in state B change to state A.

![two_state](https://github.com/hfgem/Computational_Neuroscience/blob/master/Hodgkin_Huxley_Model/Images/two_state.png)

Since the gating variables describe the opening and closing of channels, let's discuss the two-state system as such: state A will represent the channel as open, and state B will represent the channel as closed. Let's say we have a number of channels, perhaps 100, we're looking at that are moving between state A and state B. We can define 'a' as the fraction of all channels in state A at a point in time, and 'b' as the fraction of all channels in state B at a point in time. This results in 'a+b=1' or 'b=1-a'.

If we wanted to model the rate at which the number of open channels is changing (da/dt), we could use our known rates of k_A and k_B and the known state of all channels. If we take k_A*b, then we see the rate at which channels in state B are turning into channels in state A. If we take k_B*a, then we see the rate at which channels in state A are turning into channels in state B. To get the overall rate at which the number of open channels is changing, we simply subtract the rate of those closing from the rate of those opening to get:

![two_state_rate](https://github.com/hfgem/Computational_Neuroscience/blob/master/Hodgkin_Huxley_Model/Images/two_state_rate.png)

In the same way we can model the rate at which the number of closed channels is changing.

To find the steady states, based on the definition of steady state implying no change, we can set da/dt to 0 and solve:

![two_state_ss](https://github.com/hfgem/Computational_Neuroscience/blob/master/Hodgkin_Huxley_Model/Images/two_state_ss.png)

The time constant comes from rewriting the rate of change of open channels as follows:

![two_state_tau](https://github.com/hfgem/Computational_Neuroscience/blob/master/Hodgkin_Huxley_Model/Images/two_state_tau.png)

The final key to the Hodgkin-Huxley model is the set of rate constants (the alpha and beta variables). These were defined based on the experimental data Hodgkin and Huxley found to be the following:

![rate_constants](https://github.com/hfgem/Computational_Neuroscience/blob/master/Hodgkin_Huxley_Model/Images/rate_constants.png)

# Hodgkin_Huxley.py

This program includes functions for calculating the membrane potential and gating variable dynamics in a Hodgkin-Huxley model simulation. The first function, hod_hux, performs the bulk of the calculations and ultimately returns the output vectors. The functions hod_hux_rate_constants and hod_hux_support assist in the calculations needed for the rate constants at all points in time, as well as the time constants and steady states of the rate constants.

# HH_Example.py

This program calculates the membrane potential and gating variable dynamics, in a Hodgkin-Huxley model simulation, given a set of conditions for the simulation. The code outputs a plot of the applied current and resulting membrane potential to the user's desktop.


