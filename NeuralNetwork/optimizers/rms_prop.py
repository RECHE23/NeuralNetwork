from typing import List, Optional
import numpy as np
from .optimizer import Optimizer


class RMSprop(Optimizer):
    """
    RMSprop optimizer.

    This optimizer adapts the learning rate for each parameter based on the moving average
    of squared gradients. It aims to mitigate the vanishing and exploding gradient problems.

    Parameters:
    -----------
    rho : float, optional
        The decay factor for the moving average. Default is 0.9.
    epsilon : float, optional
        A small value added to the denominator for numerical stability. Default is 1e-7.
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
    rho : float
        The decay factor for the moving average.
    epsilon : float
        A small value added to the denominator for numerical stability.
    cache : list of arrays or None
        The moving average of squared gradients, initialized to None.

    Methods:
    --------
    update(parameters, gradients)
        Update the parameters using RMSprop optimization.

    """
    def __init__(self, rho: float = 0.9, epsilon: float = 1e-7, *args, **kwargs):
        """
        Initialize the RMSprop optimizer with hyperparameters.

        Parameters:
        -----------
        rho : float, optional
            The decay factor for the moving average. Default is 0.9.
        epsilon : float, optional
            A small value added to the denominator for numerical stability. Default is 1e-7.
        *args, **kwargs
            Additional arguments passed to the base class Optimizer.

        """
        self.rho: float = rho
        self.epsilon: float = epsilon
        self.cache: Optional[List[np.ndarray]] = None
        super().__init__(*args, **kwargs)

    def update(self, parameters: List[np.ndarray], gradients: List[np.ndarray]) -> List[np.ndarray]:
        """
        Update the parameters using RMSprop optimization.

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
            # Update cache: cache = rho * cache + (1 - rho) * gradient * gradient
            cached = self.rho * cached + (1 - self.rho) * gradient * gradient

            # Update parameter using RMSprop update: parameter -= learning_rate * gradient / (sqrt(cache) + epsilon)
            parameter -= self.learning_rate * gradient / (np.sqrt(cached) + self.epsilon)

            # Update attribute
            self.cache[i] = cached
            updated_parameters.append(parameter)

        return updated_parameters
