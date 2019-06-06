#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 16:52:09 2019
Functions to support the running of the Pinsky-Rinzel Model
@author: hannahgermaine
"""
import numpy as np
from PR_soma_gating import PR_soma_gating
from PR_dend_gating import PR_dend_gating

#Pinsky-Rinzel Model of an Intrinsic Burster
def pinsky_rinzel(k, t_step, time_vec, i_app_d, i_app_s, v_s, e_leak, e_h, e_na, e_k, v_d, e_ca, g_leak_s, g_leak_d, g_na_max, g_k_max, g_link, g_ca_max, g_kca_max, g_kahp_max, g_h_max, c_s, c_d, tau_ca):
    #Gating Variable Declaration/Calculation
    m_vec = np.zeros(len(v_s), dtype=float) #sodium activation variable vector
    h_vec = np.zeros(len(v_s), dtype=float) #sodium inactivation variable vector
    h_vec[0] = 0.5
    n_vec = np.zeros(len(v_s), dtype=float) #potassium activation variable vector
    n_vec[0] = 0.4
    m_ca_vec = np.zeros(len(v_s), dtype=float) #calcium current activation variable vector
    m_kca_vec = np.zeros(len(v_s), dtype=float) #calcium-dependent potassium current activation variable vector
    m_kca_vec[0] = 0.2
    m_kahp_vec = np.zeros(len(v_s), dtype=float) #potassium after hyper polarization current activation variable vector
    m_kahp_vec[0] = 0.2
    Ca_vec = np.zeros(len(v_s), dtype=float) #Dendritic calcium level
    Ca_vec[0] = 1*10**(-6)
    Chi_vec = np.zeros(len(v_s), dtype=float)
    Chi_vec[0] = min(4000*Ca_vec[0],1)
    m_h_vec = np.zeros(len(v_s), dtype=float) #hyperpolarization activation variable vector
    somatic_spikes = []
    wait_to_spike = 0
    for i in range(len(v_s)-1):
        alpha_mca, beta_mca, alpha_kca, beta_kca, alpha_kahp, beta_kahp = PR_dend_gating(v_d[i], Ca_vec[i])
        alpha_m, beta_m, alpha_h, beta_h, alpha_n, beta_n = PR_soma_gating(v_s[i])
        #Somatic calculations
        v_s[i+1] = somatic_membrane_potential(v_s[i], g_leak_s, e_leak, g_na_max, m_vec[i], h_vec[i], e_na, g_k_max, n_vec[i], e_k, g_link, v_d[i], c_s, i_app_s, t_step)
        #Question 4 modification to log spike when > -10 and wait to log again until after v_s < -30
        if v_s[i+1] <= -30*10**(-3):
            wait_to_spike = 0
        if v_s[i+1] > -10*10**(-3) and wait_to_spike == 0 :
            somatic_spikes.append(time_vec[i+1])
            wait_to_spike = 1
        #Dendritic calculations
        v_d[i+1], dca_dt = dendritic_membrane_potential(v_d[i], g_leak_d, e_leak, g_ca_max, m_ca_vec[i], e_ca, g_kca_max, m_kca_vec[i], Chi_vec[i], e_k, g_kahp_max, m_kahp_vec[i], g_h_max, m_h_vec[i], e_h, g_link, v_s[i], c_d, i_app_d, t_step, k, tau_ca, Ca_vec[i])
        #Updating Calcium Vector and Chi Vector
        Ca_vec[i+1] = dca_dt*t_step + Ca_vec[i]
        Chi_vec[i+1] = min(4000*Ca_vec[i+1],1)
        #Updating Gating Variables
        m_inf, m_tau, h_inf, h_tau, n_inf, n_tau, m_ca_inf, m_ca_tau, m_kca_inf, m_kca_tau, m_kahp_inf, m_kahp_tau, m_h_inf, m_h_tau = gatingvar(alpha_mca, beta_mca, alpha_kca, beta_kca, alpha_kahp, beta_kahp, alpha_m, beta_m, alpha_h, beta_h, alpha_n, beta_n, v_d[i])
        m_vec[i+1], h_vec[i+1], n_vec[i+1], m_ca_vec[i+1], m_kca_vec[i+1], m_kahp_vec[i+1], m_h_vec[i+1] = gatingvarupdate(t_step, m_vec[i], h_vec[i], n_vec[i], m_ca_vec[i], m_kca_vec[i], m_kahp_vec[i], m_h_vec[i], m_inf, m_tau, h_inf, h_tau, n_inf, n_tau, m_ca_inf, m_ca_tau, m_kca_inf, m_kca_tau, m_kahp_inf, m_kahp_tau, m_h_inf, m_h_tau)
    v_s_calculated = v_s
    v_d_calculated = v_d
    return v_s_calculated, v_d_calculated, m_vec, h_vec, n_vec, m_ca_vec, m_kca_vec, m_kahp_vec, m_h_vec, Chi_vec, Ca_vec, somatic_spikes

#Somatic Membrane Potential Calculation
def somatic_membrane_potential(v_s, g_leak_s, e_leak, g_na_max, m, h, e_na, g_k_max, n, e_k, g_link, v_d, c_s, i_app_s, t_step):
    s_leak_current = g_leak_s*(e_leak - v_s)
    s_max_na_current = g_na_max*m*m*h*(e_na - v_s)
    s_max_k_current = g_k_max*n*n*(e_k - v_s)
    s_link_current = g_link*(v_d - v_s)
    dvs_dt = (1/c_s)*(s_leak_current + s_max_na_current + s_max_k_current + s_link_current + i_app_s)
    v_s_now = dvs_dt*t_step + v_s
    return v_s_now

#Dendritic Membrane Potential Calculation
def dendritic_membrane_potential(v_d, g_leak_d, e_leak, g_ca_max, m_ca, e_ca, g_kca_max, m_kca, Chi, e_k, g_kahp_max, m_kahp, g_h_max, m_h, e_h, g_link, v_s, c_d, i_app_d, t_step, k, tau_ca, Ca):
    d_leak_current = g_leak_d*(e_leak - v_d)
    d_max_ca_current = g_ca_max*m_ca*m_ca*(e_ca - v_d)
    dca_dt = k*d_max_ca_current - Ca/tau_ca
    d_max_kca_current = g_kca_max*m_kca*Chi*(e_k - v_d)
    d_max_kahp_current = g_kahp_max*m_kahp*(e_k - v_d)
    d_h_current = g_h_max*m_h*(e_h - v_d)
    d_link_current = g_link*(v_d - v_s)
    dvd_dt = (1/c_d)*(d_leak_current + d_max_ca_current + d_max_kca_current + d_max_kahp_current + d_h_current - d_link_current + i_app_d)
    v_d_now = dvd_dt*t_step + v_d
    return v_d_now, dca_dt

#Gating Variable Calculation
def gatingvar(alpha_mca, beta_mca, alpha_kca, beta_kca, alpha_kahp, beta_kahp, alpha_m, beta_m, alpha_h, beta_h, alpha_n, beta_n, v_d):
    m_inf = alpha_m/(alpha_m + beta_m)
    m_tau = 1/(alpha_m + beta_m)
    h_inf = alpha_h/(alpha_h + beta_h)
    h_tau = 1/(alpha_h + beta_h)
    n_inf = alpha_n/(alpha_n + beta_n)
    n_tau = 1/(alpha_n + beta_n)
    m_ca_inf = alpha_mca/(alpha_mca + beta_mca)
    m_ca_tau = 1/(alpha_mca + beta_mca)
    m_kca_inf = alpha_kca/(alpha_kca + beta_kca)
    m_kca_tau = 1/(alpha_kca + beta_kca)
    m_kahp_inf = alpha_kahp/(alpha_kahp + beta_kahp)
    m_kahp_tau = 1/(alpha_kahp + beta_kahp)
    m_h_inf = 1/(1 + np.exp((v_d + 0.070)/0.006))
    m_h_tau = 0.272 + 1.499/(1 + np.exp(-(v_d+0.0422)/0.00873))
    return m_inf, m_tau, h_inf, h_tau, n_inf, n_tau, m_ca_inf, m_ca_tau, m_kca_inf, m_kca_tau, m_kahp_inf, m_kahp_tau, m_h_inf, m_h_tau

#Updates to Gating Variables Calculations
def gatingvarupdate(t_step, m_vec_i, h_vec_i, n_vec_i, m_ca_vec_i, m_kca_vec_i, m_kahp_vec_i, m_h_vec_i, m_inf, m_tau, h_inf, h_tau, n_inf, n_tau, m_ca_inf, m_ca_tau, m_kca_inf, m_kca_tau, m_kahp_inf, m_kahp_tau, m_h_inf, m_h_tau):
    dm_dt = (m_inf - m_vec_i)/m_tau
    m_vec_now = dm_dt*t_step + m_vec_i
    dh_dt = (h_inf - h_vec_i)/h_tau
    h_vec_now = dh_dt*t_step + h_vec_i
    dn_dt = (n_inf - n_vec_i)/n_tau
    n_vec_now = dn_dt*t_step + n_vec_i
    dca_dt = (m_ca_inf - m_ca_vec_i)/m_ca_tau
    m_ca_vec_now = dca_dt*t_step + m_ca_vec_i
    dkca_dt = (m_kca_inf - m_kca_vec_i)/m_kca_tau
    m_kca_vec_now = dkca_dt*t_step + m_kca_vec_i
    dkahp_dt = (m_kahp_inf - m_kahp_vec_i)/m_kahp_tau
    m_kahp_vec_now = dkahp_dt*t_step + m_kahp_vec_i
    dmh_dt = (m_h_inf - m_h_vec_i)/m_h_tau
    m_h_vec_now = dmh_dt*t_step + m_h_vec_i
    return m_vec_now, h_vec_now, n_vec_now, m_ca_vec_now, m_kca_vec_now, m_kahp_vec_now, m_h_vec_now