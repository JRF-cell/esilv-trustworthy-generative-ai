"""Construit les deux tableaux TD1 à partir des 103 traces réelles.
Placer ce script dans kit-td1, puis: python3 build_td1_comparisons.py
N'efface ni les traces brutes ni les champs bibliographiques déjà remplis.
"""
import csv
from collections import defaultdict
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parent
INPUT_FILES = [
    'traces-A-new.csv', 'traces-B.csv', 'traces-C.csv',
    'traces-D.csv', 'traces-E.csv',
]
COMPARE = ROOT / 'model-question-comparison-en.csv'
SUMMARY = ROOT / 'five-model-summary-en.csv'
COMPARE_COLUMNS = [
    'case_id', 'model_id', 'trace_file', 'cell_id', 'nature',
    'status', 'value_cents', 'reference_cents', 'explanation',
]
SUMMARY_COLUMNS = [
    'provider', 'model_id', 'public_index', 'index_date', 'index_source',
    'paid_route_same_model', 'input_usd_per_million',
    'output_usd_per_million', 'price_date', 'price_source', 'access_used',
    'period_results', 'age_results', 'product_results',
    'combined_results', 'trace_files', 'limits',
]


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_csv(path, columns, rows):
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)


def model_key(row):
    return f"{row['provider']}:{row['model_requested']}"


# Les types sont ceux du fichier de questions officiel (et non inférés au hasard).
import json
with (ROOT / 'questions-td1.json').open(encoding='utf-8') as f:
    question_doc = json.load(f)
questions = question_doc['questions']
case_ids = [q['id'] for q in questions]
assert len(case_ids) == 20 and len(set(case_ids)) == 20, '20 questions distinctes attendues'
family = {}
for q in questions:
    typ = q['type']
    if ' + ' in typ:
        family[q['id']] = 'combined'
    elif typ == 'period':
        family[q['id']] = 'period'
    elif typ.startswith('age '):
        family[q['id']] = 'age'
    elif typ == 'product list':
        family[q['id']] = 'product'
    else:
        raise ValueError(f"Famille inconnue pour {q['id']}: {typ}")

reference_rows = read_csv(ROOT / 'reference-td1.csv')
references = {r['case_id']: r.get('revenue_cents', '') for r in reference_rows}

trace_rows = read_csv(ROOT / 'traces-td1.csv')
if not trace_rows:
    raise ValueError('traces-td1.csv est vide')
models = {}
for name in INPUT_FILES:
    source_rows = read_csv(ROOT / name)
    if not source_rows:
        raise ValueError(f'{name} est vide')
    keys = {model_key(r) for r in source_rows}
    if len(keys) != 1:
        raise ValueError(f'{name} doit contenir un seul modèle : {keys}')
    key = keys.pop()
    if key in models:
        raise ValueError(f'Modèle dupliqué : {key}')
    models[key] = {'source': name, 'rows': source_rows}

# Exiger le même nombre de tentatives, par modèle et question,
# dans la fusion et dans les fichiers de traces originaux.
def signature(rows):
    counts = defaultdict(int)
    for row in rows:
        counts[(model_key(row), row['case_id'])] += 1
    return dict(counts)

source_rows = [r for m in models.values() for r in m['rows']]
if signature(source_rows) != signature(trace_rows):
    raise ValueError('La fusion ne correspond pas aux fichiers sources. Relancer merge_traces.py')
if len(models) != 5:
    raise ValueError(f'5 modèles attendus, trouvé {len(models)}')

# Dernière tentative (dans l'ordre réel du fichier), jamais la meilleure.
last_by_cell = {}
for row in trace_rows:
    if row['case_id'] not in case_ids:
        raise ValueError(f"Question inconnue: {row['case_id']}")
    last_by_cell[(model_key(row), row['case_id'])] = row

# Préserver les commentaires que le groupe a déjà écrits.
existing_comparison = {}
if COMPARE.exists():
    for old in read_csv(COMPARE):
        if old.get('case_id') and old.get('model_id'):
            existing_comparison[(old['model_id'], old['case_id'])] = old


def explanation(row):
    if row is None:
        return 'No trace: this question was not executed.'
    verdict = row['verdict']
    if verdict == 'correct':
        return ''
    detail = (row.get('verdict_detail') or '').strip()
    error = (row.get('error') or '').strip()
    if verdict == 'incorrect':
        return (f"Wrong result: got {row.get('value')}, expected {row.get('reference')}. "
                'REVIEW: identify the actual SQL mistake in the raw trace.')
    if verdict == 'sql_rejected':
        return f'SQL rejected by validator. {detail} {error}'.strip()[:450]
    if verdict == 'not_executed':
        return (f'No executable result. {error or detail or "Unknown reason"}')[:450]
    return f'Non-correct verdict: {verdict}. {detail} {error}'.strip()[:450]

comparison_rows = []
for key, model in models.items():
    for case in case_ids:
        last = last_by_cell.get((key, case))
        old = existing_comparison.get((key, case), {})
        comparison_rows.append({
            'case_id': case,
            'model_id': key,
            'trace_file': model['source'],
            'cell_id': last.get('cell_id', f'{key}:{case}') if last else f'{key}:{case}',
            'nature': last.get('nature', 'real') if last else 'real',
            'status': last['verdict'] if last else 'not_executed',
            'value_cents': last.get('value', '') if last else '',
            'reference_cents': (last.get('reference') or references.get(case, '')) if last else references.get(case, ''),
            'explanation': old.get('explanation', '').strip() or explanation(last),
        })
write_csv(COMPARE, COMPARE_COLUMNS, comparison_rows)

# Ne pas écraser les infos d'indice/prix déjà documentées dans le modèle.
existing_summary = {}
if SUMMARY.exists():
    for r in read_csv(SUMMARY):
        if r.get('provider') and r.get('model_id'):
            existing_summary[(r['provider'], r['model_id'])] = r

summary_rows = []
for key, model in models.items():
    provider, model_id = key.split(':', 1)
    row = dict(existing_summary.get((provider, model_id), {}))
    row['provider'] = provider
    row['model_id'] = model_id
    row['trace_files'] = model['source']
    row['access_used'] = row.get('access_used') or (
        'Groq Free API' if provider == 'groq' else 'OpenRouter Free API'
    )
    model_comparison = [r for r in comparison_rows if r['model_id'] == key]
    for fam in ('period', 'age', 'product', 'combined'):
        matches = [r for r in model_comparison if family[r['case_id']] == fam]
        ok = sum(r['status'] == 'correct' for r in matches)
        row[f'{fam}_results'] = f'{ok}/{len(matches)} correct ({100 * ok / len(matches):.1f}%)'
    failed_requests = sum(
        r['verdict'] == 'not_executed' for r in model['rows']
    )
    rate_limits = sum('429' in (r.get('error') or '') for r in model['rows'])
    rejected = sum(r['status'] == 'sql_rejected' for r in model_comparison)
    row['limits'] = (
        f'{failed_requests} failed attempt(s), including {rate_limits} HTTP 429; '
        f'{rejected} final SQL rejection(s); real calls only.'
    )
    summary_rows.append(row)
write_csv(SUMMARY, SUMMARY_COLUMNS, summary_rows)

# Vérifier que le prompt est identique pour chaque question sur les 5 modèles.
fingerprints = defaultdict(set)
for row in trace_rows:
    if row.get('prompt_sha256'):
        fingerprints[row['case_id']].add(row['prompt_sha256'])
mismatches = [case for case, fps in fingerprints.items() if len(fps) != 1]
if mismatches:
    print('ATTENTION: empreintes de prompt différentes:', ', '.join(sorted(mismatches)))

print(f'OK: {len(trace_rows)} traces brutes conservées dans traces-td1.csv')
print(f'OK: {len(comparison_rows)} lignes dans {COMPARE.name}')
print(f'OK: {len(summary_rows)} modèles dans {SUMMARY.name}')
print('\nScores finaux:')
for key, model in models.items():
    finals = [r for r in comparison_rows if r['model_id'] == key]
    ok = sum(r['status'] == 'correct' for r in finals)
    durations = []
    for r in finals:
        raw = last_by_cell.get((key, r['case_id']))
        if raw and raw.get('latency_ms'):
            try:
                durations.append(float(raw['latency_ms']))
            except ValueError:
                pass
    t = f'{median(durations):.0f} ms (médiane)' if durations else 'temps indisponible'
    print(f'  {key}: {ok}/20 ({ok * 5} %); {t}')
print('\nA compléter manuellement dans five-model-summary-en.csv:')
print('public_index, index_date, index_source, paid_route_same_model,')
print('input_usd_per_million, output_usd_per_million, price_date, price_source.')
print('A vérifier manuellement dans model-question-comparison-en.csv:')
print('les causes précises des erreurs indiquées REVIEW.')
