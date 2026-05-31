"""Regression tests for workflow/check-rules.py.

Each incident that has actually slipped through the pipeline becomes a
test fixture. The test fails if the rule that should have caught it
ever stops catching it.

Incident references map to entries in workflow/incident-log.md.
"""
import importlib.util
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_check_rules():
    """Import check-rules.py as a module despite its hyphenated filename."""
    path = REPO_ROOT / 'workflow' / 'check-rules.py'
    spec = importlib.util.spec_from_file_location('check_rules', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope='module')
def cr():
    return _load_check_rules()


# ---------------------------------------------------------------------
# Incident: 2026-05-26 em-dash leak. v3 humanization artifacts shipped
# 101 em-dashes across 7 files because no check enforced the rule.
# ---------------------------------------------------------------------

def test_em_dash_blocks(cr, tmp_path):
    f = tmp_path / 'doc.md'
    f.write_text('This sentence has an em-dash — like so.\n')
    blocking, warning = cr.check_file(f)
    names = [b[0] for b in blocking]
    assert 'em-dash' in names, f'expected em-dash BLOCK, got {blocking!r}'


def test_en_dash_blocks(cr, tmp_path):
    f = tmp_path / 'doc.md'
    f.write_text('A range like 2020–2024 trips the rule.\n')
    blocking, _ = cr.check_file(f)
    assert any(b[0] == 'en-dash' for b in blocking)


def test_clean_doc_passes(cr, tmp_path):
    f = tmp_path / 'doc.md'
    f.write_text('Plain text. No em-dash. Periods only.\n')
    blocking, _ = cr.check_file(f)
    assert blocking == []


def test_allow_pragma_exempts_em_dash_line(cr, tmp_path):
    """Documentation lines that reference banned chars can use the pragma."""
    f = tmp_path / 'doc.md'
    f.write_text(
        'No em-dashes (`—`) allowed normally. <!-- check-rules: allow -->\n'
        'But this OTHER line — with no pragma — still trips.\n'
    )
    blocking, _ = cr.check_file(f)
    # Line 1 exempted, line 2 catches 2 em-dashes
    assert len(blocking) == 2
    assert all(b[0] == 'em-dash' for b in blocking)
    assert all(b[1] == 2 for b in blocking)  # all on line 2


# ---------------------------------------------------------------------
# Incident: 2026-05-26 customer feedback "grammatical errors and mobile
# formatting issues" on a Stage-7-cleared v2 doc. Stage 7 had no grammar
# check. Section E was added; these tests pin the grammar heuristics.
# ---------------------------------------------------------------------

def test_comma_splice_warns(cr, tmp_path):
    """The 'applies, it is' pattern from the v2 draft must warn."""
    f = tmp_path / 'doc.md'
    f.write_text('The same caveat applies, it is a habit-builder.\n')
    _, warning = cr.check_file(f)
    assert any(w[0] == 'grammar-comma-splice' for w in warning)


def test_hyphen_as_emdash_warns_lowercase(cr, tmp_path):
    """The 'word - word' construction (lowercase flanking) must warn."""
    f = tmp_path / 'doc.md'
    f.write_text('I really enjoy reading - this is fine for me.\n')
    _, warning = cr.check_file(f)
    assert any(w[0] == 'grammar-hyphen-as-emdash' for w in warning)


def test_hyphen_as_emdash_warns_acronym_construction(cr, tmp_path):
    """Reviewed by Daniel Cho, CFA - investment strategist must warn.

    This specific case slipped past the first round of v2 review and
    triggered the customer comment about grammatical errors.
    """
    f = tmp_path / 'doc.md'
    f.write_text('Reviewed by Daniel Cho, CFA - investment strategist.\n')
    _, warning = cr.check_file(f)
    assert any(w[0] == 'grammar-hyphen-as-emdash' for w in warning)


def test_bare_comparative_warns(cr, tmp_path):
    """The 'bigger split than people realize' pattern must warn."""
    f = tmp_path / 'doc.md'
    f.write_text('This is the bigger split than people realize.\n')
    _, warning = cr.check_file(f)
    assert any(w[0] == 'grammar-bare-comparative' for w in warning)


def test_runon_warns(cr, tmp_path):
    """Sentence >=40 words with >=3 commas and no semicolon must warn."""
    long_sentence = (
        'This very long sentence has many parts and pieces, with multiple '
        'clauses stacked together, and additional thoughts piled on top of '
        'one another, plus a fourth section that adds yet more content, and '
        'a fifth piece, and a sixth piece, and even more besides, going on '
        'and on like this forever without ever finding a natural break.'
    )
    assert len(long_sentence.split()) >= 40
    f = tmp_path / 'doc.md'
    f.write_text(long_sentence + '\n')
    _, warning = cr.check_file(f)
    assert any(w[0] == 'grammar-runon' for w in warning)


# ---------------------------------------------------------------------
# Incident: 2026-05-14 "guaranteed return" usage in draft body even as
# a disclaimer-style negation. Brand voice rule bans the phrase outright.
# ---------------------------------------------------------------------

def test_guaranteed_return_blocks(cr, tmp_path):
    f = tmp_path / 'doc.md'
    f.write_text('No platform offers a guaranteed return on real estate.\n')
    blocking, _ = cr.check_file(f)
    assert any(b[0] == 'guaranteed-return' for b in blocking)


def test_guaranteed_returns_plural_blocks(cr, tmp_path):
    f = tmp_path / 'doc.md'
    f.write_text('You should not expect guaranteed returns from this asset class.\n')
    blocking, _ = cr.check_file(f)
    assert any(b[0] == 'guaranteed-return' for b in blocking)


def test_guaranteed_yield_blocks(cr, tmp_path):
    f = tmp_path / 'doc.md'
    f.write_text('There is no guaranteed yield on fractional shares.\n')
    blocking, _ = cr.check_file(f)
    assert any(b[0] == 'guaranteed-return' for b in blocking)


# ---------------------------------------------------------------------
# Incident: 2026-05-26 BSD-grep regression. Hook used grep -E '\+' which
# BSD grep rejects. Python implementation must work regardless of host.
# ---------------------------------------------------------------------

def test_runs_without_grep_errors_on_unicode_content(cr, tmp_path):
    """Earlier bash hook crashed on unicode punctuation under BSD grep.
    Python implementation should not have analogous failures.
    """
    f = tmp_path / 'doc.md'
    f.write_text('Mixed content: emoji 🚀, smart quotes "like this", em-dash —.\n')
    blocking, warning = cr.check_file(f)
    # Should detect the em-dash, should not raise
    assert any(b[0] == 'em-dash' for b in blocking)


# ---------------------------------------------------------------------
# Brand voice: PSFnetwork casing variants. Tier 2 BLOCKING.
# Per the 2026 client brief, the brand is written PSFnetwork (capital PSF).
# ---------------------------------------------------------------------

@pytest.mark.parametrize('variant', [
    'psfnetwork', 'PSF Network', 'PSFNETWORK', 'Psfnetwork',
])
def test_psfnetwork_casing_blocks(cr, tmp_path, variant):
    f = tmp_path / 'doc.md'
    f.write_text(f'A reference to {variant} in body prose.\n')
    blocking, _ = cr.check_file(f)
    assert any(b[0] == 'psfnetwork-casing' for b in blocking)


def test_psfnetwork_capitalized_passes(cr, tmp_path):
    f = tmp_path / 'doc.md'
    f.write_text('A reference to PSFnetwork in body prose.\n')
    blocking, _ = cr.check_file(f)
    casing_hits = [b for b in blocking if b[0] == 'psfnetwork-casing']
    assert casing_hits == []


def test_psfnetwork_domain_not_flagged(cr, tmp_path):
    f = tmp_path / 'doc.md'
    f.write_text('See https://psfnetwork.com/blog for details.\n')
    blocking, _ = cr.check_file(f)
    casing_hits = [b for b in blocking if b[0] == 'psfnetwork-casing']
    assert casing_hits == []
