from typing import List, Optional
import numpy as np
from .optimizer import Optimizer


class Adagrad(Optimizer):
    """
    Adagrad optimizer for adaptive gradient updates.

    This optimizer adapts the learning rates individually for each parameter.

    Parameters:
    -----------
    epsilon : float, optional
        A small constant added to prevent division by zero. Default is 1e-7.
    learning_rate : float, optional
        The learning rate controlling the step size of parameter updates. Default is 1e-3.
    decay : float, optional
        The learning rate decay factor applied at the end of each epoch. Default is 0.
    lr_min : float, optional
        The minimum allowed learning rate after decay. Default is 0.
    lr_max : float, optional
        The maximum allowed learning rate after decay. Default is np.inf.
    *args, **kwargs
        Additional arguments passed to the base class Optimizer.

    Attributes:
    -----------
    epsilon : float
        A small constant added to prevent division by zero.
    cache : list of arrays or None
        The cumulative sum of squared gradients, initialized to None.

    Methods:
    --------
    update(parameters, gradients)
        Update the parameters using the Adagrad algorithm.

    """
    def __init__(self, epsilon: float = 1e-7, *args, **kwargs):
        """
        Initialize the Adagrad optimizer with hyperparameters.

        Parameters:
        -----------
        epsilon : float, optional
            A small constant added to prevent division by zero. Default is 1e-7.
        *args, **kwargs
            Additional arguments passed to the base class Optimizer.

        """
        self.epsilon: float = epsilon
        self.cache: Optional[List[np.ndarray]] = None
        super().__init__(*args, **kwargs)

    def update(self, parameters: List[np.ndarray], gradients: List[np.ndarray]) -> List[np.ndarray]:
        """
        Update the parameters using the Adagrad algorithm.

        Parameters:
        -----------
        parameters : list of arrays
            List of parameter arrays to be updated.
        gradients : list of arrays
            List of gradient arrays corresponding to the parameters.

        Returns:
        --------
        updated_parameters : list of arrays
            List of updated parameter arrays.

        """
        if self.cache is None:
            self.cache = [np.zeros(shape=parameter.shape, dtype=float) for parameter in parameters]

        updated_parameters = []
        for i, (cached, parameter, gradient) in enumerate(zip(self.cache, parameters, gradients)):
            # Update cached gradient: cache += gradient^2
            cached += gradient * gradient

            # Update parameter: parameter -= learning_rate * gradient / (sqrt(cache) + epsilon)
            parameter -= self.learning_rate * gradient / (np.sqrt(cached) + self.epsilon)

            # Update attributes
            self.cache[i] = cached
            updated_parameters.append(parameter)

        return updated_parameters
