function V_m = LIF_Tutorial_2_1(V_m, V_th, V_reset, ...
        C_m, E_L, R_m, I_app, dt, noise)
    %ABOUT: This function calculates the membrane potential of a Leaky
    %   Integrate-and-Fire neuron given a set of parameters.
    %INPUTS:
    %   1. V_m = a vector of membrane potential for all time points, with
    %       V_m(1) = a starting membrane potential.
    %   2. V_th = threshold membrane potential
    %   3. V_reset = reset membrane potential
    %   4. C_m = membrane capacitance
    %   5. E_L = leak reversal potential
    %   6. R_m = membrane resistance
    %   7. I_app = a vector of the same size as V_m with applied current
    %       values
    %   8. dt = timestep of simulation
    %   9. noise = a vector of the same size as V_m with applied noise
    %OUTPUT:
    %   1. V_m = vector of calculated membrane potentials
    for i = 2:length(V_m) %1a.vi
        if V_m(i-1) > V_th %ia.viii
            %Test for threshold membrane potential and reset
            V_m(i) = V_reset;
        else
            %1a.vii
            %Calculate the change in membrane potential
            dV_m = (1/C_m)*(((E_L - V_m(i-1))/R_m) + I_app(i-1));
            %Update the membrane potential for the time step
            V_m(i) = V_m(i-1) + dV_m*dt + noise(i-1);
        end
    end
end