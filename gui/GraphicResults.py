import matplotlib.pyplot as plt
import math
import numpy as np
from methods.metodo_ondulatorio import metodo_ondulatorio, get_W


class GraphicResults:
    def __init__(self, n_co, n_cl, h, lambd, ms=range(3)):
        """
        Initializes the GraphicResults object with waveguide parameters.

        Args:
            n_co (float): Core refractive index.
            n_cl (float): Cladding refractive index.
            h (float): Waveguide height.
            lambd (float): Wavelength.
            ms (iterable, optional): Mode indices to compute (default range(3)).
        """
        self.n_co = n_co
        self.n_cl = n_cl
        self.h = h
        self.lambd = lambd

        # Precompute mode solutions using your provided method (assumed to return a dict with keys "TE" and "TM")
        self.solution = metodo_ondulatorio(
            n_co=self.n_co, 
            n_cl=self.n_cl,
            h=self.h,
            lambd=self.lambd,
            ms=ms
        )


    def get_kappa(self, theta):
        """
        Computes kappa given an angle theta (in degrees).
        """
        k0 = 2*math.pi / self.lambd
        return (k0 * self.n_co * math.cos(math.radians(theta)))


    def get_gamma(self, m, mode):
        """
        Computes gamma based on kappa and the waveguide height.
        """
        U = self.get_kappa(self.solution[mode][m]) * self.h / 2
        W = get_W(self.n_co, self.n_cl, m, mode)

        return 2 * W(U) / self.h


    # TE field functions
    def get_E_y_even(self, gamma, kappa):
        h = self.h
        C_0 = math.cos(kappa * h / 2)
        C_1 = 1
        outside_function = lambda x: C_0 * math.exp(-gamma * (abs(x) - h / 2))
        inside_function = lambda x: C_1 * math.cos(kappa * x)
        return lambda x : inside_function(x) if abs(x) <= h / 2 else outside_function(x)


    def get_E_y_odd(self, gamma, kappa):
        h = self.h
        C_0 = math.cos(kappa * h / 2)
        C_1 = 1
        left_function = lambda x: -C_0 * math.exp(gamma * (x + h / 2))
        center_function = lambda x: C_1 * math.sin(kappa * x)
        right_function = lambda x: C_0 * math.exp(-gamma * (x - h / 2))
        return lambda x: left_function(x) if x < -h / 2 else center_function(x) if abs(x) <= h / 2 else right_function(x)


    # TM field functions
    def get_H_y_even(self, gamma, kappa):
        h = self.h
        C_0 = (kappa / gamma) * math.sin(kappa * h / 2)
        C_1 = 1
        outside_function = lambda x: C_0 * math.exp(-gamma * (abs(x) - h / 2))
        inside_function = lambda x: C_1 * math.cos(kappa * x)
        return lambda x: inside_function(x) if abs(x) <= h / 2 else outside_function(x)


    def get_H_y_odd(self, gamma, kappa):
        h = self.h
        C_0 = (kappa / gamma) * math.sin(kappa * h / 2)
        C_1 = 1
        left_function = lambda x: -C_0 * math.exp(gamma * (x + h / 2))
        center_function = lambda x: C_1 * math.sin(kappa * x)
        right_function = lambda x: C_0 * math.exp(-gamma * (x - h / 2))
        return lambda x: left_function(x) if x < -h / 2 else center_function(x) if abs(x) <= h / 2 else right_function(x)


    def plot_fields(self, mode, m, parity=None, x_range=None):
        """
        Generates and returns a matplotlib figure with two subplots:
        - Left: Electric field (E)
        - Right: Magnetic field (H)
        
        Args:
            mode (str): "TE" or "TM".
            m (int): Mode index.
            parity (str, optional): "even" or "odd". If not provided, defaults to even if m is even,
                                    odd if m is odd.
            x_range (array-like, optional): Range of x values to plot. Defaults to np.linspace(-2,2,100).
        
        Returns:
            matplotlib.figure.Figure: The generated figure.
        """
        if parity is None:
            parity = "even" if m % 2 == 0 else "odd"
        mode = mode.upper()
        try:
            theta = self.solution[mode][m]
        except Exception as e:
            raise ValueError(f"Solution for mode {mode} with m={m} not found: {e}")
        kappa = self.get_kappa(theta)
        gamma = self.get_gamma(m, mode)

        # For the electric field, use the E_y functions (for TE modes) and similarly for TM modes.
        # (Assuming the same functions can be used for both cases.)
        if parity.lower() == "even":
            E_func = self.get_E_y_even(gamma, kappa)
            H_func = self.get_H_y_even(gamma, kappa)
        else:
            E_func = self.get_E_y_odd(gamma, kappa)
            H_func = self.get_H_y_odd(gamma, kappa)
        
        if x_range is None:
            x_range = np.linspace(-2, 2, 100)
        E_vals = [E_func(x) for x in x_range]
        H_vals = [H_func(x) for x in x_range]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        ax1.plot(x_range, E_vals)
        ax1.set_xlabel('x')
        ax1.set_ylabel(r"$\varepsilon_y(x)$")
        ax1.set_title(f"{mode} mode E-field (m={m}, {parity})")

        ax2.plot(x_range, H_vals)
        ax2.set_xlabel('x')
        ax2.set_ylabel(r"$H_z(x)$")
        ax2.set_title(f"{mode} mode H-field (m={m}, {parity})")

        fig.tight_layout()
        return fig


# ---------------------------
# Example usage:
# ---------------------------
if __name__ == "__main__":
    # Create a GraphicResults instance with some parameters.
    gr = GraphicResults(n_co=1.5, n_cl=1.0, h=1.0, lambd=1.0)
    # For example, plot the TE mode with m=0 (default parity even for m=0)
    fig = gr.plot_fields("TE", m=0)
    # Save the figure
    fig.savefig("TE_mode_m0.png")
