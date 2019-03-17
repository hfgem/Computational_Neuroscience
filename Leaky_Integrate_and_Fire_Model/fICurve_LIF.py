"""This function calculates the interspike interval for a LIF neuron, and from it the firing rate, given the following variables:
1.) Leak reversal potential
2.) Applied current (assumed to be steady over time)
3.) Leak conductance
4.) Threshold potential
5.) Reset potential
6.) Membrane capacitance

The function can calculate the data given individual values or vectors containing all values.
If the vector method is desired, so that a vector of different applied currents can be calculated for at once,
all other values should be provided as vectors of the same length"""

import numpy as np

def fICurve_LIF(e_l, i_app, g_l, v_th, v_reset, c_m):
    #e_l is the leak reversal potential
    #i_app is the applied current
    #g_l is the leak conductance
    #v_th is the threshold potential
    #v_reset is the reset potential
    #c_m is the membrane capacitance
    if isinstance(i_app, (list, np.ndarray)): #if all variables are given in vector form
        tau_decay = np.divide(c_m, g_l)
        v_ss = e_l + np.divide(i_app,g_l)
        ln = np.log(np.divide((v_ss -v_th),(v_ss -v_reset)))
        isi = np.multiply(-tau_decay, ln)
        firing_rate = np.divide(1,isi)
    else: #if all variables are given as individual values
        tau_decay = c_m/g_l #time constant of decay
        v_ss = e_l + i_app/g_l #steady state membrane potential
        isi = -tau_decay*np.log((v_ss - v_th)/(v_ss - v_reset))
        firing_rate = 1/isi
    return isi, firing_rate

"""Example of calls:    
e_l = -70*10**(-3)
v_th = -50*10**(-3)
v_reset = -65*10**(-3)
c_m = 2*10**(-9)
g_l = 1/(5*10**9)
i_app = 240*10**(-12)

isi, firing_rate = fICurve_LIF(e_l, i_app, g_l, v_th, v_reset, c_m)
print(isi)
print(firing_rate)"""