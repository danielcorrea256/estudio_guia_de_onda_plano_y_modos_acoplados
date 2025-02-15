import numpy as np
import math
from methods.metodo_rayos import funcion_rayo,metodo_rayo

def f_TE(theta,m):
    return 6*math.pi*math.cos(theta) - 4*math.atan((math.sqrt((2.25*math.sin(theta)**2)-1))/(1.5*math.cos(theta)))-2*m*math.pi

def f_TM(theta,m):
    return 6*math.pi*math.cos(theta) - 4*math.atan(1.5*(math.sqrt((2.25*math.sin(theta)**2)-1))/(math.cos(theta)))-2*m*math.pi

theta_c = math.asin(2/3)

def test_TE_function():
    # prueba que la función retornada por funcion_rayo para el modo TE sea la correcta en el intervalo [theta_critico, pi/2]
    linspace = np.linspace(theta_c, math.pi/2, 50)

    # probar para valores de m=0,1,2
    for m in range(3):
        f_rayo = funcion_rayo(n_co=1.5,n_t=1,h=1,k_0=2,m=0,modo='TE')
        result = [f_rayo(theta) for theta in linspace]
        real = [f_TE(theta, 0) for theta in linspace]

        assert np.allclose(result, real)



def test_TM_function():
    # prueba que la función retornada por funcion_rayo para el modo TM sea la correcta en el intervalo [theta_critico, pi/2]
    linspace = np.linspace(theta_c, math.pi/2, 50)

    # probar para valores de m=0,1,2
    for m in range(3):
        f_rayo = funcion_rayo(n_co=1.5,n_t=1,h=1,k_0=2,m=0,modo='TM')
        result = [f_rayo(theta) for theta in linspace]
        real = [f_TM(theta, 0) for theta in linspace]

        assert np.allclose(result, real)

# valores reales para los angulos dado m=0,1,2
real_values_TE = [75,59.5,43.8]

real_values_TM = [72.9, 55.5, 42.5]

def test_result():
    result = metodo_rayo(n_co=1.5,n_t=1,h=1,k_0=2,ms=range(3))

    result_TE_array = list(result['TE'].values())

    assert np.allclose(result_TE_array,real_values_TE, atol=0.1)

    result_TM_array = list(result['TM'].values())

    assert np.allclose(result_TM_array, real_values_TM, atol=0.1)
