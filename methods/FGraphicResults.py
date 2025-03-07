"""
FGraphicResults Module

This module defines the `FGraphicResults` class, which calculates and plots 
the optical coupling phenomenon in a two-waveguide system, parameterized by 
two effective indices and a wavelength. The class provides methods to compute 
key parameters (beta, delta, kappa, psi) and to plot the resulting Pa and Pb 
functions for a given F value.

Usage:
    from FGraphicResults import FGraphicResults
    
    f_results = FGraphicResults(n_eff1=1.45, n_eff2=1.29, lambd=1.0)
    fig = f_results.plot_F_graphs(F_value=0.2)
    fig.show()
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('qtagg')

class FGraphicResults:
    """
    A class for computing and plotting F-based coupling results in 
    a two-waveguide system.

    Attributes:
        n_eff1 (float): Effective index 1.
        n_eff2 (float): Effective index 2.
        lambd (float): Wavelength.
        beta1 (float): Computed beta for n_eff1.
        beta2 (float): Computed beta for n_eff2.
        delta (float): Half the difference between beta1 and beta2.
    """

    def __init__(self, n_eff1, n_eff2, lambd):
        """
        Initializes the FGraphicResults object with effective indices and wavelength.
        
        Args:
            n_eff1 (float): Effective index 1.
            n_eff2 (float): Effective index 2.
            lambd (float): Wavelength.
        """
        self.n_eff1 = n_eff1
        self.n_eff2 = n_eff2
        self.lambd = lambd
        # Compute beta values for each effective index.
        self.beta1 = self.get_beta(n_eff1, lambd)
        self.beta2 = self.get_beta(n_eff2, lambd)
        # Delta is defined as half the difference between beta1 and beta2.
        self.delta = self.get_delta(self.beta1, self.beta2)

    def get_lc(self, psi):
        """
        Computes the coupling length (L_c) given psi.

        Args:
            psi (float): The psi parameter derived from kappa and delta.

        Returns:
            float: The coupling length as π/(2 * psi).
        """
        return np.pi / 2 * psi

    def get_beta(self, n_eff, lambd):
        """
        Computes beta = k0 * n_eff.
        
        Args:
            n_eff (float): Effective refractive index.
            lambd (float): Wavelength.
        
        Returns:
            float: The computed beta.
        """
        k0 = 2 * np.pi / lambd
        return k0 * n_eff

    def get_delta(self, beta1, beta2):
        """
        Computes delta as half the difference between beta1 and beta2.
        
        Args:
            beta1 (float): Beta corresponding to n_eff1.
            beta2 (float): Beta corresponding to n_eff2.
        
        Returns:
            float: The delta value (half of beta1 - beta2).
        """
        return (beta1 - beta2) / 2

    def get_kappa(self, F):
        """
        Computes kappa based on the delta and the parameter F.
        
        Args:
            F (float): The F parameter.
            
        Returns:
            float: The computed kappa.
        """
        return self.delta / np.sqrt(1 / F - 1)

    def get_psi(self, kappa):
        """
        Computes psi as the square root of delta^2 + kappa^2.
        
        Args:
            kappa (float): The kappa parameter derived from delta and F.
            
        Returns:
            float: The computed psi.
        """
        return np.sqrt(self.delta**2 + kappa**2)

    def Pa(self, z, psi, F):
        """
        Computes Pa as 1 - F * sin^2(psi*z).
        
        Args:
            z (array-like): x values.
            psi (float): The psi parameter.
            F (float): The F parameter.
            
        Returns:
            array-like: Computed Pa values at each point in z.
        """
        return 1 - F * np.sin(psi * z)**2

    def Pb(self, z, psi, F):
        """
        Computes Pb as F * sin^2(psi*z).
        
        Args:
            z (array-like): x values.
            psi (float): The psi parameter.
            F (float): The F parameter.
            
        Returns:
            array-like: Computed Pb values at each point in z.
        """
        return F * np.sin(psi * z)**2

    def plot_F_graphs(self, F_value, x_points=100):
        """
        Generates and returns a matplotlib figure for a single F value.
        The plot displays the curves for Pa(z) and Pb(z) versus z, and additional
        information is shown below the graph.
        
        Args:
            F_value (float): The F value to plot.
            x_points (int, optional): Number of points for the x-axis. Defaults to 100.
            
        Returns:
            matplotlib.figure.Figure: The generated figure.
        """
        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(7, 4))

        # Compute kappa and psi for the given F value
        kappa = self.get_kappa(F_value)
        psi = self.get_psi(kappa)
        l_c = (np.pi / 2) * psi  # Coupling length

        # Determine the maximum x-value in multiples of pi/2
        x_max_original = (2 * np.pi) / psi
        N = int(np.ceil(x_max_original / (np.pi / 2)))
        max_tick = N * (np.pi / 2)

        # Generate x range and compute Pa/Pb
        x_range = np.linspace(0, max_tick, x_points)
        pa_values = self.Pa(x_range, psi, F_value)
        pb_values = self.Pb(x_range, psi, F_value)

        # Plot Pa and Pb with distinct styles
        ax.plot(x_range, pa_values, label=r"$P_a(z)$", color="royalblue", linewidth=2)
        ax.plot(x_range, pb_values, label=r"$P_b(z)$", color="crimson", linewidth=2)

        ax.set_xlabel("z", fontsize=11)
        ax.set_ylabel("", fontsize=11)
        ax.set_title(rf"$F = {F_value}$", fontsize=13)
        ax.legend(fontsize=10)

        # Enable grid for clarity
        ax.grid(True, linestyle=":", color="gray", alpha=0.3)

        # Set x-ticks at increments of pi/2
        tick_positions = [n * (np.pi / 2) for n in range(N + 1)]
        tick_labels = []
        for n in range(N + 1):
            if n == 0:
                tick_labels.append("0")
            elif n == 1:
                tick_labels.append(r"$\frac{\pi}{2}$")
            elif n == 2:
                tick_labels.append(r"$\pi$")
            else:
                tick_labels.append(rf"${n}\frac{{\pi}}{{2}}$")

        ax.set_xticks(tick_positions)
        ax.set_xticklabels(tick_labels, fontsize=10)

        # Tight layout, reserving space at the bottom for additional info
        fig.tight_layout(rect=(0, 0.3, 1, 0.95))

        # Place a bold 'Parameters' title below the main plot
        fig.text(0.5, 0.2, "Parameters", ha="center", va="bottom", fontsize=12, fontweight="bold")

        # Additional info text using LaTeX formatting
        additional_info = (
            r"$n_{eff_1} = " + f"{self.n_eff1}" +
            r",\quad n_{eff_2} = " + f"{self.n_eff2}" +
            r",\quad \lambda = " + f"{self.lambd}" + r"$" + "\n" + r"$" +
            r"\quad \beta_1 = " + f"{self.beta1:.2f}" +
            r",\quad \beta_2 = " + f"{self.beta2:.2f}" +
            r",\quad \delta = " + f"{self.delta:.2f}" + r"$" + "\n" + r"$" +
            r"\quad \kappa = " + f"{kappa:.2f}" +
            r",\quad \psi = " + f"{psi:.2f}" +
            r",\quad L_c = " + f"{l_c:.2f}" + r"$"
        )

        # Place the additional info text below the 'Parameters' title
        fig.text(0.5, 0.05, additional_info, ha="center", va="bottom", fontsize=10)

        return fig


# --------------------------
# Example usage:
# --------------------------
if __name__ == "__main__":
    # Create an instance with effective indices and wavelength.
    f_results = FGraphicResults(n_eff1=1.45, n_eff2=1.29, lambd=1)
    # Generate the plot for F values 0.2 and 0.5.
    fig = f_results.plot_F_graphs(F_value=0.2)
    # Display the plot.
    plt.show()
