"""Tests for workflow/mind.py, the brain clone.

The clone holds someone's own thinking, so the properties that matter are not
about formatting. They are: nothing enters as confirmed that the owner did not
confirm, nothing gets silently overwritten, and the growth measures are honest.
Every test here pins one of those.

MIND_HOME is redirected to a temp directory in every test, so a run can never
read or write the real store.
"""
import importlib.util
import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope='module')
def mind():
    spec = importlib.util.spec_from_file_location('mind', REPO_ROOT / 'workflow' / 'mind.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def store(mind, tmp_path, monkeypatch):
    monkeypatch.setenv('MIND_HOME', str(tmp_path / 'clone'))
    return mind.home()


# --- the question bank ------------------------------------------------------

def test_bank_parses_and_ids_are_unique(mind):
    bank = mind.parse_bank()
    assert len(bank) >= 100
    ids = [q['id'] for q in bank]
    assert len(ids) == len(set(ids))
    assert all(q['priority'] in ('P1', 'P2', 'P3') for q in bank)
    assert all(q['domain'] and q['text'] for q in bank)


def test_bank_covers_every_seeded_domain(mind):
    """A seed lands in a domain the interview can also ask about."""
    domains = {q['domain'] for q in mind.parse_bank()}
    seeded = {alan for _, _, alan, _, _, _ in mind.SEEDS}
    assert seeded - domains == {'acik'}, 'seed domain with no questions behind it'


# --- the model --------------------------------------------------------------

def test_format_example_in_a_comment_is_not_an_entry(mind):
    text = mind.ENTRY_FORMAT_NOTE + '\n\n### B-001. Gerçek girdi\n\n- **Durum:** onaylı\n'
    entries = mind.parse_entries(text)
    assert [e['id'] for e in entries] == ['B-001']
    assert entries[0]['title'] == 'Gerçek girdi'


def test_entry_fields_and_body_are_read(mind):
    text = ('### H-004. Bir kural\n\n- **Tür:** Kural\n- **Güven:** yüksek\n'
            '- **Durum:** onaylı\n- **Kaynak:** oturum 2026-01-01\n\nAçıklama satırı.\n')
    entry = mind.parse_entries(text)[0]
    assert entry['fields']['güven'] == 'yüksek'
    assert entry['fields']['kaynak'] == 'oturum 2026-01-01'
    assert entry['body'] == ['Açıklama satırı.']


def test_ids_increment_per_kind(mind, store):
    mind.init(store)
    first = mind.add_entry('kural', 'ilk', {'Durum': 'onaylı', 'Güven': 'orta'}, store=store)
    second = mind.add_entry('kural', 'ikinci', {'Durum': 'onaylı', 'Güven': 'orta'}, store=store)
    assert int(second[2:]) == int(first[2:]) + 1
    assert first.startswith('H-')


def test_init_seeds_unconfirmed_and_does_not_duplicate(mind, store):
    mind.init(store)
    entries = mind.all_entries(store)
    assert len(entries) == len(mind.SEEDS)
    assert {e['fields']['durum'] for e in entries} == {'onaysız'}, \
        'a seed is a hypothesis, never the owner\'s confirmed view'
    assert all(e['fields'].get('kaynak') for e in entries)
    mind.init(store)
    assert len(mind.all_entries(store)) == len(mind.SEEDS)


def test_confirm_rewrites_status_in_place_and_keeps_the_entry(mind, store):
    mind.init(store)
    target = mind.all_entries(store)[0]['id']
    mind.confirm(target, 'reddedildi', note='tam tersi', store=store)
    entry = [e for e in mind.all_entries(store) if e['id'] == target][0]
    assert entry['fields']['durum'] == 'reddedildi'
    assert 'tam tersi' in ' '.join(entry['fields'].values())
    assert len(mind.all_entries(store)) == len(mind.SEEDS), 'rejecting must not delete'


# --- capture and interview --------------------------------------------------

def test_session_answers_are_parsed_and_blanks_ignored(mind):
    text = ('## S-001 [P1] Soru bir?\n\n**Cevap:**\n\nCevap metni\ndevamı\n\n---\n'
            '## S-002 [P1] Soru iki?\n\n**Cevap:**\n\n---\n')
    blocks = mind.parse_session(text)
    assert blocks[0]['answer'] == 'Cevap metni\ndevamı'
    assert blocks[1]['answer'] == ''


def test_answered_questions_leave_the_pool(mind, store):
    mind.init(store)
    picked = mind.pick_questions(3, store=store)
    answered = picked[0]['id']
    path = mind.session_path(store=store)
    mind.write(path, '## %s [P1] soru?\n\n**Cevap:**\n\nbir cevap\n\n---\n' % answered)
    assert answered in mind.answered_ids(store)
    assert answered not in [q['id'] for q in mind.pick_questions(10, store=store)]


def test_interview_prefers_p1_then_thin_domains(mind, store):
    mind.init(store)
    picked = mind.pick_questions(10, store=store)
    assert all(q['priority'] == 'P1' for q in picked)
    covered = mind.domain_coverage(store)
    assert all(covered.get(q['domain'], 0) == 0 for q in picked), \
        'a session should spend its minutes where the clone knows least'


def test_domain_filter(mind, store):
    mind.init(store)
    picked = mind.pick_questions(5, domain='karar-verme', store=store)
    assert picked and all(q['domain'] == 'karar-verme' for q in picked)


def test_capture_writes_and_distill_tracks_processed(mind, store):
    mind.init(store)
    mind.capture('aklıma gelen şey', store=store, tag='not')
    pending = mind.raw_items(store)
    assert len(pending) == 1
    state = mind.load_state(store)
    state['processed'] = [pending[0]['id']]
    mind.save_state(state, store)
    assert mind.raw_items(store) == []
    assert len(mind.raw_items(store, include_processed=True)) == 1


# --- recall -----------------------------------------------------------------

def test_ask_finds_entries_and_flags_unconfirmed(mind, store):
    mind.init(store)
    result = mind.ask('borç kalite', store)
    assert result['entries']
    assert any(e['fields']['durum'] == 'onaysız' for e in result['entries'])


def test_ask_on_an_unknown_subject_returns_questions_instead(mind, store):
    mind.init(store)
    result = mind.ask('köpek eğitimi', store)
    assert not result['entries']


def test_confirmed_entries_outrank_unconfirmed(mind, store):
    mind.init(store)
    mind.add_entry('inanc', 'Kalite ölçülmezse dalgalanır ve borç birikir',
                   {'Durum': 'onaylı', 'Güven': 'yüksek', 'Kaynak': 'test', 'Alan': 'kalite'},
                   store=store)
    top = mind.match_entries('kalite borç', store, limit=1)[0]
    assert top['fields']['durum'] == 'onaylı'


# --- advancing --------------------------------------------------------------

def test_rehearse_then_grade_moves_fidelity(mind, store):
    mind.init(store)
    delta_id, path = mind.rehearse('bu fiyatı verir miydim', store)
    assert path.exists()
    assert 'bekliyor' in path.read_text()
    mind.grade(delta_id, 'right', store=store)
    score = mind.fidelity(store)
    assert score['count'] == 1 and score['overall'] == 100
    assert 'tutturdu' in path.read_text()


def test_fidelity_scores_partial_as_half(mind, store):
    mind.init(store)
    for verdict in ('right', 'wrong', 'partial'):
        delta_id, _ = mind.rehearse('soru', store)
        mind.grade(delta_id, verdict, store=store)
    assert mind.fidelity(store)['overall'] == 50


# --- health -----------------------------------------------------------------

def test_check_is_clean_on_a_fresh_clone(mind, store):
    mind.init(store)
    assert [f for f in mind.check(store) if f[0] == 'FAIL'] == []


def test_check_catches_a_broken_entry(mind, store):
    mind.init(store)
    path = store / 'model' / 'beliefs.md'
    path.write_text(path.read_text() + '\n### B-001. Aynı id ikinci kez\n\n- **Durum:** belirsiz\n- **Güven:** çok\n')
    messages = ' '.join(m for _, m in mind.check(store))
    assert 'iki kez' in messages
    assert 'geçersiz durum' in messages


def test_check_reports_a_missing_store_without_failing(mind, tmp_path, monkeypatch):
    monkeypatch.setenv('MIND_HOME', str(tmp_path / 'yok'))
    findings = mind.check()
    assert [f for f in findings if f[0] == 'FAIL'] == []
    assert any(level == 'INFO' for level, _ in findings)


def test_stale_entries_are_flagged_for_refresh(mind, store):
    mind.init(store)
    entry = {'fields': {'tarih': '2020-01-01', 'durum': 'onaylı'}}
    assert mind.is_stale(entry)
    entry['fields']['durum'] = 'onaysız'
    assert not mind.is_stale(entry), 'an unconfirmed entry is already on the review list'


def test_export_takes_the_clone_and_the_machinery(mind, store, tmp_path):
    mind.init(store)
    target = tmp_path / 'disari'

    class Args:
        to = str(target)

    mind.cmd_export(Args())
    assert (target / 'private' / 'model' / 'beliefs.md').exists()
    assert (target / 'workflow' / 'mind.py').exists()
    assert (target / 'mind' / 'questions' / 'bank.md').exists()


def test_the_store_never_lands_in_git(mind):
    ignored = (REPO_ROOT / '.gitignore').read_text()
    assert 'mind/private/' in ignored, 'a public repo must not carry a personal clone'
