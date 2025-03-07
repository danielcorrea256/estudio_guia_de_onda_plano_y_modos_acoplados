"""
gui.latex_util Module

This module provides the `LatexLabel` class, a PySide6 `QLabel` subclass 
for rendering LaTeX math expressions. It uses Matplotlib to convert LaTeX 
strings into images (QPixmap), ensuring minimal whitespace and a transparent 
background. This allows you to display formatted mathematical equations 
directly in a PySide6 GUI.

Example:
    from latex_util import LatexLabel

    label = LatexLabel(r"$\alpha = 123$")
    layout.addWidget(label)

Classes:
    LatexLabel: Inherits from QLabel and displays LaTeX text as a rendered image.
"""


import io
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap


class LatexLabel(QLabel):
    """
    A QLabel subclass that renders LaTeX mathematical expressions as an image.

    This class uses Matplotlib to render LaTeX MathText and converts it into 
    a QPixmap for display. It ensures minimal padding and a transparent background.

    Args:
        latex_text (str): The LaTeX string to be rendered.
        parent (QWidget, optional): The parent widget. Defaults to None.
        fontsize (int, optional): The font size of the rendered LaTeX text. Defaults to 8.
    """

    def __init__(self, latex_text, parent=None, fontsize=10):
        """
        Initializes the LatexLabel with the given LaTeX text.

        Args:
            latex_text (str): The LaTeX string to render.
            parent (QWidget, optional): The parent widget. Defaults to None.
            fontsize (int, optional): Font size for the rendered LaTeX text. Defaults to 8.
        """
        super().__init__(parent)
        pixmap = LatexLabel.latex_to_pixmap(latex_text, fontsize)
        self.setPixmap(pixmap)

    @classmethod
    def latex_to_pixmap(self, latex_text, fontsize=10):
        """
        Converts LaTeX text into a QPixmap using Matplotlib.

        This method renders the given LaTeX string as an image with a transparent
        background, ensuring minimal whitespace.

        Args:
            latex_text (str): The LaTeX string to render.
            fontsize (int): The font size of the text.

        Returns:
            QPixmap: The rendered LaTeX expression as a QPixmap.
        """

        # Create a small figure. We'll rely on bbox_inches='tight' to expand only as needed.
        fig, ax = plt.subplots(figsize=(0.01, 0.01))
        
        # Place the LaTeX text at the origin (left-bottom). 
        # ha='left', va='bottom' helps minimize space.
        ax.text(0, 0, latex_text, fontsize=fontsize, ha='left', va='bottom')

        # Remove all spines/ticks and any default margin
        ax.axis('off')
        ax.margins(0, 0)
        
        # Save figure to an in-memory buffer with tight bounding box, no extra padding
        buf = io.BytesIO()
        plt.savefig(buf,
                    format='png',
                    bbox_inches='tight',
                    pad_inches=0,
                    transparent=True)
        plt.close(fig)
        buf.seek(0)

        # Convert buffer to QPixmap
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue(), "PNG")
        return pixmap
