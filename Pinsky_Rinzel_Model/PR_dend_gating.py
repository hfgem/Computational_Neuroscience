#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 14:11:22 2019
PR_dend_gating function
@author: hannahgermaine
"""
import numpy as np

def PR_dend_gating(V_mD, Ca):
    if isinstance(V_mD, (list, np.ndarray)):
        alpha_mca = np.zeros(len(V_mD), dtype=float)
        beta_mca = np.zeros(len(V_mD), dtype=float)
        alpha_kca = np.zeros(len(V_mD), dtype=float)
        beta_kca = np.zeros(len(V_mD), dtype=float)
        alpha_kahp = np.zeros(len(V_mD), dtype=float)
        beta_kahp = 4*np.ones(len(V_mD), dtype=float)
        for i in range(len(V_mD)):
            alpha_mca[i] = 1600/(1 + np.exp(-72*(V_mD[i]-0.005)))
            b_mca_1 = 2*(10**(4))*(V_mD[i]+0.0089)
            b_mca_2 = np.exp(200*(V_mD[i]+0.0089)) - 1 + 0.000000001 #adding small value to prevent division error
            beta_mca[i] = b_mca_1/b_mca_2
            if V_mD[i] > -0.010:
                alpha_kca[i] = 2000*np.exp(-(V_mD[i]+0.0535)/0.027)
                beta_kca[i] = 0
            else:
                a_1 = ((V_mD[i]+0.050)/0.011)-((V_mD[i]+0.0535)/0.027)
                alpha_kca[i] = np.exp(a_1)/0.018975
                beta_kca[i] = (2000*np.exp(-(V_mD[i]+0.0535)/0.027)) - alpha_kca[i]
            alpha_kahp[i] = np.minimum(20, (20*(10**3)*Ca[i]))
    else:
        alpha_mca = 1600/(1 + np.exp(-72*(V_mD-0.005)))
        b_mca_1 = 2*(10**(4))*(V_mD +0.0089)
        b_mca_2 = np.exp(200*(V_mD +0.0089)) - 1 + 0.000000001 #adding small value to prevent division error
        beta_mca = b_mca_1/b_mca_2
        if V_mD > -0.010:
            alpha_kca = 2000*np.exp(-(V_mD +0.0535)/0.027)
            beta_kca = 0
        else:
            a_1 = ((V_mD +0.050)/0.011)-((V_mD +0.0535)/0.027)
            alpha_kca = np.exp(a_1)/0.018975
            beta_kca = (2000*np.exp(-(V_mD +0.0535)/0.027)) - alpha_kca
        alpha_kahp = np.minimum(20, (20*(10**3)*Ca))
        beta_kahp = 4
    
    return alpha_mca, beta_mca, alpha_kca, beta_kca, alpha_kahp, beta_kahp
