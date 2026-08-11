"""Regression tests for workflow/qa_battery.py.

Each test pins a failure mode that actually reached the final QA step before
the battery existed (incident-log 2026-08-11).
"""
import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope='module')
def qb():
    spec = importlib.util.spec_from_file_location(
        'qa_battery', REPO_ROOT / 'workflow' / 'qa_battery.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def make_article(tmp_path, body, notes=None):
    folder = tmp_path / 'test-article'
    folder.mkdir()
    notes = notes if notes is not None else (
        '**PRODUCTION NOTES | NOT PART OF THE PUBLISHED BODY**\n\n'
        '- Meta title (SEO): A Title Sized to Pass the Fifty-Five To Sixty Rule\n\n'
        '- Meta description: '
        + ('x' * 155) + '\n\n'
        '- Published: 2026-06-19\n\n')
    (folder / 'draft.md').write_text(notes + body)
    return folder


CLEAN_BODY = '# H1\n\nOpening paragraph.\n\n## Is this a question H2?\n\nBody text.\n'


def fails_of(qb, folder):
    _, _, fails, _ = qb.check_article(folder)
    return fails


# Incident: six drafts' SEO fields silently parsed to nothing because the
# June batch bolded its labels ("- **Meta description:** ..."). The battery
# and the paste kit share parse_notes, so this pins both.
def test_bold_labels_parse(qb, tmp_path):
    notes = ('**PRODUCTION NOTES | NOT PART OF THE PUBLISHED BODY**\n\n'
             '- **Meta title (SEO):** A Title Sized to Pass the Fifty-Five Rule\n\n'
             '- **Meta description:** ' + 'x' * 155 + '\n\n')
    folder = make_article(tmp_path, CLEAN_BODY, notes=notes)
    fails = fails_of(qb, folder)
    assert not any(f.startswith('F4') or f.startswith('F7 title missing')
                   for f in fails), fails


# Incident: bare "guaranteed" shipped in six Batch 2 articles.
def test_bare_guaranteed_fails(qb, tmp_path):
    folder = make_article(tmp_path, CLEAN_BODY + '\nReturns are not guaranteed.\n')
    assert any(f.startswith('F2') for f in fails_of(qb, folder))


def test_pragma_exempts_guaranteed(qb, tmp_path):
    folder = make_article(
        tmp_path,
        CLEAN_BODY + '\nRule doc: no "guaranteed". <!-- check-rules: allow -->\n')
    assert not any(f.startswith('F2') for f in fails_of(qb, folder))


# Incident: ira article shipped with no meta description at all.
def test_missing_meta_fails(qb, tmp_path):
    notes = ('**PRODUCTION NOTES | NOT PART OF THE PUBLISHED BODY**\n\n'
             '- Meta title (SEO): A Title Sized to Pass the Fifty-Five Rule\n\n')
    folder = make_article(tmp_path, CLEAN_BODY, notes=notes)
    assert any(f.startswith('F4') for f in fails_of(qb, folder))


# Incident: eight Batch 2 metas were outside 150-160 at go-live.
def test_meta_length_fails(qb, tmp_path):
    notes = ('**PRODUCTION NOTES | NOT PART OF THE PUBLISHED BODY**\n\n'
             '- Meta title (SEO): A Title Sized to Pass the Fifty-Five Rule\n\n'
             '- Meta description: too short\n\n')
    folder = make_article(tmp_path, CLEAN_BODY, notes=notes)
    assert any(f.startswith('F5') for f in fails_of(qb, folder))


# Incident: "Answer capsule:" scaffolding shipped to readers in Batch 1.
def test_answer_capsule_fails(qb, tmp_path):
    folder = make_article(
        tmp_path, CLEAN_BODY + '\n**Answer capsule:** A definition.\n')
    assert any(f.startswith('F3') for f in fails_of(qb, folder))


def test_em_dash_fails(qb, tmp_path):
    folder = make_article(tmp_path, CLEAN_BODY + '\nA thought — interrupted.\n')
    assert any(f.startswith('F1') for f in fails_of(qb, folder))


# The ratchet: baselined findings are suppressed by (slug, normalized text),
# so line-number drift does not resurrect them, and other slugs' identical
# findings still fail.
def test_baseline_normalization_strips_line_numbers(qb):
    assert qb.normalize('F2 "guaranteed" at line 42') == 'F2 "guaranteed"'
    assert qb.normalize('F3 Answer capsule label') == 'F3 Answer capsule label'


def test_repo_baseline_entries_are_batch1_only(qb):
    # New content must never be baselined. Every current entry is a Batch 1
    # slug; this test forces a conscious edit here if anyone tries to add
    # baseline entries for later batches.
    batch1 = {
        '90-percent-millionaires-real-estate',
        'best-fractional-real-estate-platforms',
        'fractional-real-estate-investing',
        'how-fractional-real-estate-is-taxed',
        'how-to-build-passive-income-with-real-estate',
        'how-to-invest-10k-in-real-estate',
        'how-to-invest-in-real-estate-with-100',
        'real-estate-crowdfunding-vs-fractional',
        'reg-a-vs-reg-d-for-fractional-investors',
        'reits-vs-fractional-real-estate',
        'square-foot-real-estate-ownership-explained',
        'what-is-proptech',
    }
    for slug, _ in qb.load_baseline():
        assert slug in batch1, f'baseline entry for non-Batch-1 slug: {slug}'


def test_full_repo_battery_is_green(qb):
    # The standing invariant: every canonical draft passes with the current
    # baseline. If this fails, either new content shipped with a violation
    # or a baseline entry was removed without fixing the underlying draft.
    folders = sorted(p for p in (REPO_ROOT / 'blog').iterdir() if p.is_dir())
    baseline = qb.load_baseline()
    problems = []
    for folder in folders:
        slug, _, fails, _ = qb.check_article(folder)
        problems += [f'{slug}: {f}' for f in fails
                     if (slug, qb.normalize(f)) not in baseline]
    assert not problems, problems
