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

    def plot_F_graphs(self, F_values=[0.2, 0.5], x_points=100):
        """
        Generates and returns a matplotlib figure with subplots for each provided F value.
        Each subplot displays the curves for Pa and Pb versus x.
        
        Args:
            F_values (list, optional): List of F values to plot. Defaults to [0.2, 0.5].
            x_points (int, optional): Number of x values for plotting. Defaults to 100.
        
        Returns:
            matplotlib.figure.Figure: The generated figure.
        """
        num_plots = len(F_values)
        fig, axs = plt.subplots(1, num_plots, figsize=(6 * num_plots, 4))
        # In case there is only one subplot, ensure axs is iterable.
        if num_plots == 1:
            axs = [axs]
        for ax, F in zip(axs, F_values):
            kappa = self.get_kappa(F)
            psi = self.get_psi(kappa)
            # Define x range: from 0 to 2*pi/psi.
            x_range = np.linspace(0, 2 * np.pi / psi, x_points)
            pa_values = self.Pa(x_range, psi, F)
            pb_values = self.Pb(x_range, psi, F)
            ax.plot(x_range, pa_values, label="Pa(z)")
            ax.plot(x_range, pb_values, label="Pb(z)")
            ax.set_xlabel("z")
            ax.set_ylabel("")
            ax.set_title(f"F = {F}")
            ax.legend()
        fig.tight_layout()
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
