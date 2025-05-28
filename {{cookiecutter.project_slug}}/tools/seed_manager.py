"""Utility for managing random seeds to ensure reproducibility.

This module provides functions to set and get random seeds for various libraries
that use random number generation, ensuring reproducibility across runs.
"""

import os
import random
from typing import Optional, Dict, Any
import numpy as np
import torch

# Try to import other common ML libraries
try:
    import tensorflow as tf
except ImportError:
    tf = None

try:
    import jax
    import jax.numpy as jnp
except ImportError:
    jax = None
    jnp = None


class SeedManager:
    """Manager for random seeds across different libraries.
    
    This class provides a unified interface to set random seeds for various
    libraries that use random number generation, ensuring reproducibility.
    
    Attributes:
        seed (int): The current random seed.
        libraries (Dict[str, bool]): Dictionary indicating which libraries
            have been seeded.
    """
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize the SeedManager with an optional seed.
        
        Args:
            seed: The random seed to use. If None, a random seed will be generated.
        """
        if seed is None:
            seed = random.randint(0, 2**32 - 1)
        self.seed = seed
        self.libraries: Dict[str, bool] = {
            'python': False,
            'numpy': False,
            'pytorch': False,
            'tensorflow': False,
            'jax': False,
        }
    
    def seed_everything(self, libraries: Optional[list] = None) -> Dict[str, bool]:
        """Set random seeds for specified libraries.
        
        Args:
            libraries: List of libraries to seed. If None, all available
                libraries will be seeded.
                
        Returns:
            Dict indicating which libraries were successfully seeded.
        """
        if libraries is None:
            libraries = list(self.libraries.keys())
            
        results = {}
        
        if 'python' in libraries and hasattr(random, 'seed'):
            random.seed(self.seed)
            self.libraries['python'] = True
            results['python'] = True
            
        if 'numpy' in libraries and np is not None:
            np.random.seed(self.seed)
            self.libraries['numpy'] = True
            results['numpy'] = True
            
        if 'pytorch' in libraries and torch is not None:
            torch.manual_seed(self.seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed_all(self.seed)
                torch.backends.cudnn.deterministic = True
                torch.backends.cudnn.benchmark = False
            self.libraries['pytorch'] = True
            results['pytorch'] = True
            
        if 'tensorflow' in libraries and tf is not None:
            tf.random.set_seed(self.seed)
            os.environ['TF_DETERMINISTIC_OPS'] = '1'
            os.environ['TF_DISABLE_SEGMENT_REDUCTION_OP_DETERMINISM_EXCEPT_WEB_LAYER'] = '1'
            self.libraries['tensorflow'] = True
            results['tensorflow'] = True
            
        if 'jax' in libraries and jax is not None:
            jax.config.update('jax_enable_x64', True)
            key = jax.random.PRNGKey(self.seed)
            jax.random.PRNGKey = lambda _: key  # type: ignore
            self.libraries['jax'] = True
            results['jax'] = True
            
        return results
    
    def get_state(self) -> Dict[str, Any]:
        """Get the current state of the seed manager.
        
        Returns:
            Dictionary containing the current seed and library states.
        """
        return {
            'seed': self.seed,
            'libraries': self.libraries.copy(),
        }
    
    def __repr__(self) -> str:
        """Return a string representation of the seed manager."""
        libs = ", ".join(f"{k}:{'✓' if v else '✗'}" for k, v in self.libraries.items())
        return f"<SeedManager(seed={self.seed}, libraries={{{libs}}})>"


# Global instance for convenience
seed_manager = SeedManager()


def set_global_seed(seed: int) -> None:
    """Set the global random seed for all supported libraries.
    
    This is a convenience function that creates and configures a global
    SeedManager instance.
    
    Args:
        seed: The random seed to use.
    """
    global seed_manager
    seed_manager = SeedManager(seed)
    seed_manager.seed_everything()


def get_global_seed() -> int:
    """Get the current global random seed.
    
    Returns:
        The current global random seed.
    """
    return seed_manager.seed


def get_seed_manager() -> SeedManager:
    """Get the global SeedManager instance.
    
    Returns:
        The global SeedManager instance.
    """
    return seed_manager


# Example usage
if __name__ == "__main__":
    # Set a specific seed
    set_global_seed(42)
    
    # Or use the manager directly
    manager = SeedManager(42)
    manager.seed_everything()
    
    # Check which libraries were seeded
    print(f"Seeded libraries: {manager.libraries}")
    
    # Get the current state
    state = manager.get_state()
    print(f"Current state: {state}")
