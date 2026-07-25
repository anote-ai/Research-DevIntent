"""IntentSpec: Execution-based Intent Violation Rate measurement for LLM code generation."""

from .dataset import load_spec_pairs
from .execute import evaluate_solution, run_solution
from .ivr import compute_ivr, compute_ivr_by_type
from .schema import ConstraintTest, IVRResult, SolutionResult, SpecPair

__version__ = "0.2.0"
__all__ = [
    # schema
    "ConstraintTest",
    "IVRResult",
    "SolutionResult",
    "SpecPair",
    # ivr
    "compute_ivr",
    "compute_ivr_by_type",
    "evaluate_solution",
    # dataset
    "load_spec_pairs",
    # execute
    "run_solution",
]
