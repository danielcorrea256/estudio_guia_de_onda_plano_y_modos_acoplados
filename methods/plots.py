import matplotlib.pyplot as plt
import math
import numpy as np
from metodo_ondulatorio import metodo_ondulatorio

solution = metodo_ondulatorio(
        n_co=1.5, 
        n_cl=1,
        h=1,
        k_0=2,
        lambd=1,
        ms=range(3))

def get_k(n_co, theta, lambd):
    # finds value k with the angle theta given in degrees
    return (2 * math.pi*n_co*math.cos(math.radians(theta)))/lambd

def get_gamma(k,h):
    # finds value gamma given value k
    return k*math.tan(k*h/2)

def get_E_y_even(gamma, k, h):
    # returns function corresponding to Epsilon_y used in even TE modes

    # calculate coefficients assumming c_1 = 1
    C_0 = math.cos(k*h/2)
    C_1 = 1

    outside_function = lambda x: C_0*math.exp(-1*gamma*(abs(x)-(h/2)))
    inside_function = lambda x: C_1 * math.cos(k*x)

    return lambda x: inside_function(x) if abs(x) <= h/2 else outside_function(x)

def get_E_y_odd(gamma, k, h):
    # returns function corresponding to Epsilon_y used in odd TE modes

    #calculate coefficients assumming c_1 = 1
    # C_0 = math.cos(k*h/2)
    # C_1 = 1

    # C_0 = 0.76
    # C_1 = 1

    left_function = lambda x: -1*C_0*math.exp(gamma*(x+(h/2)))

    center_function = lambda x: C_1*math.sin(k*x)

    # def center_function(x):
    #     print('hi')
    #     return C_1*math.sin(k*x)

    right_function= lambda x: C_0*math.exp(-1*gamma*(x-(h/2)))

    return lambda x: left_function(x) if x<(h/-2) else center_function(x) if abs(x)<=(h/2) else right_function(x)

def get_H_y_even(gamma, k, h):
    # returns function corresponding to H_y used in even TM modes
    C_0 = (k/gamma) * math.sin(k*h/2)
    C_1 = 1

    outside_function = lambda x: C_0* math.exp(-1*gamma*(abs(x)-h/2))
    inside_function = lambda x: C_1 * math.cos(k*x)

    return lambda x: inside_function(x) if abs(x)<=h/2 else outside_function(x)

def get_H_y_odd(gamma, k, h):
    # returns function corresponding to H_t used in odd TM modes

    right_function = lambda x: C_0*math.exp(-1*gamma*(x-h/2))
    center_function = lambda x: C_1*math.sin(k*x)
    left_function = lambda x: -1*C_0 * math.exp(gamma*(x+h/2))

    return lambda x: left_function(x) if x<(h/-2) else center_function(x) if abs(x)<=(h/2) else right_function(x)


def get_figure(X, function, label):
    # takes a range of x values and a function and returns a figure object of the plot
    y = [function(x) for x in X]

    plot = plt.plot(x,y)
    plt.xlabel('x')
    plt.ylabel(label)

    return plot[0].figure


# gamma_TE = get_gamma(k_TE, 1)

# k_TM = get_k(1.5,solution['TM'][0],1)

# gamma_TM = get_gamma(k_TM, 1)

E_y = get_E_y_odd(3.87, 4.55, 1)

x = np.linspace(-2,2,100)

figure = get_figure(x, E_y, r"$\varepsilon_y (x)$")

figure.savefig('plot')