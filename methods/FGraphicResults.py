import numpy as np
import matplotlib.pyplot as plt

class FGraphicResults:
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
        return np.pi / 2*psi

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
            beta1 (float)
            beta2 (float)
        
        Returns:
            float: delta value.
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
            kappa (float)
            
        Returns:
            float: The computed psi.
        """
        return np.sqrt(self.delta**2 + kappa**2)

    def Pa(self, z, psi, F):
        """
        Computes Pa as 1 - F * sin^2(psi*z).
        
        Args:
            z (array-like): x values.
            psi (float)
            F (float)
            
        Returns:
            array-like: Computed Pa values.
        """
        return 1 - F * np.sin(psi * z)**2

    def Pb(self, z, psi, F):
        """
        Computes Pb as F * sin^2(psi*z).
        
        Args:
            z (array-like): x values.
            psi (float)
            F (float)
            
        Returns:
            array-like: Computed Pb values.
        """
        return F * np.sin(psi * z)**2

    def plot_F_graphs(self, F_value, x_points=100):
        """
        Generates and returns a matplotlib figure for a single F value.
        The plot displays the curves for Pa(z) and Pb(z) versus z, and additional
        information (using LaTeX math text) is shown below the graph.
        
        Args:
            F_value (float): The F value to plot.
            x_points (int, optional): Number of points for the x-axis. Defaults to 100.
            
        Returns:
            matplotlib.figure.Figure: The generated figure.
        """
        # Create a single subplot.
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Compute kappa and psi for the given F value.
        kappa = self.get_kappa(F_value)
        psi = self.get_psi(kappa)
        l_c = np.pi / 2 * psi  # note: check your parentheses if needed
        
        # Define the x range: from 0 to 2*pi/psi.
        x_range = np.linspace(0, 2 * np.pi / psi, x_points)
        
        # Compute Pa and Pb values.
        pa_values = self.Pa(x_range, psi, F_value)
        pb_values = self.Pb(x_range, psi, F_value)
        
        # Plot the curves.
        ax.plot(x_range, pa_values, label=r"$P_a(z)$")
        ax.plot(x_range, pb_values, label=r"$P_b(z)$")
        ax.set_xlabel("z")
        ax.set_ylabel("")
        ax.set_title(r"$F = " + f"{F_value}" + r"$")
        ax.legend()
        
        # Adjust layout to leave extra space at the bottom.
        fig.tight_layout(rect=(0, 0.3, 1, 0.95))
        
        # Prepare additional info text using LaTeX formatting.
        additional_info = (
            r"$n_{eff_1} = " + f"{self.n_eff1}" +
            r",\quad n_{eff_2} = " + f"{self.n_eff2}" +
            r",\quad \lambda = " + f"{self.lambd}" + r"$" + "\n" + r"$" + 
            r"\quad \beta_1 = " + f"{self.beta1:.2f}" +
            r",\quad \beta_2 = " + f"{self.beta2:.2f}" +
            r",\quad \delta = " + f"{self.delta:.2f}" + r"$" + "\n" + r"$" + 
            r"\quad \kappa = " + f"{kappa:.2f}" + 
            r",\quad \psi = " + f"{psi:.2f}" + 
            r",\quad L_c = " + f"{l_c:.2f}" + 
            r"$"
        )
        
        # Place the additional info text at the bottom center of the figure.
        # Reduced font size (e.g. fontsize=8) and move it up a bit (e.g. y=0.05) for clarity.
        fig.text(0.5, 0.1, additional_info, ha="center", va="bottom", fontsize=12)
        
        return fig



# --------------------------
# Example usage:
# --------------------------
if __name__ == "__main__":
    # Create an instance with effective indices and wavelength.
    f_results = FGraphicResults(n_eff1=1.45, n_eff2=1.29, lambd=1)
    # Generate the plot for F values 0.2 and 0.5.
    fig = f_results.plot_F_graphs(F_values=[0.2, 0.5])
    # Display the plot.
    plt.show()
