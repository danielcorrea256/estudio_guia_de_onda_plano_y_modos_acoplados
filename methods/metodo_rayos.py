from scipy.optimize import root_scalar
import matplotlib.pyplot as plt
import numpy as np
import math


def phi(n_co, n_t, modo):
    cociente = n_co**2 / n_t**2
    inside_sqrt = lambda theta: (cociente * math.sin(theta)**2) - 1
    if modo=='TE':
        return lambda theta: math.atan((n_t / (n_co * math.cos(theta))) * math.sqrt(inside_sqrt(theta)))
    elif modo=='TM':
        return lambda theta: math.atan((n_co / (n_t * math.cos(theta))) * math.sqrt(inside_sqrt(theta)))

def funcion_rayo(n_co, n_cl, h, lambd, m, modo):

    #función phi que depende del modo (TM o TE)
    Phi = phi(n_co, n_cl, modo)
    k_0 = 2 * math.pi / lambd
    
    # La ecuación que queremos resolver
    z = lambda theta: 2 * n_co * k_0 * h * math.cos(theta) - (4 * Phi(theta)) - (2 * m * math.pi)

    return z  # Buscamos la raíz de esta función

def metodo_rayo(n_co, n_cl, h, lambd, ms, debug=False):
    TEs = {}
    TMs = {}

    # theta critico
    theta_c = math.asin(n_cl/n_co)
    for m in ms:
        # resultado para modo TE
        f_TE = funcion_rayo(n_co=n_co,n_cl=n_cl,h=h, lambd=lambd, m=m, modo='TE')
        
        if debug:
            theta_values = np.linspace(theta_c, math.pi / 2)
            f_TE_values = [f_TE(theta) for theta in theta_values]
            plt.plot(theta_values, f_TE_values)
            #plt.ylim(-1, 1)
            plt.axhline(0, color='black', linewidth=1)  # Adds an x-axis at y = 0
            plt.show()

        theta_TE = root_scalar(f_TE,method="bisect",bracket=[theta_c,math.pi/2]).root
        TEs[m] = math.degrees(theta_TE)

        # resultado para modo TM
        f_TM= funcion_rayo(n_co=n_co,n_cl=n_cl,h=h,lambd=lambd,m=m, modo='TM')
        theta_TM = root_scalar(f_TM,method="bisect",bracket=[theta_c,math.pi/2]).root
        TMs[m] = math.degrees(theta_TM)

    return {'TE': TEs, 'TM': TMs}


if __name__ == "__main__":
    metodo_rayo(1.5, 1, 1, 10, [1], True)