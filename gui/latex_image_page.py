import io
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap

class LatexLabel(QLabel):
    """
    A custom QLabel that renders (MathText) LaTeX as an image using Matplotlib,
    with minimal padding and a transparent background.
    """

    def __init__(self, latex_text, parent=None, fontsize=8):
        super().__init__(parent)
        pixmap = self._latex_to_pixmap(latex_text, fontsize)
        self.setPixmap(pixmap)

    def _latex_to_pixmap(self, latex_text, fontsize):
        """
        Render LaTeX text to an in-memory PNG (via Matplotlib),
        then convert to a QPixmap with minimal whitespace.
        """
        # Create a small figure. We'll rely on bbox_inches='tight' to expand only as needed.
        fig, ax = plt.subplots(figsize=(0.01, 0.01))
        
        # Place the LaTeX text at the origin (left-bottom). 
        # ha='left', va='bottom' helps minimize space.
        ax.text(0, 0, latex_text, fontsize=fontsize, ha='left', va='bottom')

        # Remove all spines/ticks and any default margin
        ax.axis('off')
        ax.margins(0, 0)
        
        # "Tight layout" can help, though we'll mainly rely on bbox_inches='tight'
        plt.tight_layout(pad=0)
        
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
