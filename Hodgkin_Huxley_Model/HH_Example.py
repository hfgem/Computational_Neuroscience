#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: hannahgermaine

This code calculates the membrane potential and gating variable dynamics,
in a Hodgkin-Huxley model simulation, given a set of conditions. The code
outputs a plot of the applied current and resulting membrane potential to
the user's desktop.
"""

import Hodgkin_Huxley as hh
import matplotlib.pyplot as plt
import numpy as np
import os

desktop = os.environ["HOME"] + "/Desktop/"

#Variables:
#time vector
t_max = 0.35 #0.35 seconds
t_step = 2*10**(-6) #timestep
t_vector = np.arange(0,t_max,t_step) #vector of time values
#conductances
g_leak = 30*10**(-9) #30 nS leak conductance
max_g_na = 12*10**(-6) #12 microS maximum sodium conductance
max_g_k = 3.6*10**(-6) #3.6 microS maximum delayed rectifier conductance
#reversal potentials
e_na = 45*10**(-3) #45 mV sodium reversal potential
e_k = -82*10**(-3) #-82 mV potassium reversal potential
e_l = -60*10**(-3) #-60 mV leak reversal potential
c_m = 100*10**(-12) #100 pF membrane capacitance
#membrane potential vector
v_vector = np.zeros(len(t_vector)) #vector of membrane potentials
v_vector[0] = e_l + 0.01 #initializing membrane potential to slightly above leak reversal potential
#applied current vector
i_app = np.zeros(len(t_vector)) #vector of applied currents
i_base = 0.65*10**(-9) #base applied current of 0.65 nA
i_app += i_base
t_start = int((100*10**(-3))/t_step) #increase applied current at 100 ms
dur_applied = t_start #duration of applied current - 100 ms
indices_i_app_increase = np.arange(0,dur_applied) + t_start #indices to increase applied current
np.add.at(i_app, indices_i_app_increase, 0.22*10**(-9)) #Increase the applied current to 0.22 nA
#gating variable vectors
m = np.zeros(len(t_vector)) #m - sodium activation vector
h = np.zeros(len(t_vector)) #h - sodium inactivation vector
n = np.zeros(len(t_vector)) #n - potassium activation vector

#Run Hodgkin-Huxley simulation for above variables
v_calculated, m_calculated, h_calculated, n_calculated = hh.hod_hux(m, h, n, t_step, t_vector, v_vector, i_app, g_leak, max_g_na, max_g_k, e_na, e_k, e_l, c_m)

#Plot results of simulation
plt.figure(1, figsize=(10,10))
plt.subplot(211)
plt.plot(t_vector, i_app)
plt.xlabel("Time (in seconds)")
plt.ylabel("Current (in Amperes)")
plt.title("Applied Current")
plt.subplot(212)
plt.plot(t_vector, v_calculated)
plt.xlabel("Time (in seconds)")
plt.ylabel("Membrane Potential (in Volts)")
plt.title("Membrane Potential in Hodgkin Huxley")
plt.subplots_adjust(top=1.0, bottom=0.1, left=0.1, right=1.0, hspace=0.5,
                    wspace=0.5)
plt.savefig(desktop + "HH_simulation_figure.png", bbox_inches='tight')
plt.show()
