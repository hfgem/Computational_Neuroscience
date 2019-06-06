import matplotlib.pyplot as plt
import os
from PR_soma_gating import PR_soma_gating
from PR_dend_gating import PR_dend_gating
import timeit

start = timeit.time.time()

desktop = os.environ["HOME"] + "/Desktop/"

"""Variable Declaration"""
Vhigh = 0.05
Vlow = -0.085
Vdiff = Vhigh - Vlow
V_m = [-0.085+(i*0.00001) for i in range(int(Vdiff/0.00001))] #vector of values for membrane potential
Cahigh = 2*10**(-3)
Ca = [(Cahigh/len(V_m))*i  for i in range(len(V_m))] #vector of values for calcium concentration

"""Run Programs"""
alpha_mca, beta_mca, alpha_kca, beta_kca, alpha_kahp, beta_kahp = PR_dend_gating(V_m, Ca)
alpha_m, beta_m, alpha_h, beta_h, alpha_n, beta_n = PR_soma_gating(V_m)

"""Plot Results"""
plt.figure(1)
plt.subplot(511)
plt.plot(V_m, alpha_mca, label="Activation")
plt.plot(V_m, beta_mca, label="Deactivation")
plt.xlabel("Membrane Potential (V)")
plt.title("Dendritic Calcium Rate Constants")
plt.legend()
plt.subplot(512)
plt.plot(V_m, alpha_kca, label="Activation")
plt.plot(V_m, beta_kca, label="Deactivation")
plt.xlabel("Membrane Potential (V)")
plt.title("Dendritic Calcium-dependent Potassium Rate Constants")
plt.legend()
plt.subplot(513)
plt.plot(Ca, alpha_kahp, label="Activation")
plt.plot(Ca, beta_kahp, label="Deactivation")
plt.xlabel("Calcium Concentration (M)")
plt.title("Dendritic After-Hyperpolarization Rate Constants")
plt.legend()
#Plot of somatic gating variables
plt.subplot(514)
plt.plot(V_m, alpha_m, label="Activation")
plt.plot(V_m, beta_m, label="Deactivation")
plt.plot(V_m, alpha_h, label="Inactivation")
plt.plot(V_m, beta_h, label="Deinactivation")
plt.xlabel("Membrane Potential (V)")
plt.title("Somatic Sodium Rate Constants")
plt.legend()
plt.subplot(515)
plt.plot(V_m, alpha_n, label="Activation")
plt.plot(V_m, beta_n, label="Deactivation")
plt.xlabel("Membrane Potential (V)")
plt.title("Somatic Potassium Rate Constants")
plt.legend()
plt.subplots_adjust(top=3.0, bottom=0.1, left=0.1, right=1.0, hspace=0.5,
                    wspace=0.5)
plt.savefig(desktop + "Germaine_2_figure.png", bbox_inches='tight')
plt.show()

end = timeit.time.time()
print("Time to run: " + str(round((end-start),2)) + " seconds")