import matplotlib.pyplot as plt
import numpy as np
import os
import pinskysupport as ps
import timeit

start = timeit.time.time()

desktop = os.environ["HOME"] + "/Desktop/"

"""Variable Declaration"""
time = 2 #2 seconds
t_step = 2*10**(-6) #2 microseconds
time_vec = [i*t_step for i in range(int(time/t_step))]
a_s = 1/3 #fractional area of soma
a_d = 1 - a_s #fractional area of dendrite
k = (5*10**6)/a_d #conversion from charge to concentration in units MC^-1
g_link = 50*10**(-9) #50 nS link conductance
v_s = np.zeros(len(time_vec), dtype=float) #somatic membrane potential vector
v_d = np.zeros(len(time_vec), dtype=float) #dendritic membrane potential vector
tau_ca = 50*10**(-3) #50 ms time constant for decay of calcium
i_app_d = 0 #dendritic applied current
i_app_s = 0 #somatic applied current
e_leak = -60*10**(-3) #-60 mV leak reversal potential
e_na = 60*10**(-3) #60 mV sodium reversal potential
e_h = -20*10**(-3) #-20 mV hyperpolarization reversal potential
e_k = -75*10**(-3) #-75 mV potassium reversal potential
e_ca = 80*10**(-3) #80 mV calcium reversal potential
g_leak_s = a_s * 5*10**(-9) #Somatic leak conductance in nS
g_leak_d = a_d * 5*10**(-9) #Dendritic leak conductance in nS
g_na_max = a_s * 3*10**(-6) #maximum sodium conductance in microS
g_k_max = a_s * 2*10**(-6) #maximum delayed rectifier conductance in microS
g_h_max = 0*10**(-9) #(0 nS) maximum hyperpolarization conductance: usually anywhere from 0-200nS
g_link = 20*10**(-9) #link conductance
g_ca_max = a_d * 2*10**(-6) #maximum calcium conductance
g_kca_max = a_d * 2.5*10**(-6) #maximum calcium-dependent potassium conductance
g_kahp_max = a_d * 40*10**(-9) #maximum after-hyperpolarization conductance
c_s = a_s * 100*10**(-12) #capacitance of soma in Farads
c_d = a_d * 100*10**(-12) #capacitance of dendrite in Farads
v_s[0] = e_leak
v_d[0] = e_leak

"""Run Program"""
v_s_calculated, v_d_calculated, m_vec, h_vec, n_vec, m_ca_vec, m_kca_vec, m_kahp_vec, m_h_vec, Chi_vec, Ca_vec, somatic_spikes = ps.pinsky_rinzel(k, t_step, time_vec, i_app_d, i_app_s, v_s, e_leak, e_h, e_na, e_k, v_d, e_ca, g_leak_s, g_leak_d, g_na_max, g_k_max, g_link, g_ca_max, g_kca_max, g_kahp_max, g_h_max, c_s, c_d, tau_ca)

"""Plot Results"""
start_time = int(len(time_vec)/11)
end_time = int(start_time + len(time_vec)/40)
plt.figure(1)
plt.subplot(211)
plt.plot(time_vec, v_s_calculated, label="Somatic Membrane Potential")
plt.plot(time_vec, v_d_calculated, label="Dendritic Membrane Potential")
plt.xlabel("Time (s)")
plt.ylabel("Membrane Potential (V)")
plt.title("Membrane Potential as a Function of Time (2 seconds)")
plt.legend()
plt.subplot(212)
plt.plot(time_vec[start_time:end_time], v_s_calculated[start_time:end_time], label="Somatic Membrane Potential")
plt.plot(time_vec[start_time:end_time], v_d_calculated[start_time:end_time], label="Dendritic Membrane Potential")
plt.xlabel("Time (s)")
plt.ylabel("Membrane Potential (V)")
plt.title("Membrane Potential as a Function of Time (zoomed)")
plt.legend()
plt.subplots_adjust(top=3.0, bottom=0.1, left=0.1, right=1.0, hspace=0.5,
                    wspace=0.5)
plt.savefig(desktop + "Germaine_3_figure.png", bbox_inches='tight')
plt.show()
print("Total Number of Spikes: " + str(len(somatic_spikes)))

end = timeit.time.time()
print("Time to run: " + str(round((end-start),2)) + " seconds")