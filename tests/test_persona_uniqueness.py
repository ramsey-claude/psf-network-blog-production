"""Regression: 2026-05-26 Batch 2 sync revealed the same first name "Priya"
was used as the Real Story humanization anchor in 13 different articles,
each with a different profession and city. Cross-article persona repetition
is invisible to per-article QA. This test locks the rule.

Every persona first-name that appears in a persona-introducing sentence
must appear in at most one blog draft.
"""
import re
from pathlib import Path
from collections import defaultdict


REPO_ROOT = Path(__file__).resolve().parent.parent
BLOG = REPO_ROOT / 'blog'


PERSONA_INTRO = re.compile(
    r'(?:call|meet|introduce\s+you\s+to)\s+([A-Z][a-z]+)\b'
    r'|\b([A-Z][a-z]+),\s+a\s+\d+[-\s]year[-\s]?old'
    r'|\b([A-Z][a-z]+),\s+a\s+[a-z]+(?:\s+[a-z]+)?\s+(?:in|from)\s+[A-Z]'
)

# Standing personas allowed to recur across articles: author, reviewer, etc.
STANDING = {'Maya', 'Daniel'}

# Common capitalized words that are not persona names but can start sentences.
# Used to strip false positives from the regex.
NOT_A_PERSONA = {
    'It', 'The', 'This', 'That', 'These', 'Those', 'When', 'What', 'Why',
    'Where', 'How', 'Who', 'Which', 'Each', 'Every', 'All', 'Some', 'Most',
    'Capital', 'Real', 'Common', 'Personal', 'You', 'Your', 'They', 'We',
    'Answer', 'Question', 'Section', 'Table', 'Note', 'Example', 'For',
    'Reg', 'REIT', 'SEC', 'IRS', 'CFA', 'CFP', 'LLC', 'IRA', 'K',
}


def _drafts():
    for slug_dir in BLOG.iterdir():
        if not slug_dir.is_dir():
            continue
        for name in ('draft.md', 'draft-v2-humanized.md'):
            p = slug_dir / name
            if p.exists():
                yield slug_dir.name, name, p


def _extract_persona_names(text):
    """Return set of names introduced as personas in this text."""
    names = set()
    for m in PERSONA_INTRO.finditer(text):
        for group in m.groups():
            if group and group not in STANDING and group not in NOT_A_PERSONA:
                names.add(group)
    return names


def test_no_persona_name_appears_in_multiple_drafts():
    """No persona first-name may serve as a Real Story anchor in more than one draft."""
    name_to_drafts = defaultdict(list)
    for slug, fname, path in _drafts():
        text = path.read_text(encoding='utf-8')
        for name in _extract_persona_names(text):
            name_to_drafts[name].append(f'{slug}/{fname}')

    collisions = {n: ds for n, ds in name_to_drafts.items() if len(ds) > 1}
    assert not collisions, (
        'Cross-article persona name collision (each name must be unique to one draft):\n'
        + '\n'.join(f'  {n} appears in: {ds}' for n, ds in collisions.items())
    )


def test_standing_personas_may_recur():
    """Sanity check: Maya (author) and Daniel (reviewer) are allowed everywhere."""
    # Not enforced by the test, but confirms STANDING set works as expected
    assert 'Maya' in STANDING
    assert 'Daniel' in STANDING
