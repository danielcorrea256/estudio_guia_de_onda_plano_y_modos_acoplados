"""
methods.field_functions Module

This module provides a set of functions for calculating TE and TM field profiles 
(even and odd) in a planar waveguide. Each function returns a lambda that computes 
the field value at a given x position, based on parameters like the waveguide height (h), 
the propagation constants (kappa, gamma), and the chosen parity (even or odd).

Usage:
    from field_functions import (
        get_E_y_even, get_H_z_even, get_E_y_odd, get_H_z_odd,
        get_H_y_even, get_E_z_even, get_H_y_odd, get_E_z_odd
    )

    # Example for TE field (even):
    E_y = get_E_y_even(h, gamma, kappa)
    field_value_at_x = E_y(x)
"""

import math

# TE field functions
def get_E_y_even(h, gamma, kappa):
    """
    Returns a lambda function representing the even TE electric field profile (E_y).

    Args:
        h (float): The waveguide height.
        gamma (float): A computed propagation constant factor (for TE).
        kappa (float): A computed propagation constant factor (for TE).

    Returns:
        function: A lambda taking x as input and returning E_y(x) for the even TE mode.
    """
    C_0 = math.cos(kappa * h / 2)
    C_1 = 1
    print("C0 Ey even", C_0)
    print("C1 Ey even", C_1)
    outside_function = lambda x: C_0 * math.exp(-gamma * (abs(x) - h / 2))
    inside_function = lambda x: C_1 * math.cos(kappa * x)
    return lambda x: inside_function(x) if abs(x) <= h / 2 else outside_function(x)

def get_H_z_even(h, gamma, kappa):
    """
    Returns a lambda function representing the even TE magnetic field profile (H_z).

    Args:
        h (float): The waveguide height.
        gamma (float): A computed propagation constant factor (for TE).
        kappa (float): A computed propagation constant factor (for TE).

    Returns:
        function: A lambda taking x as input and returning H_z(x) for the even TE mode.
    """
    C_0 = (kappa / gamma) * math.sin(kappa * h / 2)
    C_1 = 1
    print("C0 Hz even", C_0)
    print("C1 Hz even", C_1)
    left_function = lambda x: gamma * C_0 * math.exp(-gamma * (abs(x) - h / 2))
    center_function = lambda x: -kappa * C_1 * math.sin(kappa * x)
    right_function = lambda x: -gamma * C_0 * math.exp(-gamma * (abs(x) - h / 2))
    return lambda x: left_function(x) if x < -h/2 else center_function(x) if abs(x) <= h/2 else right_function(x)

def get_E_y_odd(h, gamma, kappa):
    """
    Returns a lambda function representing the odd TE electric field profile (E_y).

    Args:
        h (float): The waveguide height.
        gamma (float): A computed propagation constant factor (for TE).
        kappa (float): A computed propagation constant factor (for TE).

    Returns:
        function: A lambda taking x as input and returning E_y(x) for the odd TE mode.
    """
    C_0 = math.sin(kappa * h / 2)
    C_1 = 1
    print("C0 Ey odd", C_0)
    print("C1 Ey odd", C_1)
    left_function = lambda x: -C_0 * math.exp(gamma * (x + h / 2))
    center_function = lambda x: C_1 * math.sin(kappa * x)
    right_function = lambda x: C_0 * math.exp(-gamma * (x - h / 2))
    return lambda x: left_function(x) if x < -h/2 else center_function(x) if abs(x) <= h/2 else right_function(x)

def get_H_z_odd(h, gamma, kappa):
    """
    Returns a lambda function representing the odd TE magnetic field profile (H_z).

    Args:
        h (float): The waveguide height.
        gamma (float): A computed propagation constant factor (for TE).
        kappa (float): A computed propagation constant factor (for TE).

    Returns:
        function: A lambda taking x as input and returning H_z(x) for the odd TE mode.
    """
    C_0 = -(kappa / gamma) * math.cos(kappa * h / 2)
    C_1 = 1
    print("C0 Hz odd", C_0)
    print("C1 Hz odd", C_1)
    left_function = lambda x: -C_0 * gamma * math.exp(gamma*(x + h/2))
    center_function = lambda x: C_1 * kappa * math.cos(kappa * x)
    right_function = lambda x: -C_0 * gamma * math.exp(-gamma*(x - h/2))
    return lambda x: left_function(x) if x < -h/2 else center_function(x) if abs(x) <= h/2 else right_function(x)

# TM field functions
def get_H_y_even(h, gamma, kappa):
    """
    Returns a lambda function representing the even TM magnetic field profile (H_y).

    Args:
        h (float): The waveguide height.
        gamma (float): A computed propagation constant factor (for TM).
        kappa (float): A computed propagation constant factor (for TM).

    Returns:
        function: A lambda taking x as input and returning H_y(x) for the even TM mode.
    """
    C_0 = math.cos(kappa * h / 2)
    C_1 = 1
    print("C0 Hy even", C_0)
    print("C1 Hy even", C_1)
    outside_function = lambda x: C_0 * math.exp(-gamma * (abs(x) - h / 2))
    inside_function = lambda x: C_1 * math.cos(kappa * x)
    return lambda x: inside_function(x) if abs(x) <= h / 2 else outside_function(x)

def get_E_z_even(h, gamma, kappa):
    """
    Returns a lambda function representing the even TM electric field profile (E_z).

    Args:
        h (float): The waveguide height.
        gamma (float): A computed propagation constant factor (for TM).
        kappa (float): A computed propagation constant factor (for TM).

    Returns:
        function: A lambda taking x as input and returning E_z(x) for the even TM mode.
    """
    C_0 = (kappa / gamma) * math.sin(kappa * h / 2)
    C_1 = 1
    print("C0 Ez even", C_0)
    print("C1 Ez even", C_1)
    left_function = lambda x: gamma * C_0 * math.exp(-gamma * (abs(x) - h / 2))
    center_function = lambda x: -kappa * C_1 * math.sin(kappa * x)
    right_function = lambda x: -gamma * C_0 * math.exp(-gamma * (abs(x) - h / 2))
    return lambda x: left_function(x) if x < -h/2 else center_function(x) if abs(x) <= h/2 else right_function(x)

def get_H_y_odd(h, gamma, kappa):
    """
    Returns a lambda function representing the odd TM magnetic field profile (H_y).

    Args:
        h (float): The waveguide height.
        gamma (float): A computed propagation constant factor (for TM).
        kappa (float): A computed propagation constant factor (for TM).

    Returns:
        function: A lambda taking x as input and returning H_y(x) for the odd TM mode.
    """
    C_0 = math.sin(kappa * h / 2)
    C_1 = 1
    print("C0 Hy odd", C_0)
    print("C1 Hy odd", C_1)
    left_function = lambda x: -C_0 * math.exp(gamma * (x + h / 2))
    center_function = lambda x: C_1 * math.sin(kappa * x)
    right_function = lambda x: C_0 * math.exp(-gamma * (x - h / 2))
    return lambda x: left_function(x) if x < -h/2 else center_function(x) if abs(x) <= h/2 else right_function(x)

def get_E_z_odd(h, gamma, kappa):
    """
    Returns a lambda function representing the odd TM electric field profile (E_z).

    Args:
        h (float): The waveguide height.
        gamma (float): A computed propagation constant factor (for TM).
        kappa (float): A computed propagation constant factor (for TM).

    Returns:
        function: A lambda taking x as input and returning E_z(x) for the odd TM mode.
    """
    C_0 = -(kappa / gamma) * math.cos(kappa * h / 2)
    C_1 = 1
    print("C0 Ez odd", C_0)
    print("C1 Ez odd", C_1)
    left_function = lambda x: -gamma * C_0 * math.exp(gamma * (x + h / 2))
    center_function = lambda x: kappa * C_1 * math.cos(kappa * x)
    right_function = lambda x: -gamma * C_0 * math.exp(-gamma * (x - h / 2))
    return lambda x: left_function(x) if x < -h/2 else center_function(x) if abs(x) <= h/2 else right_function(x)
