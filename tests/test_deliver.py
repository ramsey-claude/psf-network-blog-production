"""Regression tests for workflow/deliver.py QA gate.

Incident: 2026-05-26 v2 humanized draft was uploaded to Drive without
Stage 7 QA. Stage 9 should never bypass Stage 7. deliver.py is the
enforcement point.
"""
import importlib.util
import sys
from pathlib import Path
from unittest import mock

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_deliver():
    path = REPO_ROOT / 'workflow' / 'deliver.py'
    spec = importlib.util.spec_from_file_location('deliver', path)
    mod = importlib.util.module_from_spec(spec)
    # deliver.py imports happen at module load; tolerate missing google libs
    # by mocking the get_service path if needed. For this unit-level test
    # we only exercise the QA gate, which is pure stdlib.
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope='module')
def deliver():
    return _load_deliver()


def test_check_qa_refuses_missing_recommendation(deliver, tmp_path):
    """qa-report without a Recommendation section fails the gate."""
    qa = tmp_path / 'qa.md'
    qa.write_text('# QA Report\n\nSome content but no verdict.\n')
    with pytest.raises(SystemExit) as exc:
        deliver.check_qa(qa)
    assert 'verdict' in str(exc.value).lower() or 'recommendation' in str(exc.value).lower()


def test_check_qa_refuses_fail_verdict(deliver, tmp_path):
    """qa-report with FAIL verdict refuses delivery."""
    qa = tmp_path / 'qa.md'
    qa.write_text(
        '# QA Report\n\n'
        '## Recommendation\n\n'
        'FAIL. Route to Stage 4.\n'
    )
    with pytest.raises(SystemExit) as exc:
        deliver.check_qa(qa)
    assert 'PUBLISH' in str(exc.value) or 'refused' in str(exc.value).lower()


def test_check_qa_accepts_publish_in_header_format(deliver, tmp_path):
    """## Recommendation\\n\\nPUBLISH ... passes."""
    qa = tmp_path / 'qa.md'
    qa.write_text(
        '# QA Report\n\n'
        '## Summary\n\n0 FAIL, 27 PASS.\n\n'
        '## Recommendation\n\n'
        'PUBLISH (re-deliver). Replace prior Drive doc.\n'
    )
    verdict = deliver.check_qa(qa)
    assert 'PUBLISH' in verdict


def test_check_qa_accepts_publish_in_inline_format(deliver, tmp_path):
    """RECOMMENDATION: PUBLISH inline label format also passes.

    This is the v1 qa-report format. deliver.py supports both formats
    so old reports do not need to be migrated.
    """
    qa = tmp_path / 'qa.md'
    qa.write_text(
        '# QA Report\n\n'
        'Stage 7. Loop 0.\n'
        'QA_RESULT: PASS\n'
        'RECOMMENDATION: PUBLISH\n'
    )
    verdict = deliver.check_qa(qa)
    assert 'PUBLISH' in verdict


def test_check_qa_refuses_fail_in_summary(deliver, tmp_path):
    """Summary listing any FAIL count blocks even with PUBLISH verdict."""
    qa = tmp_path / 'qa.md'
    qa.write_text(
        '# QA Report\n\n'
        '## Summary\n\n2 FAIL items found.\n\n'
        '## Recommendation\n\nPUBLISH\n'
    )
    with pytest.raises(SystemExit) as exc:
        deliver.check_qa(qa)
    assert 'FAIL' in str(exc.value)


def test_find_artifacts_v1_uses_unversioned_names(deliver, tmp_path, monkeypatch):
    """For --version v1, the wrapper looks for draft.md + qa-report.md."""
    blog_dir = tmp_path / 'blog' / 'test-slug'
    blog_dir.mkdir(parents=True)
    (blog_dir / 'draft.md').write_text('content')
    (blog_dir / 'qa-report.md').write_text('content')

    monkeypatch.setattr(deliver, 'REPO', tmp_path)
    draft, qa = deliver.find_artifacts('test-slug', 'v1')
    assert draft.name == 'draft.md'
    assert qa.name == 'qa-report.md'


def test_find_artifacts_v2_uses_versioned_names(deliver, tmp_path, monkeypatch):
    """For non-v1 versions, names include the version suffix."""
    blog_dir = tmp_path / 'blog' / 'test-slug'
    blog_dir.mkdir(parents=True)
    (blog_dir / 'draft-v2-humanized.md').write_text('content')
    (blog_dir / 'qa-report-v2-humanized.md').write_text('content')

    monkeypatch.setattr(deliver, 'REPO', tmp_path)
    draft, qa = deliver.find_artifacts('test-slug', 'v2-humanized')
    assert draft.name == 'draft-v2-humanized.md'
    assert qa.name == 'qa-report-v2-humanized.md'


def test_find_artifacts_missing_file_exits(deliver, tmp_path, monkeypatch):
    """Missing draft or qa-report blocks delivery."""
    blog_dir = tmp_path / 'blog' / 'test-slug'
    blog_dir.mkdir(parents=True)
    (blog_dir / 'draft.md').write_text('content')
    # qa-report.md intentionally missing

    monkeypatch.setattr(deliver, 'REPO', tmp_path)
    with pytest.raises(SystemExit) as exc:
        deliver.find_artifacts('test-slug', 'v1')
    assert 'Missing' in str(exc.value) or 'qa-report' in str(exc.value)
