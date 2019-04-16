#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: hannahgermaine

This code includes functions for calculating the membrane potential and gating
variable dynamics in a Hodgkin-Huxley model simulation. The first function,
hod_hux, performs the bulk of the calculations and ultimately returns the output
vectors. The functions hod_hux_rate_constants and hod_hux_support assist in the
calculations needed for the rate constants at all points in time, as well as the
time constants and steady states of the rate constants.
"""

import numpy as np

#Hodgkin-Huxley Model
def hod_hux(m_vec, h_vec, n_vec, t_step, t_vector, v_m, i_app, g_leak, max_g_na, max_g_k, e_na, e_k, e_l, c_m):
    i_total_vec = [0 for i in range(len(t_vector))]
    for i in range(len(t_vector) - 1):
        #Finding change and updating membrane potential
        i_leak = g_leak*(e_l - v_m[i])
        i_na = max_g_na*m_vec[i]*m_vec[i]*m_vec[i]*h_vec[i]*(e_na - v_m[i])
        i_k = max_g_k*n_vec[i]*n_vec[i]*n_vec[i]*n_vec[i]*(e_k - v_m[i])
        i_total = i_leak + i_na + i_k + i_app[i]
        i_total_vec[i+1] = i_total
        dvm_dt = i_total/c_m
        v_m[i+1] = dvm_dt*t_step + v_m[i]
        al_m, bet_m, al_h, bet_h, al_n, bet_n = hod_hux_rate_constants(v_m[i])
        tau_m, tau_h, tau_n, m_inf, h_inf, n_inf = hod_hux_support(al_m, bet_m, al_h, bet_h, al_n, bet_n)
        #Finding change and updating gating variables
        dm_dt = (m_inf - m_vec[i])/tau_m
        m_vec[i+1] = dm_dt*t_step + m_vec[i]
        dh_dt = (h_inf - h_vec[i])/tau_h
        h_vec[i+1] = dh_dt*t_step + h_vec[i]
        dn_dt = (n_inf - n_vec[i])/tau_n
        n_vec[i+1] = dn_dt*t_step + n_vec[i]
    v_calculated = v_m
    m_calculated = m_vec
    h_calculated = h_vec
    n_calculated = n_vec
    return v_calculated, m_calculated, h_calculated, n_calculated

def hod_hux_rate_constants(v_m):
    #Defining rate constants
    if v_m == -0.045:
        al_m = 10**3 #modified alpha_m rate constant to not divide by 0
    else:
        al_m = ((10**5)*(-v_m - 0.045))/(np.exp(100*(-v_m - 0.045))-1) #sodium activation rate
    bet_m = 4*(10**3)*np.exp((-v_m - 0.070)/0.018) #sodium deactivation rate
    al_h = 70*np.exp(50*(-v_m-0.070)) #sodium inactivation rate
    bet_h = (10**3)/(1 + np.exp(100*(-v_m-0.040))) #sodium deinactivation rate
    if v_m == -0.060:
        al_n = 100 #modified alpha_n rate constant to not divide by 0
    else:
        al_n = ((10**4)*(-v_m-0.060))/(np.exp(100*(-v_m-0.060))-1) #potassium activation rate
    bet_n = 125*np.exp((-v_m-0.070)/0.08) #potassium deactivation rate
    return al_m, bet_m, al_h, bet_h, al_n, bet_n
    

def hod_hux_support(al_m, bet_m, al_h, bet_h, al_n, bet_n):
    #Support the hodgkin-huxley model through calculation of time constants and steady states
    #Time constants
    tau_m = 1/(al_m + bet_m)
    tau_h = 1/(al_h + bet_h)
    tau_n = 1/(al_n + bet_n)
    #Steady states
    m_inf = al_m/(al_m + bet_m)
    h_inf = al_h/(al_h + bet_h)
    n_inf = al_n/(al_n + bet_n)
    return tau_m, tau_h, tau_n, m_inf, h_inf, n_inf
    