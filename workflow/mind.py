#!/usr/bin/env python3
"""
Mind: a clone of the operator's own thinking, built to keep growing.

Not a note folder. A note folder stores what you wrote down; this stores what
you know, in a shape something else can reason with, and it measures how well
it predicts you.

Four moving parts:

  1. Elicitation. Knowledge that stays in one head is not transferable, and the
     bottleneck is never storage, it is getting it out. `interview` asks the
     highest-yield unanswered questions from a bank, weighted toward the areas
     the clone knows least about.

  2. The model. Raw answers are distilled into typed entries: beliefs,
     heuristics (if X then I do Y because Z), preferences, decisions, open
     questions. Every entry carries where it came from, how sure you are, and
     whether you have confirmed it. Nothing enters as fact because a machine
     inferred it.

  3. Recall. `ask` returns what the clone already holds on a subject, including
     the heuristics that bear on it, contradictions between entries, and the
     honest gap when it holds nothing.

  4. Advance. `rehearse` makes the clone answer as you before you do, `grade`
     records whether it got you right, and the correction becomes new material.
     `fidelity` is the number that says whether the clone is actually becoming
     you or just accumulating text.

Privacy. This repository is public. The clone is not: everything personal lives
in a store outside version control, `mind/private/` by default, overridable
with MIND_HOME. This script, the question bank, and the protocol are the only
parts that live in git. `export` moves the store somewhere private and takes
the machinery with it.

Exit codes:
  0  ok
  1  findings (failed integrity check, empty result)
  2  invocation error

Usage:
  python3 workflow/mind.py init
  python3 workflow/mind.py interview --n 8
  python3 workflow/mind.py capture "aklıma gelen şey"
  python3 workflow/mind.py distill
  python3 workflow/mind.py ask "fiyatlandırma konusunda ne düşünüyorum"
  python3 workflow/mind.py rehearse --question "..."
  python3 workflow/mind.py grade X-001 --verdict partial
  python3 workflow/mind.py gaps
  python3 workflow/mind.py stats
"""
import argparse
import json
import math
import os
import re
import shutil
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSETS = REPO_ROOT / 'mind'
BANK_PATH = ASSETS / 'questions' / 'bank.md'
PROTOCOL = ASSETS / 'AGENT.md'

# Outside the repo by default. The clone belongs to a person, not to a project,
# and this repository happens to be public.
DEFAULT_HOME = Path.home() / '.mind'


def home():
    """Where the clone lives. Outside this repo by default and by design."""
    return Path(os.environ.get('MIND_HOME') or DEFAULT_HOME).expanduser()


def today():
    return date.today().isoformat()


# Entry kinds. The prefix is the id, the file is where entries of that kind
# live, the label is what the operator sees.
KINDS = {
    'inanc': ('B', 'model/beliefs.md', 'İnanç'),
    'kural': ('H', 'model/heuristics.md', 'Kural'),
    'tercih': ('P', 'model/preferences.md', 'Tercih'),
    'karar': ('D', 'model/decisions.md', 'Karar'),
    'soru': ('O', 'model/open-questions.md', 'Açık soru'),
}
KIND_BY_PREFIX = {prefix: kind for kind, (prefix, _, _) in KINDS.items()}
STATUSES = ('onaysız', 'onaylı', 'revize', 'reddedildi')
CONFIDENCE = ('yüksek', 'orta', 'düşük')
STALE_DAYS = 180

ENTRY_HEAD = re.compile(r'^###\s+([A-Z]-\d{3})\.\s*(.+)$')
FIELD = re.compile(r'^-\s+\*\*(.+?):\*\*\s*(.*)$')
BANK_ITEM = re.compile(r'^-\s+(S-\d{3})\s+\[(P[123])\]\s+(.+)$')
BANK_DOMAIN = re.compile(r'^##\s+(.+?)\s*$')


def read(path):
    try:
        return Path(path).read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        return ''


def write(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def slugify(text, max_len=40):
    table = str.maketrans('çğıöşüÇĞİÖŞÜ', 'cgiosucgiosu')
    text = text.translate(table).lower()
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text[:max_len].strip('-') or 'not'


# ---------------------------------------------------------------------------
# recall primitives: small on purpose, so this file works anywhere it is copied
# ---------------------------------------------------------------------------

# Unicode-aware: an ASCII class shreds "köpek" into "k" and "pek", and those
# fragments then match everything.
TOKEN = re.compile(r"[^\W_]+(?:['’_-][^\W_]+)*", re.UNICODE)
COMBINING_DOT = '\u0307'
HEADING_RE = re.compile(r'^(#{1,6})\s+(.+)$')
CHUNK_MAX_LINES = 120


def fold(text):
    """Lowercase for matching. Turkish İ lowercases to i plus a combining dot."""
    return text.lower().replace(COMBINING_DOT, '')


def tokens_of(text):
    return TOKEN.findall(fold(text))


def chunks_of(path):
    """Heading-aware chunks, so a hit points at a section and not a whole file."""
    lines = read(path).split('\n')
    chunks, buf, heading, start = [], [], '', 1

    def flush():
        if any(line.strip() for line in buf):
            chunks.append({'path': str(path), 'heading': heading, 'line': start,
                           'lines': list(buf), 'text': '\n'.join(buf)})

    for i, line in enumerate(lines, start=1):
        match = HEADING_RE.match(line)
        if match or len(buf) >= CHUNK_MAX_LINES:
            flush()
            buf, start = [], i
            if match:
                heading = match.group(2).strip()
        buf.append(line)
    flush()
    for chunk in chunks:
        chunk['tokens'] = Counter(tokens_of(chunk['text']))
        chunk['label_tokens'] = set(tokens_of(chunk['heading']))
    return chunks


def rank(query, chunks, limit=6):
    """Term frequency against inverse document frequency, heading weighted."""
    terms = tokens_of(query)
    if not terms or not chunks:
        return []
    doc_freq = Counter()
    for chunk in chunks:
        for term in set(terms):
            if chunk['tokens'].get(term):
                doc_freq[term] += 1
    total = len(chunks)
    phrase = fold(query).strip()

    scored = []
    for chunk in chunks:
        score, hits = 0.0, 0
        for term in terms:
            count = chunk['tokens'].get(term, 0)
            if not count:
                continue
            hits += 1
            weight = math.log((total + 1) / (doc_freq[term] + 1)) + 1.0
            score += (1 + math.log(count)) * weight
            if term in chunk['label_tokens']:
                score += 1.5 * weight
        if not hits:
            continue
        score *= (hits / len(terms)) ** 1.5
        if len(phrase) > 6 and phrase in fold(chunk['text']):
            score += 6.0
        scored.append((score, chunk))

    scored.sort(key=lambda pair: (-pair[0], pair[1]['path'], pair[1]['line']))
    results = []
    for _, chunk in scored[:limit]:
        best, best_hits, offset = '', 0, 0
        for i, line in enumerate(chunk['lines']):
            found = sum(1 for term in set(terms) if term in fold(line))
            if found > best_hits:
                best, best_hits, offset = line.strip(), found, i
        results.append({'path': chunk['path'], 'line': chunk['line'] + offset,
                        'heading': chunk['heading'],
                        'snippet': ' '.join(best.split())[:220] or ' '.join(chunk['text'].split())[:220]})
    return results


# ---------------------------------------------------------------------------
# the model
# ---------------------------------------------------------------------------

def parse_entries(text, source=''):
    """Entries out of one model file. Format is heading plus labelled bullets.

    HTML comment blocks are skipped: every model file carries the format example
    in a comment, and an example is not an entry.
    """
    entries = []
    current = None
    in_comment = False
    for lineno, line in enumerate(text.split('\n'), start=1):
        if in_comment:
            if '-->' in line:
                in_comment = False
            continue
        if line.lstrip().startswith('<!--') and '-->' not in line:
            in_comment = True
            continue
        head = ENTRY_HEAD.match(line)
        if head:
            if current:
                entries.append(current)
            current = {'id': head.group(1), 'title': head.group(2).strip(),
                       'fields': {}, 'line': lineno, 'source': source, 'body': []}
            continue
        if current is None:
            continue
        field = FIELD.match(line)
        if field:
            current['fields'][field.group(1).strip().lower()] = field.group(2).strip()
        elif line.strip():
            current['body'].append(line.strip())
    if current:
        entries.append(current)
    return entries


def all_entries(store=None):
    store = home() if store is None else store
    entries = []
    for kind, (prefix, relpath, label) in KINDS.items():
        path = store / relpath
        for entry in parse_entries(read(path), source=relpath):
            entry['kind'] = kind
            entry['label'] = label
            entries.append(entry)
    return entries


def next_id(prefix, entries):
    used = [int(e['id'][2:]) for e in entries if e['id'].startswith(prefix + '-')]
    return '%s-%03d' % (prefix, max(used, default=0) + 1)


def format_entry(entry_id, title, fields, note=''):
    lines = ['### %s. %s' % (entry_id, title), '']
    for label, value in fields.items():
        lines.append('- **%s:** %s' % (label, value))
    if note:
        lines += ['', note]
    lines.append('')
    return '\n'.join(lines)


def add_entry(kind, title, fields, note='', store=None):
    """Append one entry to its file and return the id it got."""
    store = home() if store is None else store
    prefix, relpath, label = KINDS[kind]
    path = store / relpath
    entry_id = next_id(prefix, all_entries(store))
    body = read(path).rstrip('\n')
    payload = format_entry(entry_id, title, fields, note)
    write(path, (body + '\n\n' + payload) if body else payload)
    return entry_id


# ---------------------------------------------------------------------------
# the question bank
# ---------------------------------------------------------------------------

def parse_bank_text(text):
    questions = []
    domain = ''
    for line in text.split('\n'):
        heading = BANK_DOMAIN.match(line)
        if heading:
            domain = heading.group(1).strip()
            continue
        item = BANK_ITEM.match(line.strip())
        if item and domain:
            questions.append({'id': item.group(1), 'priority': item.group(2),
                              'domain': domain, 'text': item.group(3).strip()})
    return questions


def store_bank_path(store=None):
    return (home() if store is None else store) / 'questions.md'


def parse_bank(text=None, store=None):
    """The starter bank plus whatever the person's own answers have added.

    A fixed list of questions written by someone else runs out, and worse, it
    keeps asking about the life it imagined instead of the one being lived. Any
    answer that opens a new question gets that question appended to the store's
    own bank, and from then on it is part of the pool.
    """
    if text is not None:
        return parse_bank_text(text)
    questions = parse_bank_text(read(BANK_PATH))
    questions += parse_bank_text(read(store_bank_path(store)))
    seen, unique = set(), []
    for question in questions:
        if question['id'] in seen:
            continue
        seen.add(question['id'])
        unique.append(question)
    return unique


def add_question(text, domain='kendi', priority='P1', store=None):
    """Append a question to the person's own bank."""
    store = home() if store is None else store
    path = store_bank_path(store)
    existing = parse_bank(store=store)
    used = [int(q['id'][2:]) for q in existing if q['id'][2:].isdigit()]
    question_id = 'S-%03d' % (max(used, default=0) + 1)
    body = read(path)
    if not body:
        body = ('# Kendi soruların\n\nCevaplarından doğan sorular buraya eklenir. '
                'Başlangıç bankası mind/questions/bank.md, bu dosya onun devamı.\n')
    header = '## %s' % domain
    line = '- %s [%s] %s' % (question_id, priority, text.strip())
    if header in body:
        parts = body.split(header, 1)
        rest = parts[1].split('\n## ', 1)
        block = rest[0].rstrip('\n') + '\n' + line + '\n'
        body = parts[0] + header + block + ('\n## ' + rest[1] if len(rest) > 1 else '')
    else:
        body = body.rstrip('\n') + '\n\n%s\n\n%s\n' % (header, line)
    write(path, body)
    return question_id


def state_path(store=None):
    return (home() if store is None else store) / 'state.json'


def load_state(store=None):
    path = state_path(store)
    if not path.exists():
        return {'asked': {}, 'answered': [], 'processed': [], 'fidelity': []}
    try:
        data = json.loads(read(path))
    except json.JSONDecodeError:
        return {'asked': {}, 'answered': [], 'processed': [], 'fidelity': []}
    for key, default in (('asked', {}), ('answered', []), ('processed', []), ('fidelity', [])):
        data.setdefault(key, default)
    return data


def save_state(data, store=None):
    write(state_path(store), json.dumps(data, ensure_ascii=False, indent=2) + '\n')


# ---------------------------------------------------------------------------
# raw capture: inbox and interview sessions
# ---------------------------------------------------------------------------

SESSION_Q = re.compile(r'^##\s+(S-\d{3})\s+\[(P[123])\]\s+(.+)$')
ANSWER_MARK = '**Cevap:**'


def session_path(when=None, store=None):
    store = home() if store is None else store
    return store / 'sessions' / ('%s.md' % (when or today()))


def parse_session(text):
    """Question blocks in a session file, with whatever answer was written."""
    blocks = []
    current = None
    collecting = False
    for line in text.split('\n'):
        head = SESSION_Q.match(line)
        if head:
            if current:
                blocks.append(current)
            current = {'id': head.group(1), 'priority': head.group(2),
                       'question': head.group(3).strip(), 'answer': []}
            collecting = False
            continue
        if current is None:
            continue
        if line.strip().startswith(ANSWER_MARK):
            collecting = True
            rest = line.strip()[len(ANSWER_MARK):].strip()
            if rest:
                current['answer'].append(rest)
            continue
        if line.strip() == '---':
            collecting = False
            continue
        if collecting and line.strip():
            current['answer'].append(line.rstrip())
    if current:
        blocks.append(current)
    for block in blocks:
        block['answer'] = '\n'.join(block['answer']).strip()
    return blocks


def all_sessions(store=None):
    store = home() if store is None else store
    folder = store / 'sessions'
    sessions = []
    if folder.is_dir():
        for path in sorted(folder.glob('*.md')):
            sessions.append({'path': path, 'date': path.stem, 'blocks': parse_session(read(path))})
    return sessions


def answered_ids(store=None):
    answered = set(load_state(store)['answered'])
    for session in all_sessions(store):
        answered.update(block['id'] for block in session['blocks'] if block['answer'])
    return answered


def domain_coverage(store=None):
    counts = Counter()
    for entry in all_entries(store):
        counts[entry['fields'].get('alan', 'belirsiz')] += 1
    return counts


def pick_questions(n=8, domain=None, store=None):
    """Highest-yield unanswered questions.

    Priority first, then the domains the clone knows least about, so a session
    spends its minutes where the model is thinnest rather than where the bank
    happens to start.
    """
    answered = answered_ids(store)
    coverage = domain_coverage(store)
    pool = [q for q in parse_bank(store=store) if q['id'] not in answered]
    if domain:
        pool = [q for q in pool if domain.lower() in q['domain'].lower()]
    pool.sort(key=lambda q: (q['priority'], coverage.get(q['domain'], 0), q['id']))
    return pool[:n]


def capture(text, store=None, tag=''):
    store = home() if store is None else store
    stamp = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    path = store / 'inbox' / ('%s-%s.md' % (stamp, slugify(tag or text)))
    write(path, '---\ntarih: %s\netiket: %s\n---\n\n%s\n' % (today(), tag or 'serbest', text.strip()))
    return path


def raw_items(store=None, include_processed=False):
    """Everything captured that has not yet been distilled into the model."""
    store = home() if store is None else store
    processed = set(load_state(store)['processed'])
    items = []
    folder = store / 'inbox'
    if folder.is_dir():
        for path in sorted(folder.glob('*.md')):
            item_id = 'inbox:%s' % path.stem
            if include_processed or item_id not in processed:
                items.append({'id': item_id, 'kind': 'inbox', 'path': path,
                              'text': read(path), 'label': path.name})
    for session in all_sessions(store):
        for block in session['blocks']:
            if not block['answer']:
                continue
            item_id = 'session:%s:%s' % (session['date'], block['id'])
            if include_processed or item_id not in processed:
                items.append({'id': item_id, 'kind': 'session', 'path': session['path'],
                              'text': 'Soru: %s\n\nCevap: %s' % (block['question'], block['answer']),
                              'label': '%s %s' % (session['date'], block['id'])})
    return items


# ---------------------------------------------------------------------------
# optional seeding from a work repo
#
# Off by default. The clone is a person, not a project, and a project only ever
# shows one slice of one. When `init --from-repo` is passed, these hypotheses
# are drawn from the decisions recorded in this repository and land unconfirmed
# with their evidence, so confirming or rejecting one takes a second.
# ---------------------------------------------------------------------------

REPO_SEEDS = [
    ('kural', 'Çalışan bir sistem onay istemek yerine kendini toparlamalı',
     'otomasyon', 'orta',
     'workflow/incident-log.md 2026-05-15: operatör, izin isteyen bileşik komutu reddederek "tam otonom değil" noktasını kanıtladı',
     'Otonomi burada bir konfor tercihi değil, sistemin tanımı gibi davranılıyor.'),
    ('inanc', 'Görünmeyen borç, bilinen borçtan tehlikelidir',
     'kalite', 'yüksek',
     'checklist/qa-gate.md "Rule scope" ve workflow/qa-baseline.txt: kapsam dışı kalan içeriğin açığı aynı gün yazılı hale getiriliyor',
     ''),
    ('kural', 'Yeni bir kural eklerken kapsamı aynı satırda yazılır',
     'kalite', 'yüksek',
     'checklist/qa-gate.md "Rule scope", incident-log 2026-08-11',
     'Kapsamsız kural, sessiz uyumsuzluk üretiyor.'),
    ('tercih', 'Kapanmış bir konu denetimlerde yeniden açılmaz',
     'calisma-tarzi', 'orta',
     'brand/voice-samples/README.md: "Do not re-open this as an action item in audits"',
     ''),
    ('inanc', 'Rekabet duruşu zayıfken o karşılaştırmayı hiç yazmamak daha iyidir',
     'strateji', 'orta',
     'ROADMAP.md Step 2: yüksek getirili mevduat, doğrudan kiralık ve tatil kiralaması karşılaştırmaları askıya alındı',
     'İçerik fırsatı ile konumlanma riski çatıştığında konumlanma kazanıyor.'),
    ('tercih', 'Müşteriye giden şey tek ve temiz olmalı, sürüm yığını değil',
     'teslimat', 'orta',
     'workflow/pipeline.md Stage 9: yükleme öncesi klasör temizleniyor',
     ''),
    ('kural', 'Kalite kapısı koda gömülmeli, iyi niyete bırakılmamalı',
     'kalite', 'yüksek',
     'workflow/deliver.py: QA raporu olmadan teslimat reddediliyor, 2026-05-26 kaçağından sonra eklendi',
     ''),
    ('inanc', 'Uzun tire, metnin makine yazımı olduğunu ele veren en güçlü işarettir',
     'icerik', 'yüksek',
     'checklist/ai-tells.md Tier 0',
     ''),
    ('tercih', 'Sayı, sıfattan iyidir',
     'icerik', 'yüksek',
     'brand/tone-and-voice.md ses kuralı 6',
     ''),
    ('inanc', 'İnsan hikayesi taşımayan metin insan gibi okunmaz',
     'icerik', 'yüksek',
     'checklist/humanization-pass.md: Real Story, POV Anchor, Contrarian Note zorunlu',
     ''),
    ('inanc', 'Okur iki makale okuduğunda karakter çakışmasını fark eder',
     'icerik', 'orta',
     'workflow/incident-log.md 2026-05-26: 15 makalenin 13ünde aynı isim',
     ''),
    ('tercih', 'Kimlik bilgisi hiçbir koşulda repoya girmez',
     'guvenlik', 'yüksek',
     'SECURITY.md ve push.sh içindeki gömülü token temizliği',
     ''),
    ('kural', 'Bir hata tekrar ederse kural olur, tek seferlikse sadece not',
     'ogrenme', 'orta',
     'workflow/incident-log.md giriş şablonu: "the new active rule (if any), or no new rule, one-off"',
     ''),
    ('inanc', 'Retrospektif atlanırsa öğrenme döngüsü kırılır',
     'ogrenme', 'yüksek',
     'workflow/trigger-contract.md Stage 11: "Skipping post-run QA breaks the learning loop"',
     ''),
    ('tercih', 'Paralı araca bağımlılık yerine herkesin görebildiği kaynak',
     'arastirma', 'orta',
     'workflow/incident-log.md Active rules: Semrush çağrılmıyor, WebFetch ve WebSearch tek yol',
     ''),
    ('kural', 'Önce hub, sonra ona bağlanan spoke',
     'strateji', 'orta',
     'checklist/topic-selection.md ve pipeline Stage -1',
     ''),
    ('inanc', 'Ölçülmeyen içerik kalitesi zamanla dalgalanır',
     'kalite', 'yüksek',
     'workflow/incident-log.md 2026-08-11: batch başına yeniden yazılan kontroller yüzünden kapsam oynuyordu',
     ''),
    ('inanc', 'ABD dışına çıkmak şu aşamada dikkat dağıtır',
     'strateji', 'orta',
     'ROADMAP.md operating scope: tek pazar, tek dil',
     ''),
    ('soru', 'Batch 2 kapak yenilemesi neden geri alındı?',
     'acik', 'düşük',
     'git 0bf8ddf, gerekçe commit mesajında yok, kapaklar Drive a yüklenmişti',
     'Cevap gelene kadar kapaklar yeniden üretilmemeli.'),
]


MODEL_HEADERS = {
    'model/beliefs.md': ('İnançlar', 'Doğru olduğunu düşündüğün şeyler. Her biri bir kanıta ve bir güven seviyesine bağlı.'),
    'model/heuristics.md': ('Kurallar', 'Karar verirken kullandığın eğer/o zaman kalıpları. Klonun sana en çok benzediği yer burası.'),
    'model/preferences.md': ('Tercihler', 'Neyi sevdiğin, neye tahammül etmediğin, nasıl çalışmak istediğin.'),
    'model/decisions.md': ('Kararlar', 'Verilmiş kararlar ve sonuçları. Zamanla en değerli dosya bu olur: yargının kaydı.'),
    'model/open-questions.md': ('Açık sorular', 'Cevabını bilmediğin ama bilmen gereken şeyler.'),
    'model/identity.md': ('Kimlik', 'Kim olduğun, ne yaptığın, neyi hedeflediğin. Klonun başlangıç noktası.'),
    'model/voice.md': ('Ses', 'Nasıl konuşuyorsun. Klon senin adına yazacaksa buradan öğrenir.'),
}

ENTRY_FORMAT_NOTE = """<!-- Biçim: her giriş bir başlık ve altında etiketli satırlar.

### B-001. Kısa ve tek cümlelik ifade

- **Tür:** inanç
- **Alan:** strateji
- **Güven:** yüksek | orta | düşük
- **Durum:** onaysız | onaylı | revize | reddedildi
- **Kaynak:** nereden geldi (oturum, kutu girdisi, repo kanıtı)
- **Tarih:** YYYY-MM-DD

Elle yazabilirsin, ya da:
python3 workflow/mind.py add --kind inanc --title "..." --alan strateji --kaynak "..."
-->"""


def init(store=None, reseed=False, from_repo=False):
    """Create the store. Seeding from the work repo is opt in."""
    store = home() if store is None else store
    created = []
    for folder in ('model', 'model/domains', 'inbox', 'sessions', 'deltas'):
        (store / folder).mkdir(parents=True, exist_ok=True)

    for relpath, (title, blurb) in MODEL_HEADERS.items():
        path = store / relpath
        if path.exists():
            continue
        header = '# %s\n\n%s\n' % (title, blurb)
        if relpath in [p for _, p, _ in KINDS.values()]:
            header += '\n' + ENTRY_FORMAT_NOTE + '\n'
        write(path, header)
        created.append(relpath)

    seeded = 0
    if from_repo and (reseed or not all_entries(store)):
        for kind, title, alan, guven, kaynak, note in REPO_SEEDS:
            add_entry(kind, title, {
                'Tür': KINDS[kind][2], 'Alan': alan, 'Güven': guven,
                'Durum': 'onaysız', 'Kaynak': 'bu iş reposundan çıkarıldı: ' + kaynak,
                'Tarih': today(),
            }, note=note, store=store)
            seeded += 1

    if not state_path(store).exists():
        save_state(load_state(store), store)
    return created, seeded


# ---------------------------------------------------------------------------
# recall
# ---------------------------------------------------------------------------

def entry_text(entry):
    return ' '.join([entry['title']] + list(entry['fields'].values()) + entry['body'])


def match_entries(query, store=None, limit=8):
    terms = {t for t in tokens_of(query) if len(t) > 2}
    scored = []
    for entry in all_entries(store):
        tokens = set(tokens_of(entry_text(entry)))
        hits = terms & tokens
        if not hits:
            continue
        score = len(hits) / max(len(terms), 1)
        if entry['fields'].get('durum') == 'onaylı':
            score += 0.25
        scored.append((score, entry))
    scored.sort(key=lambda pair: (-pair[0], pair[1]['id']))
    return [entry for _, entry in scored[:limit]]


def store_chunks(store=None):
    """Index everything in the store: model, sessions, inbox, rehearsals."""
    store = home() if store is None else store
    chunks = []
    for path in sorted(store.rglob('*.md')):
        chunks.extend(chunks_of(path))
    return chunks


def ask(query, store=None, limit=6):
    store = home() if store is None else store
    entries = match_entries(query, store, limit=limit)
    raw = rank(query, store_chunks(store), limit=limit)
    terms = {t for t in tokens_of(query) if len(t) > 3}
    suggestions = [q for q in parse_bank(store=store)
                   if terms & set(tokens_of(q['text']))
                   and q['id'] not in answered_ids(store)][:3]
    return {'entries': entries, 'raw': raw, 'suggestions': suggestions}


# ---------------------------------------------------------------------------
# advancing: rehearse, grade, measure
# ---------------------------------------------------------------------------

VERDICTS = {'right': 1.0, 'partial': 0.5, 'wrong': 0.0}
VERDICT_TR = {'right': 'tutturdu', 'partial': 'kısmen', 'wrong': 'ıskaladı'}


def rehearse(question, store=None):
    """Open a prediction: the clone answers first, the owner corrects after."""
    store = home() if store is None else store
    folder = store / 'deltas'
    folder.mkdir(parents=True, exist_ok=True)
    used = [int(p.stem.split('-')[1]) for p in folder.glob('X-*.md') if p.stem.split('-')[1].isdigit()]
    delta_id = 'X-%03d' % (max(used, default=0) + 1)
    path = folder / ('%s.md' % delta_id)
    write(path, '\n'.join([
        '# %s provası' % delta_id,
        '',
        '- **Tarih:** %s' % today(),
        '- **Soru:** %s' % question,
        '- **Durum:** bekliyor',
        '',
        '## Klonun cevabı',
        '',
        '(Ajan burayı doldurur: sadece onaylı girdilerden, kullandığı girdi idlerini yazarak.)',
        '',
        '## Senin cevabın',
        '',
        '',
        '## Fark',
        '',
        '(İki cevap arasındaki fark. Bu fark yeni bir kural, inanç ya da tercih doğurur.)',
        '',
    ]))
    return delta_id, path


def grade(delta_id, verdict, note='', store=None):
    store = home() if store is None else store
    path = store / 'deltas' / ('%s.md' % delta_id)
    if not path.exists():
        return None
    text = read(path).replace('- **Durum:** bekliyor',
                              '- **Durum:** %s (%s)' % (VERDICT_TR[verdict], today()))
    if note:
        text = text.rstrip('\n') + '\n\n## Not\n\n%s\n' % note
    write(path, text)
    data = load_state(store)
    data['fidelity'].append({'id': delta_id, 'date': today(), 'verdict': verdict})
    save_state(data, store)
    return path


def fidelity(store=None):
    records = load_state(store)['fidelity']
    if not records:
        return {'count': 0, 'overall': None, 'recent': None, 'records': []}
    scores = [VERDICTS[r['verdict']] for r in records if r['verdict'] in VERDICTS]
    recent = scores[-10:]
    return {'count': len(scores),
            'overall': round(100 * sum(scores) / len(scores)) if scores else None,
            'recent': round(100 * sum(recent) / len(recent)) if recent else None,
            'records': records}


# ---------------------------------------------------------------------------
# health
# ---------------------------------------------------------------------------

def is_stale(entry):
    stamp = entry['fields'].get('tarih', '')
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', stamp):
        return False
    age = date.today() - date.fromisoformat(stamp)
    return age > timedelta(days=STALE_DAYS) and entry['fields'].get('durum') == 'onaylı'


def gaps(store=None):
    store = home() if store is None else store
    entries = all_entries(store)
    coverage = domain_coverage(store)
    bank = parse_bank(store=store)
    answered = answered_ids(store)
    bank_domains = {q['domain'] for q in bank}
    return {
        'thin_domains': sorted(d for d in bank_domains if coverage.get(d, 0) == 0),
        'unconfirmed': [e for e in entries if e['fields'].get('durum') == 'onaysız'],
        'stale': [e for e in entries if is_stale(e)],
        'sourceless': [e for e in entries if not e['fields'].get('kaynak')],
        'unanswered_p1': [q for q in bank if q['priority'] == 'P1' and q['id'] not in answered],
        'next': pick_questions(5, store=store),
        'raw_pending': raw_items(store),
    }


def check(store=None):
    """Integrity of the clone, and of the assets when there is no clone yet."""
    findings = []
    store = home() if store is None else store

    bank = parse_bank(store=store)
    if not bank:
        findings.append(('FAIL', 'soru bankası okunamadı: %s' % BANK_PATH))
    seen = {}
    for question in bank:
        if question['id'] in seen:
            findings.append(('FAIL', 'soru bankasında tekrar eden id: %s' % question['id']))
        seen[question['id']] = question
    if not PROTOCOL.exists():
        findings.append(('FAIL', 'ajan protokolü yok: %s' % PROTOCOL))

    if not store.exists():
        findings.append(('INFO', 'klon deposu yok. Kurmak için: python3 workflow/mind.py init'))
        return findings

    ids = {}
    for entry in all_entries(store):
        if entry['id'] in ids:
            findings.append(('FAIL', '%s iki kez tanımlı (%s ve %s)'
                             % (entry['id'], ids[entry['id']], entry['source'])))
        ids[entry['id']] = entry['source']
        durum = entry['fields'].get('durum', '')
        guven = entry['fields'].get('güven', '')
        if durum not in STATUSES:
            findings.append(('FAIL', '%s geçersiz durum: %r' % (entry['id'], durum)))
        if entry['kind'] != 'soru' and guven not in CONFIDENCE:
            findings.append(('FAIL', '%s geçersiz güven: %r' % (entry['id'], guven)))
        if not entry['fields'].get('kaynak'):
            findings.append(('WARN', '%s kaynaksız, nereden geldiği yazılmamış' % entry['id']))
        if not entry['fields'].get('tarih'):
            findings.append(('WARN', '%s tarihsiz' % entry['id']))

    for record in load_state(store)['fidelity']:
        if not (store / 'deltas' / ('%s.md' % record['id'])).exists():
            findings.append(('WARN', 'fidelity kaydı %s için prova dosyası yok' % record['id']))

    for entry in all_entries(store):
        if is_stale(entry):
            findings.append(('WARN', '%s %s tarihli, tazelenmeli' % (entry['id'], entry['fields'].get('tarih'))))
    return findings


def stats(store=None):
    store = home() if store is None else store
    entries = all_entries(store)
    raw = raw_items(store, include_processed=True)
    bank = parse_bank(store=store)
    answered = answered_ids(store)
    words = sum(len(entry_text(e).split()) for e in entries)
    words += sum(len(item['text'].split()) for item in raw)
    return {
        'entries': entries, 'by_kind': Counter(e['kind'] for e in entries),
        'by_status': Counter(e['fields'].get('durum', 'belirsiz') for e in entries),
        'coverage': domain_coverage(store), 'raw': raw,
        'sessions': all_sessions(store), 'bank': bank, 'answered': answered,
        'words': words, 'fidelity': fidelity(store), 'pending': raw_items(store),
    }


def confirm(entry_id, status, note='', store=None):
    """Set an entry's status in place. The seed review runs on this.

    Comment blocks are stepped over: every model file carries a format example
    with a sample id in it, and rewriting the example instead of the entry is a
    silent way to corrupt someone's own notes.
    """
    store = home() if store is None else store
    for kind, (prefix, relpath, label) in KINDS.items():
        if not entry_id.startswith(prefix + '-'):
            continue
        path = store / relpath
        out, inside, in_comment, touched = [], False, False, False
        for line in read(path).split('\n'):
            if in_comment:
                out.append(line)
                if '-->' in line:
                    in_comment = False
                continue
            if line.lstrip().startswith('<!--') and '-->' not in line:
                in_comment = True
                out.append(line)
                continue
            head = ENTRY_HEAD.match(line)
            if head:
                inside = head.group(1) == entry_id
            if inside and line.startswith('- **Durum:**'):
                out.append('- **Durum:** %s' % status)
                if note:
                    out.append('- **Not (%s):** %s' % (today(), note))
                touched = True
                continue
            if inside and touched and line.startswith('- **Tarih:**'):
                out.append('- **Tarih:** %s' % today())
                continue
            out.append(line)
        if touched:
            write(path, '\n'.join(out))
            return path
    return None


# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------

def cmd_init(args):
    store = home()
    created, seeded = init(store, reseed=args.reseed, from_repo=args.from_repo)
    print('Klon deposu: %s' % store)
    print('  %d dosya oluşturuldu.' % len(created))
    if seeded:
        print('  %d tohum girdi bu iş reposundan çıkarıldı, hepsi "onaysız".' % seeded)
        print('  Gözden geçir: python3 workflow/mind.py gaps')
    print('')
    print('Klon boş başlar ve senin cevaplarınla dolar. İlk oturum:')
    print('')
    print('  python3 workflow/mind.py interview --n 8')
    print('')
    print('Sorular oturum dosyasına yazılır, cevapları altına yazarsın, sonra:')
    print('  python3 workflow/mind.py distill')
    return 0


def cmd_capture(args):
    text = ' '.join(args.text) if args.text else sys.stdin.read()
    if not text.strip():
        print('Boş girdi. Metni argüman olarak ya da stdin ile ver.', file=sys.stderr)
        return 2
    path = capture(text, tag=args.tag)
    print('Kutuya düştü: %s' % path)
    print('Modele işlemek için: python3 workflow/mind.py distill')
    return 0


def cmd_interview(args):
    store = home()
    questions = pick_questions(args.n, args.domain, store)
    if not questions:
        print('Bankada cevaplanmamış soru kalmadı%s.'
              % (' (%s alanında)' % args.domain if args.domain else ''))
        print('Yeni soru eklemek için: mind/questions/bank.md')
        return 1
    path = session_path(store=store)
    existing = read(path)
    already = {block['id'] for block in parse_session(existing)}
    blocks = []
    for question in questions:
        if question['id'] in already:
            continue
        blocks.append('\n'.join([
            '## %s [%s] %s' % (question['id'], question['priority'], question['text']),
            '',
            '_%s_' % question['domain'],
            '',
            ANSWER_MARK,
            '',
            '',
            '---',
            '',
        ]))
    if not existing:
        existing = '\n'.join([
            '# Oturum %s' % today(),
            '',
            'Cevapları **Cevap:** satırının altına yaz. Ham hali yeterli, düzeltmeyi klon yapar.',
            'Bilmiyorsan boş bırak, soru bir sonraki oturumda geri gelir.',
            '',
            'Bitince: python3 workflow/mind.py distill',
            '',
            '---',
            '',
        ])
    write(path, existing.rstrip('\n') + '\n\n' + '\n'.join(blocks))
    print('Oturum dosyası: %s' % path)
    print('')
    for question in questions:
        print('  %s [%s] %s' % (question['id'], question['priority'], question['text']))
    print('')
    print('%d soru yazıldı. Cevapları dosyaya yaz, sonra: python3 workflow/mind.py distill' % len(blocks))
    return 0


def cmd_distill(args):
    store = home()
    pending = raw_items(store)
    if args.done_all or args.done:
        data = load_state(store)
        marked = [item['id'] for item in pending] if args.done_all else list(args.done)
        data['processed'] = sorted(set(data['processed']) | set(marked))
        save_state(data, store)
        print('%d ham kayıt işlenmiş olarak işaretlendi.' % len(marked))
        return 0
    if not pending:
        print('İşlenmemiş ham kayıt yok. Kutu ve oturumlar temiz.')
        return 0
    print('İŞLENMEMİŞ HAM KAYITLAR (%d)' % len(pending))
    print('')
    print('Bunları modele çevir. Her cümle için sor: bu bir inanç mı, bir karar kuralı mı,')
    print('bir tercih mi, verilmiş bir karar mı, yoksa açık bir soru mu? Uydurma, sadece')
    print('yazılanı yapılandır. Emin olmadığın yeri açık soru olarak bırak.')
    print('')
    for item in pending:
        print('=' * 72)
        print('%s  (%s)' % (item['id'], item['label']))
        print('-' * 72)
        print(item['text'].strip()[:2000])
        print('')
    print('=' * 72)
    print('')
    print('Girdi yazmak için:')
    print('  python3 workflow/mind.py add --kind kural --title "..." \\')
    print('      --alan karar-verme --guven orta --kaynak "%s"' % pending[0]['id'])
    print('')
    print('Hepsi işlendiğinde: python3 workflow/mind.py distill --done-all')
    return 0


def cmd_add(args):
    store = home()
    entry_id = add_entry(args.kind, args.title, {
        'Tür': KINDS[args.kind][2],
        'Alan': args.alan or 'belirsiz',
        'Güven': args.guven,
        'Durum': args.durum,
        'Kaynak': args.kaynak or 'elle eklendi',
        'Tarih': today(),
    }, note=args.note or '', store=store)
    print('%s yazıldı: %s' % (entry_id, args.title))
    return 0


def cmd_confirm(args):
    path = confirm(args.id, args.durum, args.note or '')
    if not path:
        print('%s bulunamadı.' % args.id, file=sys.stderr)
        return 1
    print('%s → %s (%s)' % (args.id, args.durum, path))
    return 0


def cmd_addq(args):
    question_id = add_question(' '.join(args.text), domain=args.domain, priority=args.priority)
    print('%s eklendi (%s): %s' % (question_id, args.domain, ' '.join(args.text)))
    print('Havuza girdi, sıradaki oturumda çıkabilir.')
    return 0


def cmd_ask(args):
    store = home()
    query = ' '.join(args.query)
    result = ask(query, store, limit=args.limit)
    if not result['entries'] and not result['raw']:
        print('Klon bu konuda hiçbir şey tutmuyor: %r' % query)
        if result['suggestions']:
            print('')
            print('Sormaya değer sorular:')
            for question in result['suggestions']:
                print('  %s %s' % (question['id'], question['text']))
        return 1
    if result['entries']:
        print('KLONUN BİLDİĞİ')
        print('')
        for entry in result['entries']:
            fields = entry['fields']
            print('  %s [%s / %s] %s' % (entry['id'], fields.get('durum', '?'),
                                         fields.get('güven', '?'), entry['title']))
            if fields.get('kaynak'):
                print('      kaynak: %s' % fields['kaynak'][:110])
        print('')
    if result['raw']:
        print('HAM KAYITLARDAN')
        print('')
        for hit in result['raw']:
            where = hit['path']
            try:
                where = str(Path(where).relative_to(store))
            except ValueError:
                pass
            print('  %s:%d  %s' % (where, hit['line'], hit['snippet'][:150]))
        print('')
    unconfirmed = [e for e in result['entries'] if e['fields'].get('durum') == 'onaysız']
    if unconfirmed:
        print('DİKKAT: %d girdi henüz onaylanmamış (%s). Klon bunları senin görüşün diye sunmamalı.'
              % (len(unconfirmed), ', '.join(e['id'] for e in unconfirmed)))
        print('')
    if result['suggestions']:
        print('BOŞLUK: bu konuda sorulmamış sorular')
        for question in result['suggestions']:
            print('  %s %s' % (question['id'], question['text']))
    return 0


def cmd_rehearse(args):
    store = home()
    question = ' '.join(args.question) if args.question else ''
    if not question:
        pending = [q for q in parse_bank(store=store) if q['id'] not in answered_ids(store)]
        if not pending:
            print('Prova için soru kalmadı.', file=sys.stderr)
            return 1
        question = pending[0]['text']
    delta_id, path = rehearse(question, store)
    print('%s açıldı: %s' % (delta_id, path))
    print('')
    print('Sıra: klon önce cevaplasın (sadece onaylı girdilerden, id atıfıyla), sonra sen')
    print('kendi cevabını yaz. Fark, klonun sana benzemediği yerdir ve yeni girdi doğurur.')
    print('')
    print('Notlandırmak için: python3 workflow/mind.py grade %s --verdict right|partial|wrong' % delta_id)
    return 0


def cmd_grade(args):
    path = grade(args.id, args.verdict, args.note or '')
    if not path:
        print('%s bulunamadı.' % args.id, file=sys.stderr)
        return 1
    score = fidelity()
    print('%s: %s' % (args.id, VERDICT_TR[args.verdict]))
    print('Sadakat: genel %%%s, son 10 prova %%%s (%d prova)'
          % (score['overall'], score['recent'], score['count']))
    return 0


def cmd_fidelity(args):
    score = fidelity()
    if not score['count']:
        print('Henüz prova yok. Başlamak için: python3 workflow/mind.py rehearse')
        return 1
    print('Sadakat: genel %%%s, son 10 prova %%%s (%d prova)'
          % (score['overall'], score['recent'], score['count']))
    print('')
    for record in score['records'][-12:]:
        print('  %s  %-8s %s' % (record['date'], VERDICT_TR.get(record['verdict'], '?'), record['id']))
    return 0


def cmd_gaps(args):
    store = home()
    if not store.exists():
        print('Klon deposu yok. Kurmak için: python3 workflow/mind.py init', file=sys.stderr)
        return 1
    report = gaps(store)
    print('BOŞLUKLAR')
    print('')
    print('  Onaysız girdi        %d' % len(report['unconfirmed']))
    print('  Kaynaksız girdi      %d' % len(report['sourceless']))
    print('  Tazelenmesi gereken  %d' % len(report['stale']))
    print('  İşlenmemiş ham kayıt %d' % len(report['raw_pending']))
    print('  Cevapsız P1 soru     %d' % len(report['unanswered_p1']))
    if report['thin_domains']:
        print('')
        print('  Hiç girdisi olmayan alanlar:')
        for domain in report['thin_domains']:
            print('    %s' % domain)
    if report['unconfirmed'][:args.limit]:
        print('')
        print('  Onay bekleyenler:')
        for entry in report['unconfirmed'][:args.limit]:
            print('    %s  %s' % (entry['id'], entry['title'][:90]))
    print('')
    print('  Sıradaki sorular:')
    for question in report['next']:
        print('    %s [%s] %s' % (question['id'], question['priority'], question['text'][:88]))
    return 0


def cmd_digest(args):
    store = home()
    cutoff = (date.today() - timedelta(days=args.days)).isoformat()
    entries = [e for e in all_entries(store) if e['fields'].get('tarih', '') >= cutoff]
    sessions = [s for s in all_sessions(store) if s['date'] >= cutoff]
    score = fidelity(store)
    print('SON %d GÜN' % args.days)
    print('')
    print('  Yeni ya da güncellenen girdi  %d' % len(entries))
    print('  Oturum                        %d' % len(sessions))
    print('  Cevaplanan soru               %d'
          % sum(1 for s in sessions for b in s['blocks'] if b['answer']))
    if score['count']:
        print('  Sadakat                       genel %%%s, son 10 %%%s' % (score['overall'], score['recent']))
    print('')
    for entry in entries[:args.limit]:
        print('  %s [%s] %s' % (entry['id'], entry['fields'].get('durum', '?'), entry['title'][:88]))
    print('')
    report = gaps(store)
    print('  Sıradaki hamle: %d onaysız girdiyi gözden geçir, %d ham kaydı modele çevir.'
          % (len(report['unconfirmed']), len(report['raw_pending'])))
    return 0


def cmd_check(args):
    findings = check()
    fails = [f for f in findings if f[0] == 'FAIL']
    for level, message in findings:
        if level == 'WARN' and args.quiet:
            continue
        print('  [%s] %s' % (level, message), file=sys.stderr)
    print('\n%d FAIL, %d WARN.' % (len(fails), len([f for f in findings if f[0] == 'WARN'])),
          file=sys.stderr)
    return 1 if fails else 0


def cmd_stats(args):
    store = home()
    if not store.exists():
        print('Klon deposu yok. Kurmak için: python3 workflow/mind.py init', file=sys.stderr)
        return 1
    data = stats(store)
    print('Klon        %s' % store)
    print('Girdi       %d toplam' % len(data['entries']))
    for kind, count in data['by_kind'].most_common():
        print('              %-12s %d' % (KINDS[kind][2], count))
    print('Durum       %s' % ', '.join('%s %d' % (k, v) for k, v in data['by_status'].most_common()))
    print('Ham kayıt   %d yakalanmış, %d işlenmemiş' % (len(data['raw']), len(data['pending'])))
    print('Röportaj    %d oturum, bankadaki %d sorunun %d tanesi cevaplandı'
          % (len(data['sessions']), len(data['bank']), len(data['answered'])))
    print('Hacim       %d kelime' % data['words'])
    if data['fidelity']['count']:
        print('Sadakat     genel %%%s, son 10 %%%s (%d prova)'
              % (data['fidelity']['overall'], data['fidelity']['recent'], data['fidelity']['count']))
    else:
        print('Sadakat     henüz prova yok')
    print('Alanlar     %s' % ', '.join('%s %d' % (d, c) for d, c in data['coverage'].most_common(8)))
    return 0


def cmd_export(args):
    store = home()
    target = Path(args.to).expanduser()
    target.mkdir(parents=True, exist_ok=True)
    if store.exists():
        shutil.copytree(store, target / 'private', dirs_exist_ok=True)
    for asset in (BANK_PATH, PROTOCOL, ASSETS / 'README.md'):
        if asset.exists():
            destination = target / 'mind' / asset.relative_to(ASSETS)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(asset, destination)
    script = REPO_ROOT / 'workflow' / 'mind.py'
    destination = target / 'workflow' / script.name
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(script, destination)
    print('Kopyalandı: %s' % target)
    print('')
    print('Orada kullanmak için:')
    print('  export MIND_HOME=%s' % (target / 'private'))
    print('  python3 %s/workflow/mind.py stats' % target)
    print('')
    print('Özel bir repoya koyacaksan private/ klasörünü commitle, burada kalan kopyayı sil.')
    return 0


def main():
    parser = argparse.ArgumentParser(description='Beyin klonu: bildiğini dışarı çıkar, büyüt.')
    sub = parser.add_subparsers(dest='command')

    p = sub.add_parser('init', help='klon deposunu kur')
    p.add_argument('--from-repo', action='store_true',
                   help='bu iş reposunun kayıtlarından varsayım tohumları çıkar')
    p.add_argument('--reseed', action='store_true', help='dolu depoya tohumları tekrar yaz')
    p.set_defaults(func=cmd_init)

    p = sub.add_parser('capture', help='aklına geleni ham haliyle kutuya at')
    p.add_argument('text', nargs='*')
    p.add_argument('--tag', default='', help='kısa etiket')
    p.set_defaults(func=cmd_capture)

    p = sub.add_parser('interview', help='sıradaki en verimli soruları oturum dosyasına yaz')
    p.add_argument('--n', type=int, default=8)
    p.add_argument('--domain', help='tek bir alana odaklan')
    p.set_defaults(func=cmd_interview)

    p = sub.add_parser('distill', help='ham kayıtları modele çevirmek için paketi bas')
    p.add_argument('--done', nargs='+', help='bu ham kayıtları işlenmiş say')
    p.add_argument('--done-all', action='store_true', help='bekleyen her şeyi işlenmiş say')
    p.set_defaults(func=cmd_distill)

    p = sub.add_parser('add', help='modele tek bir girdi yaz')
    p.add_argument('--kind', required=True, choices=list(KINDS))
    p.add_argument('--title', required=True)
    p.add_argument('--alan', default='')
    p.add_argument('--guven', default='orta', choices=list(CONFIDENCE))
    p.add_argument('--durum', default='onaylı', choices=list(STATUSES))
    p.add_argument('--kaynak', default='')
    p.add_argument('--note', default='')
    p.set_defaults(func=cmd_add)

    p = sub.add_parser('confirm', help='bir girdinin durumunu değiştir')
    p.add_argument('id')
    p.add_argument('--durum', default='onaylı', choices=list(STATUSES))
    p.add_argument('--note', default='')
    p.set_defaults(func=cmd_confirm)

    p = sub.add_parser('addq', help='bankaya kendi sorunu ekle')
    p.add_argument('text', nargs='+')
    p.add_argument('--domain', default='kendi')
    p.add_argument('--priority', default='P1', choices=['P1', 'P2', 'P3'])
    p.set_defaults(func=cmd_addq)

    p = sub.add_parser('ask', help='klon bu konuda ne tutuyor')
    p.add_argument('query', nargs='+')
    p.add_argument('--limit', type=int, default=6)
    p.set_defaults(func=cmd_ask)

    p = sub.add_parser('rehearse', help='klon senin yerine cevaplasın, sonra düzelt')
    p.add_argument('--question', nargs='*')
    p.set_defaults(func=cmd_rehearse)

    p = sub.add_parser('grade', help='provayı notlandır')
    p.add_argument('id')
    p.add_argument('--verdict', required=True, choices=list(VERDICTS))
    p.add_argument('--note', default='')
    p.set_defaults(func=cmd_grade)

    sub.add_parser('fidelity', help='klon sana ne kadar benziyor').set_defaults(func=cmd_fidelity)

    p = sub.add_parser('gaps', help='eksikler ve sıradaki sorular')
    p.add_argument('--limit', type=int, default=10)
    p.set_defaults(func=cmd_gaps)

    p = sub.add_parser('digest', help='son N günde ne oldu')
    p.add_argument('--days', type=int, default=7)
    p.add_argument('--limit', type=int, default=12)
    p.set_defaults(func=cmd_digest)

    p = sub.add_parser('check', help='klonun bütünlüğü')
    p.add_argument('--quiet', action='store_true')
    p.set_defaults(func=cmd_check)

    sub.add_parser('stats', help='klon ne kadar büyüdü').set_defaults(func=cmd_stats)

    p = sub.add_parser('export', help='klonu başka bir yere taşı')
    p.add_argument('--to', required=True)
    p.set_defaults(func=cmd_export)

    args = parser.parse_args()
    if not getattr(args, 'func', None):
        parser.print_help()
        return 2
    try:
        return args.func(args)
    except BrokenPipeError:
        # Piped into head or less. Not an error, just a reader who stopped.
        try:
            sys.stdout.close()
        except BrokenPipeError:
            pass
        return 0


if __name__ == '__main__':
    sys.exit(main())
