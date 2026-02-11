"""Models package for PowerBIMentor.

This package contains model wrappers for AI evaluation services.
"""

from .model import Model
from .gemini import Gemini

__all__ = ["Model", "Gemini"]
