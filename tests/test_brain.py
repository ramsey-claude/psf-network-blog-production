"""Tests for workflow/brain.py, the operation's index over its own knowledge.

Two kinds of test here. Most pin the extraction contract: given a source file
shaped the way the incident log, the roadmap, and an article folder are shaped,
the brain has to read the same facts a person would. The last one is the
invariant that matters in CI: the registries committed to the repo match what
the current sources produce, so nobody can push a source change that quietly
leaves the brain describing a repo that no longer exists.
"""
import importlib.util
import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope='module')
def brain():
    spec = importlib.util.spec_from_file_location('brain', REPO_ROOT / 'workflow' / 'brain.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


LOG_SAMPLE = """# Pipeline Incident Log

### 2026-01-02: Something broke in delivery

- **Stage:** 9 (Client delivery)
- **Symptom:** the upload landed as the wrong file type
- **Root cause:** the converter did not run
  and nobody noticed until the client asked
- **Rule:** Active Rules > Tooling > Uploads

---

## Active rules (apply on every run)

### Tooling
- **Drive uploads:** use the REST API. Never the MCP.
- **Charts:** components are `.tsx`, never `.jsx`.

### Process
- **Loop budget:** combined maximum 3.
  On exceed, halt.

---

## Incident history

### 2025-12-24: An older thing

- **Stage:** 7 (Pre-publish QA)
- **Rule:** no new rule, one-off

## Open issues / known limitations

- **Loop enforcement is procedural:** Claude reads the count and stops.
"""


def test_parses_active_rules_with_categories(brain):
    parsed = brain.parse_incident_log(LOG_SAMPLE)
    ids = [rule['id'] for rule in parsed['rules']]
    assert ids == ['R-tooling-drive-uploads', 'R-tooling-charts', 'R-process-loop-budget']


def test_rule_statement_absorbs_continuation_lines(brain):
    parsed = brain.parse_incident_log(LOG_SAMPLE)
    loop = [r for r in parsed['rules'] if r['id'] == 'R-process-loop-budget'][0]
    assert loop['statement'] == 'combined maximum 3. On exceed, halt.'
    assert loop['category'] == 'Process'


def test_rule_ids_are_stable_against_reordering(brain):
    reordered = LOG_SAMPLE.replace(
        '- **Drive uploads:** use the REST API. Never the MCP.\n- **Charts:** components are `.tsx`, never `.jsx`.',
        '- **Charts:** components are `.tsx`, never `.jsx`.\n- **Drive uploads:** use the REST API. Never the MCP.')
    before = {r['id'] for r in brain.parse_incident_log(LOG_SAMPLE)['rules']}
    after = {r['id'] for r in brain.parse_incident_log(reordered)['rules']}
    assert before == after


def test_parses_incidents_and_open_issues(brain):
    parsed = brain.parse_incident_log(LOG_SAMPLE)
    dates = [i['date'] for i in parsed['incidents']]
    assert dates == ['2026-01-02', '2025-12-24']
    first = parsed['incidents'][0]
    assert first['headline'] == 'Something broke in delivery'
    assert first['fields']['stage'] == '9 (Client delivery)'
    assert first['fields']['root cause'].endswith('until the client asked')
    assert len(parsed['open_issues']) == 1
    assert parsed['open_issues'][0]['label'] == 'Loop enforcement is procedural'


def test_duplicate_labels_are_reported_not_merged(brain):
    duplicated = LOG_SAMPLE.replace(
        '- **Charts:** components are `.tsx`, never `.jsx`.',
        '- **Drive uploads:** a second rule with the same label.')
    rules = brain.parse_incident_log(duplicated)['rules']
    assert len(rules) == 3
    assert [r for r in rules if r.get('duplicate_of')]


def test_slugify_is_bounded_and_stable(brain):
    assert brain.slugify('Permission prompts, self-recover, do not pause').startswith('permission-prompts')
    assert len(brain.slugify('a' * 200)) <= 44
    assert brain.slugify('Drive uploads') == brain.slugify('drive   uploads!')


def test_sanitize_carries_the_pragma_onto_a_quoted_ban(brain):
    line = 'six uses of the word guaranteed shipped'
    assert brain.sanitize(line).endswith(brain.ALLOW_PRAGMA)
    assert brain.sanitize('a clean line') == 'a clean line'
    already = 'quoted ban <!-- check-rules: allow -->'
    assert brain.sanitize(already) == already


def test_generated_output_passes_the_content_linter(brain):
    """Whatever the brain emits has to survive the repo's own rules."""
    check_rules = brain._cr
    for relpath, renderer in brain.GENERATED.items():
        text = renderer(brain.context())
        for name, pattern, _ in check_rules.BLOCKING:
            for match in pattern.finditer(text):
                line = text[:match.start()].count('\n')
                assert brain.ALLOW_PRAGMA in text.split('\n')[line], \
                    f'{relpath} emits an unpragma\'d {name}: {match.group(0)!r}'


def test_article_status_reads_the_evidence_on_disk(brain, tmp_path):
    folder = tmp_path / 'some-slug'
    folder.mkdir()
    assert brain.article_status({}, folder) == 'empty'
    (folder / 'draft.md').write_text('# hi')
    assert brain.article_status({}, folder) == 'draft-only'
    (folder / 'qa-report.md').write_text('PUBLISH')
    assert brain.article_status({}, folder) == 'qa-passed'
    (folder / 'delivery-manifest.md').write_text('id')
    assert brain.article_status({}, folder) == 'delivered'
    assert brain.article_status({'stage': 'published'}, folder) == 'published'


def test_topic_tokens_reconcile_number_forms(brain):
    assert '10000' in brain.topic_tokens('How to invest $10,000 in real estate')
    assert '10000' in brain.topic_tokens('how-to-invest-10k-in-real-estate')
    assert '401' in brain.topic_tokens('fractional-real-estate-401k-rollover')
    assert '401' in brain.topic_tokens('Fractional real estate in a 401(k) rollover')


def test_best_match_prefers_the_tighter_candidate(brain):
    wanted = {'reit'}
    candidates = {'reit-dividend-taxation': {'reit', 'dividend', 'taxation'},
                  'reits-vs-fractional': {'reit'}}
    key, recall = brain.best_match(wanted, candidates)
    assert key == 'reits-vs-fractional'
    assert recall == 1.0


def test_search_finds_the_section_that_holds_the_answer(brain):
    results = brain.search('answer capsule words', {'ops', 'brain'}, limit=5)
    assert results
    assert any('capsule' in hit['snippet'].lower() or 'capsule' in hit['heading'].lower()
               for hit in results)
    assert all(hit['line'] >= 1 for hit in results)


def test_check_flags_a_stale_registry(brain, monkeypatch, tmp_path):
    stale = REPO_ROOT / 'brain' / 'rules.md'
    original = stale.read_text()
    try:
        stale.write_text(original + '\nan edit nothing generated\n')
        findings = brain.check()
        assert any(level == 'FAIL' and 'rules.md' in message for level, message in findings)
    finally:
        stale.write_text(original)


def test_check_flags_an_unresolvable_rule_citation(brain):
    page = REPO_ROOT / 'brain' / 'canon' / 'brand.md'
    original = page.read_text()
    try:
        page.write_text(original + '\nSee `R-nope-does-not-exist` for details.\n')
        findings = brain.check()
        assert any('R-nope-does-not-exist' in message for _, message in findings)
    finally:
        page.write_text(original)


def test_repo_brain_is_current_and_sound(brain):
    """The invariant CI depends on: committed registries match live sources."""
    fails = [message for level, message in brain.check() if level == 'FAIL']
    assert fails == [], 'run: python3 workflow/brain.py build'
