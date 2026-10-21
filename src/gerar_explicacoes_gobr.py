from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import List, Dict, Tuple

DECL_RE = re.compile(r'^(time|carteira|segmentacao|parametros)\s+"(.*)"\s*:\s*$', re.I)

FREQ_FIXED = {
    'diaria()': 'diariamente (a cada 1 dia)',
    'semanal()': 'semanalmente (a cada 7 dias)',
    'quinzenal()': 'quinzenalmente (a cada 15 dias)',
    'mensal()': 'mensalmente (a cada 30 dias)',
    'bimestral()': 'a cada 2 meses (60 dias)',
    'trimestral()': 'a cada 3 meses (90 dias)',
    'semestral()': 'a cada 6 meses (180 dias)',
    'anual()': 'anualmente (a cada 365 dias)',
}


def strip_accents(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def canon(s: str) -> str:
    return strip_accents(s.lower()).strip()


def quoted_values(s: str) -> List[str]:
    return re.findall(r'"([^"]+)"', s)


def join_multiline_clauses(lines: List[str]) -> List[str]:
    """Join DSL clauses split across lines because of long function arguments or preference blocks."""
    out: List[str] = []
    buf = ''
    parens = 0
    for raw in lines:
        if not raw.strip() or raw.lstrip().startswith('#'):
            continue
        s = raw.strip()
        if not buf:
            buf = s
            parens = s.count('(') - s.count(')')
            # preference on a line by itself is continued on next line(s)
            if canon(s) == 'preferencia':
                parens = 999
                continue
            if parens <= 0:
                out.append(buf)
                buf = ''
        else:
            # if we were in a 'preferencia' multiline block, continue while next line looks like preference continuation
            if parens == 999:
                c = canon(s)
                if c.startswith(('maior ', 'menor ', 'normal ', 'na ', 'no ', 'e ')):
                    buf += ' ' + s
                    # preference continuation normally ends when line doesn't end in 'e'; but DSL often uses 'e' prefix.
                    # We cannot know next line here, so defer until a clear new clause arrives.
                    continue
                else:
                    out.append(buf)
                    buf = s
                    parens = s.count('(') - s.count(')')
                    if parens <= 0:
                        out.append(buf)
                        buf = ''
                    continue
            buf += ' ' + s
            parens += s.count('(') - s.count(')')
            if parens <= 0:
                out.append(buf)
                buf = ''
    if buf:
        out.append(buf)
    # Some fallback expressions are wrapped onto a continuation line starting with 'ou'.
    merged = []
    for item in out:
        if canon(item).startswith('ou ') and merged:
            merged[-1] = merged[-1] + ' ' + item
        else:
            merged.append(item)
    return merged


def parse_blocks(text: str) -> List[Dict]:
    blocks = []
    current = None
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith('#') or canon(raw.strip()).startswith('version '):
            continue
        # declarations are at top-level in these files
        m = DECL_RE.match(raw.strip())
        if m:
            if current:
                current['clauses'] = join_multiline_clauses(current['raw_lines'])
                blocks.append(current)
            current = {'type': canon(m.group(1)), 'name': m.group(2), 'raw_lines': [], 'raw_header': raw.strip()}
        elif current:
            current['raw_lines'].append(raw)
    if current:
        current['clauses'] = join_multiline_clauses(current['raw_lines'])
        blocks.append(current)
    return blocks


def humanize_target(clause: str) -> str:
    c = canon(clause)
    vals = quoted_values(clause)
    names = ', '.join(f'“{v}”' for v in vals)
    if c.startswith('do time'):
        return f'clientes vinculados ao time {names}' if vals else 'clientes vinculados ao time indicado'
    if c.startswith('da carteira'):
        return f'clientes da carteira {names}' if vals else 'clientes da carteira indicada'
    if c.startswith('da segmentacao'):
        return f'clientes da segmentação {names}' if vals else 'clientes da segmentação indicada'
    return clause


def humanize_condition_fragment(fragment: str) -> str:
    s = fragment.strip().rstrip('.')
    c = canon(s)
    # remove connective prefix only; caller handles joining
    if c.startswith('quando '):
        s = s[len(s.split()[0]):].strip()
        c = canon(s)
    elif c.startswith('e '):
        s = s[2:].strip()
        c = canon(s)

    # common semantic transforms, ordered from specific to generic
    m = re.fullmatch(r'recencia de positivacao global entre (\d+) dias? e (\d+) dias?', c)
    if m:
        return f'com a última compra/positivação na empresa entre {m.group(1)} e {m.group(2)} dias atrás'
    m = re.fullmatch(r'recencia de positivacao global em (\d+) dias?', c)
    if m:
        return f'com a última compra/positivação na empresa nos últimos {m.group(1)} dias'
    m = re.fullmatch(r'fora da recencia de positivacao global entre (\d+) dias? e (\d+) dias?', c)
    if m:
        return f'cuja última compra/positivação na empresa está fora do intervalo de {m.group(1)} a {m.group(2)} dias atrás'
    m = re.fullmatch(r'fora da recencia de positivacao global em (\d+) dias?', c)
    if m:
        return f'sem compra/positivação na empresa nos últimos {m.group(1)} dias'

    m = re.fullmatch(r'recencia de positivacao do vendedor entre (\d+) dias? e (\d+) dias?', c)
    if m:
        return f'com a última compra/positivação com o vendedor entre {m.group(1)} e {m.group(2)} dias atrás'
    m = re.fullmatch(r'recencia de positivacao do vendedor em (\d+) dias?', c)
    if m:
        return f'com a última compra/positivação com o vendedor nos últimos {m.group(1)} dias'
    m = re.fullmatch(r'fora da recencia de positivacao do vendedor entre (\d+) dias? e (\d+) dias?', c)
    if m:
        return f'cuja última compra/positivação com o vendedor está fora do intervalo de {m.group(1)} a {m.group(2)} dias atrás'
    m = re.fullmatch(r'fora da recencia de positivacao do vendedor em (\d+) dias?', c)
    if m:
        return f'sem compra/positivação com o vendedor nos últimos {m.group(1)} dias'

    m = re.fullmatch(r'recencia de positivacao entre (\d+) dias? e (\d+) dias?', c)
    if m:
        return f'com a última compra/positivação entre {m.group(1)} e {m.group(2)} dias atrás'
    m = re.fullmatch(r'recencia de positivacao em (\d+) dias?', c)
    if m:
        return f'com a última compra/positivação nos últimos {m.group(1)} dias'
    m = re.fullmatch(r'fora da recencia de positivacao entre (\d+) dias? e (\d+) dias?', c)
    if m:
        return f'cuja última compra/positivação está fora do intervalo de {m.group(1)} a {m.group(2)} dias atrás'
    m = re.fullmatch(r'fora da recencia de positivacao em (\d+) dias?', c)
    if m:
        return f'sem compra/positivação nos últimos {m.group(1)} dias'

    replacements = [
        ('status na receita federal definido como baixada', 'com status “baixada” na Receita Federal'),
        ('no ciclo de vida prospect com a empresa', 'com ciclo de vida Prospect na empresa'),
        ('no ciclo de vida ativo com a empresa', 'com ciclo de vida Ativo na empresa'),
        ('no ciclo de vida inativo com a empresa', 'com ciclo de vida Inativo na empresa'),
        ('no ciclo de vida prospect com o vendedor', 'com ciclo de vida Prospect para o vendedor'),
        ('ativos para o vendedor', 'ativos para o vendedor'),
        ('ativos para a empresa', 'ativos para a empresa'),
        ('inativos para o vendedor', 'inativos para o vendedor'),
        ('inativos para a empresa', 'inativos para a empresa'),
        ('sem venda ou prospects', 'que nunca compraram (sem venda/prospects)'),
        ('sem vendas', 'sem vendas'),
        ('sem venda', 'sem venda'),
        ('inadimplentes', 'inadimplentes'),
        ('adimplentes', 'adimplentes'),
        ('pessoa juridica', 'pessoa jurídica'),
        ('pessoa fisica', 'pessoa física'),
        ('cliente filial', 'que são filiais'),
        ('e o cliente filial', 'que são filiais'),
        ('é o cliente filial', 'que são filiais'),
        ('bloqueados', 'bloqueados'),
    ]
    for a, b in replacements:
        if c == a:
            return b

    # generic readable rewrites
    t = s
    t = re.sub(r'\bramo de atividade igual\s*\(', 'dos ramos de atividade (', t, flags=re.I)
    t = re.sub(r'\bramo de atividade diferente\s*\(', 'fora dos ramos de atividade (', t, flags=re.I)
    t = re.sub(r'\bnome da cidade igual\s*\(', 'localizados nas cidades (', t, flags=re.I)
    t = re.sub(r'\bnome do bairro igual\s*\(', 'localizados nos bairros (', t, flags=re.I)
    t = re.sub(r'\buf do estado igual\s*\(', 'localizados nos estados/UF (', t, flags=re.I)
    t = re.sub(r'\bcodigo da rota igual\s*\(', 'das rotas de código (', t, flags=re.I)
    t = re.sub(r'\bo rotulo contem\s*\(', 'cujo rótulo contém (', t, flags=re.I)
    t = re.sub(r'\bcnae [ée] igual\s*\(', 'com CNAE (', t, flags=re.I)
    t = re.sub(r'\bcurva ([abc]) com a empresa\b', lambda m: f'classificados na curva {m.group(1).upper()} com a empresa', t, flags=re.I)
    t = re.sub(r'\brecencia de visita\b', 'recência de visita', t, flags=re.I)
    t = re.sub(r'\brecencia de positivacao\b', 'recência de compra/positivação', t, flags=re.I)
    t = re.sub(r'\bfrequencia historica\b', 'frequência histórica', t, flags=re.I)
    t = re.sub(r'\bmedia faturada\b', 'média faturada', t, flags=re.I)
    t = re.sub(r'\bnao tem credito\b', 'sem crédito disponível', t, flags=re.I)
    t = re.sub(r'\btem credito\b', 'com crédito disponível', t, flags=re.I)
    t = re.sub(r'\bcadastrado faz (\d+) dias?\b', r'cadastrados há \1 dias', t, flags=re.I)
    return t.strip()


def humanize_frequency(rest: str) -> str:
    r = rest.strip()
    c = canon(r)
    m = re.fullmatch(r'de (\d+) dias?', c)
    if m:
        return f'atender a cada {m.group(1)} dias'
    m = re.fullmatch(r'de (\d+) dia', c)
    if m:
        return f'atender a cada {m.group(1)} dia'
    if c in FREQ_FIXED:
        return f'atender {FREQ_FIXED[c]}'
    # pivot-date variants
    for key, label in [('quinzenal', 'a cada 15 dias'), ('bimestral', 'a cada 60 dias')]:
        m = re.fullmatch(rf'{key}\(([^)]+)\)', c)
        if m:
            return f'atender {label}, usando a data pivot informada'
    if c == 'do vendedor':
        return 'usar a frequência configurada pelo próprio vendedor para o cliente'
    if c == 'do historico':
        return 'usar a frequência calculada com base no histórico'
    if c == 'de qualquer vendedor':
        return 'usar a frequência configurada por qualquer vendedor para o cliente'
    if c == 'de ativos da empresa':
        return 'usar a frequência média dos clientes ativos da empresa'
    if c == 'de inativos da empresa':
        return 'usar a frequência média dos clientes inativos da empresa'
    if c == 'de ativos do vendedor':
        return 'usar a frequência média dos clientes ativos do vendedor'
    if c == 'de inativos do vendedor':
        return 'usar a frequência média dos clientes inativos do vendedor'
    if c == 'do govendas':
        return 'usar a frequência padrão do Govendas'
    if c == 'remover':
        return 'remover a configuração de frequência existente'
    # fallback chains and limits: keep semantics close to DSL while cleaning accents
    t = r
    t = re.sub(r'\bdo historico\b', 'do histórico', t, flags=re.I)
    t = re.sub(r'\bno minimo\b', 'no mínimo', t, flags=re.I)
    t = re.sub(r'\bno maximo\b', 'no máximo', t, flags=re.I)
    return f'aplicar frequência {t}'


def humanize_preference(clause: str) -> str:
    # clause begins with preferencia/preferência
    r = re.sub(r'^prefer[eê]ncia\s*', '', clause.strip(), flags=re.I).strip()
    c = canon(r)
    if c == 'nos dias uteis':
        return 'dar preferência de atendimento aos dias úteis (segunda a sexta-feira)'
    if c == 'nos dias uteis e no sabado':
        return 'dar preferência de atendimento aos dias úteis e ao sábado'
    if c == 'do vendedor':
        return 'usar a preferência de dias configurada pelo vendedor'
    if c.startswith('do historico'):
        t = re.sub(r'\bhistorico\b', 'histórico', r, flags=re.I)
        return f'usar a preferência de dias {t}'
    if r:
        # normalize day accents lightly
        t = r.replace('terca', 'terça').replace('sabado', 'sábado').replace('uteis', 'úteis')
        return f'definir preferência de atendimento {t}'
    return 'definir preferência de dias conforme as opções seguintes'


def classify_clause(clause: str) -> str:
    c = canon(clause)
    if c.startswith(('do time', 'da carteira', 'da segmentacao')):
        return 'target'
    if c.startswith(('frequencia ', 'frequência ')):
        return 'action'
    if c.startswith(('preferencia', 'preferência')):
        return 'action'
    if c in ('nao agendar', 'não agendar', 'fixo', 'roteirizavel', 'nao roteirizavel', 'não roteirizavel'):
        return 'action'
    if c.startswith(('sem choque', 'restrito ')):
        return 'action'
    if c.startswith(('quando ', 'e ')):
        return 'condition'
    # temporal clauses typically start with these and occur outside when
    if c.startswith(('no dia ', 'antes do dia ', 'depois do dia ', 'a partir do dia ', 'entre os dias ',
                     'na segunda', 'na terca', 'na terça', 'na quarta', 'na quinta', 'na sexta', 'no sabado',
                     'no domingo', 'todos os dias', 'nos dias uteis', 'no fim de semana', 'na primeira semana',
                     'na segunda semana', 'na terceira semana', 'na quarta semana', 'na ultima semana',
                     'na primeira quinzena', 'na segunda quinzena', 'em janeiro', 'em fevereiro', 'em marco',
                     'em março', 'em abril', 'em maio', 'em junho', 'em julho', 'em agosto', 'em setembro',
                     'em outubro', 'em novembro', 'em dezembro', 'no primeiro ', 'no segundo ', 'no terceiro ',
                     'no quarto ', 'no quinto ', 'no sexto ')):
        return 'temporal'
    return 'other'


def humanize_action(clause: str) -> str:
    c = canon(clause)
    if c.startswith('frequencia '):
        rest = re.sub(r'^frequ[eê]ncia\s+', '', clause.strip(), flags=re.I)
        return humanize_frequency(rest)
    if c.startswith('preferencia'):
        return humanize_preference(clause)
    if c in ('nao agendar', 'não agendar'):
        return 'não agendar esses clientes'
    if c == 'fixo':
        return 'marcar a parametrização como fixa'
    if c == 'roteirizavel':
        return 'marcar os clientes como roteirizáveis'
    if c in ('nao roteirizavel', 'não roteirizavel'):
        return 'marcar os clientes como não roteirizáveis'
    if c.startswith('sem choque'):
        t = re.sub(r'^sem choque\s*', '', clause.strip(), flags=re.I)
        return f'evitar choque/conflito de atendimento {t}'.strip()
    if c.startswith('restrito '):
        return f'restringir o agendamento {clause.strip()[len("restrito "):]}'.strip()
    return clause.strip()


def humanize_temporal(clause: str) -> str:
    t = clause.strip()
    t = t.replace('uteis', 'úteis').replace('terca', 'terça').replace('sabado', 'sábado').replace('marco', 'março')
    return t


def build_record(file_name: str, idx: int, block: Dict) -> Dict:
    clauses = block['clauses']
    targets, conditions, actions, temporals, others = [], [], [], [], []
    for cl in clauses:
        typ = classify_clause(cl)
        if typ == 'target': targets.append(cl)
        elif typ == 'condition': conditions.append(cl)
        elif typ == 'action': actions.append(cl)
        elif typ == 'temporal': temporals.append(cl)
        else: others.append(cl)

    target_texts = [humanize_target(x) for x in targets]
    cond_texts = [humanize_condition_fragment(x) for x in conditions]
    action_texts = [humanize_action(x) for x in actions]
    temporal_texts = [humanize_temporal(x) for x in temporals]

    # Keep unclassified content visible, rather than silently dropping it.
    if others:
        cond_texts.extend([x.strip() for x in others])

    if target_texts:
        subject = ' e '.join(target_texts)
    else:
        subject = 'clientes abrangidos pela parametrização'

    if cond_texts:
        # Preserve conjunction semantics while making a readable sentence.
        cond_phrase = '; e '.join(cond_texts)
        base = f'Para {subject}, considerar clientes {cond_phrase}.'
    else:
        base = f'Aplicar a regra a {subject}.'

    if temporal_texts:
        base += ' A parametrização é aplicada somente ' + ', '.join(temporal_texts) + '.'

    if action_texts:
        base += ' Ação: ' + '; '.join(action_texts) + '.'
    else:
        base += ' A parametrização não contém uma ação operacional reconhecida pelo gerador; revisar o bloco original.'

    # A shorter embedding-friendly explanation.
    pieces = []
    if cond_texts:
        pieces.append('Clientes ' + '; e '.join(cond_texts))
    else:
        pieces.append(subject.capitalize())
    if action_texts:
        pieces.append('devem ' + '; '.join(action_texts))
    short = '. '.join(pieces).rstrip('.') + '.'

    raw_block = block['raw_header'] + '\n' + '\n'.join(x.rstrip() for x in block['raw_lines'])
    problems = []
    # Basic source-quality checks. We report; we do not repair source rules.
    balance = sum(line.count('(') - line.count(')') for line in block['raw_lines'])
    if balance != 0:
        problems.append(f'parênteses desbalanceados no bloco (saldo {balance})')
    if not action_texts:
        problems.append('nenhuma ação de parametrização reconhecida')
    if others:
        problems.append('há cláusulas não classificadas automaticamente')
    status = 'revisao_necessaria' if problems else 'ok'
    embedding_text = f"{block['name']}. {short}"
    if target_texts:
        embedding_text += ' Alvo: ' + '; '.join(target_texts) + '.'

    return {
        'id': f'{Path(file_name).stem}__param_{idx:03d}',
        'arquivo': file_name,
        'ordem_no_arquivo': idx,
        'tipo': 'parametros',
        'nome_regra': block['name'],
        'alvo': target_texts,
        'filtros_temporais': temporal_texts,
        'condicoes': cond_texts,
        'acoes': action_texts,
        'explicacao_curta': short,
        'explicacao_detalhada': base,
        'texto_embedding': embedding_text,
        'status_validacao': status,
        'problemas_validacao': problems,
        'dsl_original': raw_block,
        'clausulas_nao_classificadas': others,
    }


def generate(input_dir: Path, out_jsonl: Path, out_md: Path) -> Tuple[int, int, int]:
    records = []
    file_count = 0
    unclassified_count = 0
    for f in sorted(input_dir.glob('*.gobr')):
        file_count += 1
        text = f.read_text(encoding='utf-8', errors='replace')
        blocks = parse_blocks(text)
        pidx = 0
        for b in blocks:
            if b['type'] != 'parametros':
                continue
            pidx += 1
            rec = build_record(f.name, pidx, b)
            unclassified_count += len(rec['clausulas_nao_classificadas'])
            records.append(rec)

    with out_jsonl.open('w', encoding='utf-8') as w:
        for rec in records:
            w.write(json.dumps(rec, ensure_ascii=False) + '\n')

    by_file: Dict[str, List[Dict]] = {}
    for r in records:
        by_file.setdefault(r['arquivo'], []).append(r)

    with out_md.open('w', encoding='utf-8') as w:
        w.write('# Explicações de regras de negócio geradas a partir das parametrizações GoBR\n\n')
        w.write(f'- Arquivos `.gobr` processados: **{file_count}**\n')
        w.write(f'- Blocos `parametros` convertidos: **{len(records)}**\n')
        w.write(f'- Cláusulas não classificadas automaticamente: **{unclassified_count}**\n\n')
        w.write('> Cada explicação mantém o bloco GoBR original no JSONL para rastreabilidade. O Markdown agrupa as explicações por arquivo.\n\n')
        for fname in sorted(by_file):
            w.write(f'## {fname}\n\n')
            for r in by_file[fname]:
                w.write(f'### {r["nome_regra"]}\n\n')
                w.write(r['explicacao_detalhada'] + '\n\n')

    return file_count, len(records), unclassified_count


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='Gera explicações em linguagem de negócio a partir de parametrizações GoBR.')
    ap.add_argument('input_dir', type=Path, help='Diretório com arquivos .gobr')
    ap.add_argument('--jsonl', type=Path, default=Path('parametrizacoes_explicadas.jsonl'))
    ap.add_argument('--md', type=Path, default=Path('parametrizacoes_explicadas.md'))
    ap.add_argument('--embeddings-jsonl', type=Path, default=None, help='Saída enxuta pronta para indexação vetorial')
    args = ap.parse_args()
    fc, rc, uc = generate(args.input_dir, args.jsonl, args.md)
    if args.embeddings_jsonl:
        with args.embeddings_jsonl.open('w', encoding='utf-8') as out:
            with args.jsonl.open(encoding='utf-8') as src:
                for line in src:
                    rec = json.loads(line)
                    slim = {
                        'id': rec['id'],
                        'arquivo': rec['arquivo'],
                        'ordem_no_arquivo': rec['ordem_no_arquivo'],
                        'nome_regra': rec['nome_regra'],
                        'texto': rec['texto_embedding'],
                        'status_validacao': rec['status_validacao'],
                    }
                    out.write(json.dumps(slim, ensure_ascii=False) + '\n')
    print(f'Processados {fc} arquivos; geradas {rc} explicações; {uc} cláusulas não classificadas.')
