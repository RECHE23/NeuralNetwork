from typing import Tuple, Optional
import numpy as np
from . import Layer


class Reshape(Layer):
    """
    A layer for reshaping the input data to a specified shape.

    Parameters:
    -----------
    output_shape : tuple
        Desired shape of the output data.
    dtype : str, optional
        Data type of the output data. Default is 'float32'.
    *args, **kwargs:
        Additional arguments to pass to the base class.

    Methods:
    --------
    _forward_propagation(input_data: np.ndarray) -> None:
        Reshape the input data to the specified output shape.
    _backward_propagation(upstream_gradients: np.ndarray, y_true: np.ndarray) -> None:
        Reshape the upstream gradients to match the input shape.

    Attributes:
    -----------
    dtype : str
        Data type of the output data.
    input_shape : tuple or None
        Shape of the input data.
    output_shape : tuple
        Desired shape of the output data.
    """

    def __init__(self, output_shape: Tuple[int, ...], dtype: str = 'float32', *args, **kwargs):
        """
        Initialize the Reshape with the desired output shape and data type.

        Parameters:
        -----------
        output_shape : tuple
            Desired shape of the output data.
        dtype : str, optional
            Data type of the output data. Default is 'float32'.
        *args, **kwargs:
            Additional arguments to pass to the base class.
        """
        self.dtype: str = dtype
        self._output_shape: Tuple[int, ...] = output_shape
        super().__init__(*args, **kwargs)

    @property
    def output_shape(self) -> Tuple[int, ...]:
        """
        Get the output shape (batch_size, output_shape) of the data.
        """
        return self._output_shape

    def __repr__(self) -> str:
        input_shape = f"input_shape={self.input_shape}, " if self.input else ""
        return f"{self.__class__.__name__}({input_shape}output_shape={self.output_shape}, dtype={self.dtype})"

    def _forward_propagation(self, input_data: np.ndarray) -> None:
        """
        Reshape the input data to the specified output shape.

        Parameters:
        -----------
        input_data : np.ndarray
            The input data to be reshaped.
        """
        self.output = np.reshape(input_data.astype(self.dtype), (-1, *self.output_shape))

    def _backward_propagation(self, upstream_gradients: np.ndarray, y_true: np.ndarray) -> None:
        """
        Reshape the upstream gradients to match the input shape.

        Parameters:
        -----------
        upstream_gradients : np.ndarray
            Upstream gradients coming from the subsequent layer.
        y_true : np.ndarray
            The true labels (not used in this layer).
        """
        self.retrograde = np.reshape(upstream_gradients, (-1, *self.input_shape[1:]))
