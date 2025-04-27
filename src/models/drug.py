from dataclasses import dataclass
from typing import List, Dict, Optional, Union, Literal

@dataclass
class Effect:
    """Represents a drug effect."""
    name: str
    priority: int
    multiplier: float = 1.0
    
    def __str__(self) -> str:
        return self.name

@dataclass
class Ingredient:
    """Represents an ingredient that can be combined."""
    name: str
    base_effect: str
    price: float
    
    def __str__(self) -> str:
        return self.name

@dataclass
class Strain:
    """Represents a marijuana strain."""
    name: str
    base_effect: str
    cost: float
    
    def __str__(self) -> str:
        return self.name

@dataclass
class DrugType:
    """Represents a type of drug that can be produced."""
    name: str
    base_price: float
    cost_formula: str
    production_units: Dict[str, int]
    
    def __str__(self) -> str:
        return self.name.capitalize()

@dataclass
class CombinationRule:
    """Represents a rule for combining effects."""
    base: str
    base_effect: str
    modifier: str
    result_effect: str
    modifier_effect: str
    
    def __str__(self) -> str:
        return f"{self.base_effect} + {self.modifier} = {self.result_effect}"

@dataclass
class DrugOptions:
    """Options for drug production."""
    drug_type: Literal["marijuana", "meth", "cocaine"]
    grow_tent: bool = False
    pgr: bool = False
    strain: Optional[str] = None
    quality: Optional[int] = None
    
    def __str__(self) -> str:
        options = [f"Type: {self.drug_type.capitalize()}"]
        if self.grow_tent:
            options.append("Grow Tent: Yes")
        if self.pgr:
            options.append("PGR: Yes")
        if self.strain:
            options.append(f"Strain: {self.strain}")
        if self.quality:
            quality_names = ["Low", "Medium", "High"]
            options.append(f"Quality: {quality_names[self.quality-1]}")
        return ", ".join(options)

@dataclass
class OptimizationResult:
    """Result of an optimization run."""
    effects: List[str]
    path: List[str]
    ingredient_cost: float
    production_cost: float
    base_price: float
    total_value: float
    
    @property
    def total_cost(self) -> float:
        return self.production_cost + self.ingredient_cost
    
    @property
    def profit(self) -> float:
        return self.total_value - self.total_cost
    
    def __str__(self) -> str:
        return f"Profit: ${self.profit:.2f}, Effects: {len(self.effects)}, Ingredients: {len(self.path)}"
