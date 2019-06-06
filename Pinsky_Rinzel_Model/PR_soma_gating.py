#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 13:16:54 2019
HW4 PR_Soma_gating function
@author: hannahgermaine
"""
import numpy as np

def PR_soma_gating(V_m):
    a_m_1 = np.multiply(320*(10**(3)),np.add(V_m,0.0469))
    a_m_2 = 1 - np.exp(np.multiply(-250,np.add(V_m,0.0469))) + 0.000000001 #adding small value to prevent division error
    alpha_m = a_m_1/a_m_2
    b_m_1 = np.multiply(280*(10**3),np.add(V_m,0.0199))
    b_m_2 = np.exp(np.multiply(200,np.add(V_m,0.0199)))-1 + 0.000000001 #adding small value to prevent division error
    beta_m = b_m_1/b_m_2
    alpha_h = 128*np.exp(-np.add(V_m,0.043)/0.018)
    beta_h = 4*(10**3)/(1+ np.exp(np.multiply(-200,np.add(V_m, 0.020))))
    a_n_1 = np.multiply(16*(10**3),np.add(V_m, 0.0249))
    a_n_2 = 1-np.exp(np.multiply(-200,np.add(V_m,0.0249))) + 0.000000001 #adding small value to prevent division error
    alpha_n = a_n_1/a_n_2
    beta_n = 250*np.exp(np.multiply(-25,np.add(V_m,0.040)))
    return alpha_m, beta_m, alpha_h, beta_h, alpha_n, beta_n
