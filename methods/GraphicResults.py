import matplotlib.pyplot as plt
import matplotlib
import math
import numpy as np
import methods.field_functions as ff
from methods.metodo_ondulatorio import metodo_ondulatorio

matplotlib.use('qtagg')

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
        # Precompute mode solutions (assumed to return a dict with keys "TE" and "TM")
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
        k0 = 2 * math.pi / self.lambd
        return k0 * self.n_co * math.cos(math.radians(theta))

    def get_gamma(self, kappa, mode, parity):
        """
        Computes gamma based on kappa and the waveguide height.
        """
        h = self.h
        if mode.upper() == 'TE':
            if parity == 'even':
                return kappa * math.tan(kappa * h / 2)
            elif parity == 'odd':
                return -kappa / math.tan(kappa * h / 2)
        elif mode.upper() == 'TM':
            if parity == 'even':
                return ((self.n_cl/self.n_co)**2) * kappa * math.tan(kappa * h / 2)
            elif parity == 'odd':
                return -((self.n_cl/self.n_co)**2) * kappa / math.tan(kappa * h / 2)

    def plot_fields(self, mode, m, parity=None, x_range=None):
        """
        Generates and returns a matplotlib figure with two subplots:
        - Left: Electric field (E)
        - Right: Magnetic field (H)
        
        Args:
            mode (str): "TE" or "TM".
            m (int): Mode index.
            parity (str, optional): "even" or "odd". Defaults based on m.
            x_range (array-like, optional): Range of x values to plot.
            
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
        
        kappa_val = self.get_kappa(theta)
        gamma_val = self.get_gamma(kappa_val, mode, parity)

        # Select field functions based on mode and parity
        if mode == "TE":
            first_label = r"$\varepsilon_y(x)$"
            second_label = r"$H_z(x)$"
            if parity.lower() == "even":
                E_func = ff.get_E_y_even(self.h, gamma_val, kappa_val)
                H_func = ff.get_H_z_even(self.h, gamma_val, kappa_val)
            else:
                E_func = ff.get_E_y_odd(self.h, gamma_val, kappa_val)
                H_func = ff.get_H_z_odd(self.h, gamma_val, kappa_val)
        else:  # mode == "TM"
            first_label = r"$\varepsilon_z(x)$"
            second_label = r"$H_y(x)$"
            if parity.lower() == "even":
                E_func = ff.get_E_z_even(self.h, gamma_val, kappa_val)
                H_func = ff.get_H_y_even(self.h, gamma_val, kappa_val)
            else:
                E_func = ff.get_E_z_odd(self.h, gamma_val, kappa_val)
                H_func = ff.get_H_y_odd(self.h, gamma_val, kappa_val)

        if x_range is None:
            x_range = np.linspace(-2 * self.h, 2 * self.h, 100)

        E_vals = [E_func(x) for x in x_range]
        H_vals = [H_func(x) for x in x_range]

        # Create subplots with a larger figure size
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        # Plot E field
        ax1.plot(x_range, E_vals, color="royalblue", linewidth=2)
        ax1.set_xlabel("x", fontsize=12)
        ax1.set_ylabel(first_label, fontsize=12)
        ax1.set_title(f"{mode} mode E-field (m={m}, {parity})", fontsize=14)
        ax1.grid(True, linestyle=":", color="gray", alpha=0.3)

        # Plot H field
        ax2.plot(x_range, H_vals, color="crimson", linewidth=2)
        ax2.set_xlabel("x", fontsize=12)
        ax2.set_ylabel(second_label, fontsize=12)
        ax2.set_title(f"{mode} mode H-field (m={m}, {parity})", fontsize=14)
        ax2.grid(True, linestyle=":", color="gray", alpha=0.3)

        # Optional: add a figure-wide title
        # fig.suptitle("Field Distributions for TE/TM Modes", fontsize=16, fontweight="bold")

        fig.tight_layout()
        return fig


# ---------------------------
# Example usage:
# ---------------------------
if __name__ == "__main__":
    # Create an instance of GraphicResults with some parameters.
    gr = GraphicResults(n_co=1.5, n_cl=1.0, h=1.0, lambd=1.0)
    # For example, plot the TM mode with m=0 (default parity for m=0 is even)
    fig = gr.plot_fields("TM", m=0)
    fig.savefig("TM_mode_m0.png")
