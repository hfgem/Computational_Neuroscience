"""This function calculates the membrane potential and spike-times of a Adaptive Exponential Leaky Integrate-and-Fire (AELIF) Neuron given the following variables:
- time vector (containing every point in time being modeled) (time_vector)
- membrane potential vector (to be filled in) (v_m)
- membrane capacitance (c_m)
- membrane resistance (r_m)
- leak potential (e_l)
- applied current vector (i_vector)
- maximum membrane potential (v_max)
- threshold membrane potential (v_th)
- reset membrane potential (v_reset)
- strength of threshold change term (delta_th)
- timestep (dt)
- strength of rate of decay of the SRA current (tau_sra)
- SRA current initial condition (i_sra)
- SRA conductance magnitude (a)
- SRA current magnitude (b)"""

def aelif(time_vector, v_m, c_m, r_m, e_l, i_vector, v_max, v_th, v_reset, delta_th, dt, tau_sra, i_sra, a, b):
    spiketimes = [] #create an empty array to store the times the neuron spikes
    v_calculated = v_m
    i_sra_vector = [] #create an empty array to store the spike rate adaptation current over time
    i_sra_vector.append(i_sra) #add the initial condition
    for i in range(len(time_vector) - 1):
        dvm_dt = (1/c_m)*((1/r_m)*(e_l - v_calculated[i] + delta_th*np.exp((v_calculated[i] - v_th)/delta_th)) - i_sra + i_vector[i])
        di_sra = (1/tau_sra)*(a*(v_calculated[i] - e_l) - i_sra)
        v_calculated[i+1] = dvm_dt*dt + v_calculated[i]
        i_sra += di_sra*dt
        if v_calculated[i+1] > v_max:
            v_calculated[i+1] = v_reset #reset if there's a spike past maximum membrane potential so it does not continue increasing infinitely
            spiketimes.append(time_vector[i+1])
            i_sra += b #update the adaptation current strength
        i_sra_vector.append(i_sra)
    return v_calculated, spiketimes, i_sra_vector
#return the membrane potential over time, spike times, and the SRA current over time

"""Example use:
#Variable declaration
e_l = -75*10**(-3) #-75 mV leak reversal potential
v_th = -50*10**(-3) #-50 mV threshold potential
v_reset = -80*10**(-3) #-80 mV reset potential
v_max = 50*10**(-3) #arbitrarily chosen 50 mV v_max
delta_th = 2*10**(-3) #2mV voltage-range for spike uptick
a = 2*10**(-9) #2nS I_sra control term - adaptation recovery
b = 0.02*10**(-9) #0.02nA I_sra current step - adaptation strength
g_l = 10*10**(-9) #10 nS Leak conductance
r_m = 1/g_l #Total membrane resistance
c_m = 100*10**(-12) #100pF total membrane capacitance
tau_sra = 200*10**(-3) #200 ms time constant for g_sra
i_sra = 0 #Spike-rate adaptation current

#Time vector
dt = 0.1*(10**(-3)) #time step in seconds (0.1 milliseconds)
t_max = 1.5 #maximum time in seconds = 1500 miliseconds
time_vector = [x*dt for x in range(int(t_max/dt))]

#Membrane voltage vector
v_m_zeros = np.zeros(len(time_vector))
v_m_zeros[0] = e_l

#Applied current - 500 pA of applied current from 0.5s to 1.0s
i_app = 500*10**(-12)
i_vector = np.zeros(len(time_vector))
starting = 0.5/dt
ending = 1.0/dt
for i in range(int(ending - starting)):
    i_vector[int(starting + i)] = i_app #fill the applied current vector
    
#Call function
v_calculated, spiketimes, i_sra_vector = aelif(time_vector, v_m_zeros, c_m, r_m, e_l, i_vector, v_max, v_th, v_reset, delta_th, dt, tau_sra, i_sra, a, b)
"""