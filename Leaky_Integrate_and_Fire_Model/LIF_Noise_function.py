"""This function calculates the membrane potential and spike-times of a Leaky Integrate-and-Fire (LIF) Neuron with added noise given the following variables:
- membrane capacitance
- membrane resistance
- leak potential
- resting membrane potential
- threshold membrane potential
- applied current
- noise scale"""

def leaky_IF_noise(time_vector, sigma_i, v_m, c_m, r_m, e_l, i_app, v_th, v_reset, dt):
    #time_vector is a vector composed of each time increment
    #sigma_i scales the level of noise
    #v_m is a matrix of membrane potentials, with v_m[0] = initial condition
    #c_m - membrane capacitance
    #r_m - membrane resistance
    #e_l - leak potential
    #i_app - applied current
    #v_th - threshold membrane potential for spiking
    #v_reset - neuron resting membrane potential
    spiketimes = [] #vector containing the times a neuron spiked
    v_calculated = v_m #vector containing the membrane potential at each 
    for i in range(len(time_vector) - 1):
        #The following equations describe the behavior of a LIF neuron with an added noise term
        dvm_dt = (1/c_m)*((1/r_m)*(e_l - v_calculated[i]) + i_app[i+1])
        v_calculated[i+1] = dvm_dt*dt + v_calculated[i] + (np.random.randn(1)*sigma_i*math.sqrt(dt)) #pull values from a standard normal and scale using the noise scale
        if v_calculated[i+1] > v_th:
            v_calculated[i+1] = v_reset #reset the membrane potential if there's a spike past threshold
            spiketimes.append(time_vector[i+1]) #save the time the neuron spiked
    return v_calculated, spiketimes #return the membrane potential vector and spike times