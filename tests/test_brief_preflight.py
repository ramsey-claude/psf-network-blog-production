"""Tests for workflow/brief_preflight.py.

The script enforces brief-required-sections.md. These tests pin the contract.
"""
import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_preflight():
    path = REPO_ROOT / 'workflow' / 'brief_preflight.py'
    spec = importlib.util.spec_from_file_location('brief_preflight', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope='module')
def preflight():
    return _load_preflight()


VALID_BRIEF = """\
# Brief: Test Topic

## Metadata
| Field | Value |
|-------|-------|
| Slug | test-topic |

## Target Keywords
| Keyword | Volume |
|---------|--------|
| test keyword | 100 |

## ICP
First-time investor looking to test the pipeline thoroughly.

## Content Angle
Honest comparison of test approaches with real examples and structural framing.

## Human Anchors

### A. Real Story
Marcus, a 38-year-old physical therapist in Austin, put $7,200 into three fractional shares of a duplex in Q3 2024. His first quarterly distribution was $94 and he was genuinely surprised it arrived on schedule, which he said changed his trust level immediately.

### B. POV Anchor
We think the per-square-foot model is the only fractional structure that lets a first-time investor understand exactly what they own. Crowdfunding gives you a slice of a fund; we give you a number of square feet in a specific building at a specific address that you can drive past.

### C. Contrarian Note
The standard industry view is that REITs offer liquid real-estate exposure. The catch nobody leads with is that REIT pricing tracks the stock market, not the underlying property. A REIT can fall thirty percent in a quarter even when every building in its portfolio is fully occupied and rent-paying.

### Source
Founder interview, 2026-03-14. Permission granted for anonymized use.

## Competitor Gap
- Competitor X does not cover this

## Regulatory Flags
- SEC: standard offering language
"""


def test_valid_brief_passes(preflight, tmp_path):
    f = tmp_path / 'brief.md'
    f.write_text(VALID_BRIEF)
    assert preflight.check_brief(f) == []


def test_missing_human_anchors_fails(preflight, tmp_path):
    f = tmp_path / 'brief.md'
    f.write_text(VALID_BRIEF.replace('## Human Anchors', '## Disabled Anchors'))
    failures = preflight.check_brief(f)
    assert any('Human Anchors' in x for x in failures)


def test_missing_real_story_subfield_fails(preflight, tmp_path):
    text = VALID_BRIEF.replace('### A. Real Story', '### A. Not A Story')
    f = tmp_path / 'brief.md'
    f.write_text(text)
    failures = preflight.check_brief(f)
    assert any('Real Story' in x for x in failures)


def test_short_anchor_fails(preflight, tmp_path):
    text = VALID_BRIEF.replace(
        'Marcus, a 38-year-old physical therapist in Austin, put $7,200 into three fractional shares of a duplex in Q3 2024. His first quarterly distribution was $94 and he was genuinely surprised it arrived on schedule, which he said changed his trust level immediately.',
        'Too short.',
    )
    f = tmp_path / 'brief.md'
    f.write_text(text)
    failures = preflight.check_brief(f)
    assert any('too short' in x for x in failures)


def test_placeholder_token_in_anchor_fails(preflight, tmp_path):
    text = VALID_BRIEF.replace(
        'Marcus, a 38-year-old physical therapist',
        'TODO: insert a real story here about a physical therapist',
    )
    f = tmp_path / 'brief.md'
    f.write_text(text)
    failures = preflight.check_brief(f)
    assert any('placeholder' in x.lower() for x in failures)


def test_missing_source_fails(preflight, tmp_path):
    text = VALID_BRIEF.replace('### Source\nFounder interview', '### Disabled\nFounder interview')
    f = tmp_path / 'brief.md'
    f.write_text(text)
    failures = preflight.check_brief(f)
    assert any('Source' in x for x in failures)


def test_missing_file_returns_error(preflight, tmp_path):
    failures = preflight.check_brief(tmp_path / 'does-not-exist.md')
    assert failures
    assert any('not found' in x for x in failures)


def test_all_required_sections_checked(preflight, tmp_path):
    """If we strip everything but the title, every required section should fail."""
    f = tmp_path / 'brief.md'
    f.write_text('# Brief: empty\n')
    failures = preflight.check_brief(f)
    # Should report missing Metadata, Target Keywords, ICP, Content Angle,
    # Human Anchors, Competitor Gap, Regulatory Flags = 7 required sections
    missing_count = sum(1 for f in failures if 'Missing required section' in f)
    assert missing_count == 7
