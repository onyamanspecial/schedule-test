from pathlib import Path
import yaml
from typing import Dict, Any, Optional

class ConfigManager:
    """Manages configuration loading and access for the application."""
    
    def __init__(self, config_dir: Optional[str] = None):
        """Initialize the configuration manager.
        
        Args:
            config_dir: Optional directory path for configuration files.
                        If None, uses the default data directory.
        """
        self.config_dir = Path(config_dir) if config_dir else Path(__file__).parent.parent / "data"
        self.config_cache = {}
        
    def load_config(self, name: str) -> Dict[str, Any]:
        """Load a configuration file by name.
        
        Args:
            name: Name of the configuration file (without extension)
            
        Returns:
            Dictionary containing the configuration data
            
        Raises:
            FileNotFoundError: If the configuration file doesn't exist
            ValueError: If the file format is invalid
        """
        if name in self.config_cache:
            return self.config_cache[name]
            
        file_path = self.config_dir / f"{name}.yaml"
        
        try:
            with open(file_path, 'r') as f:
                config = yaml.safe_load(f)
                self.config_cache[name] = config
                return config
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file {file_path} not found")
        except yaml.YAMLError:
            raise ValueError(f"Invalid YAML format in {file_path}")
    
    def get_all_configs(self) -> Dict[str, Any]:
        """Load and merge all configuration files into a single dictionary.
        
        Returns:
            Dictionary containing all configuration data
        """
        config_files = ["effects", "combinations", "effect_multipliers", 
                       "ingredient_prices", "drug_pricing"]
        
        result = {}
        for name in config_files:
            result[name] = self.load_config(name)
            
        return result
