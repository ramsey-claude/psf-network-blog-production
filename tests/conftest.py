"""Shared fixtures for the pipeline test suite."""
import sys
from pathlib import Path

# Make workflow/ importable so tests can hit check_rules / deliver internals
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / 'workflow'))
