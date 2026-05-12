const sampleRows = [
  {
    target: '1.1.1.1',
    ok: true,
    sent: 3,
    received: 3,
    packet_loss: 0,
    min_ms: 12.4,
    avg_ms: 13.1,
    max_ms: 14.2,
    jitter_ms: 0.74,
    started_at: '2026-05-12T17:21:07Z',
  },
  {
    target: 'github.com',
    ok: true,
    sent: 3,
    received: 3,
    packet_loss: 0,
    min_ms: 28.8,
    avg_ms: 31.6,
    max_ms: 36.4,
    jitter_ms: 3.16,
    started_at: '2026-05-12T17:21:07Z',
  },
  {
    target: 'example.invalid',
    ok: false,
    sent: 3,
    received: 0,
    packet_loss: null,
    min_ms: null,
    avg_ms: null,
    max_ms: null,
    jitter_ms: null,
    started_at: '2026-05-12T17:21:07Z',
    error: 'Name or service not known',
  },
];

const h = React.createElement;

function formatMs(value) {
  if (value === null || value === undefined) return '-';
  return `${value}ms`;
}

function formatLoss(value) {
  if (value === null || value === undefined) return '-';
  return `${value}%`;
}

function getSummary(rows) {
  const online = rows.filter((row) => row.ok).length;
  const failed = rows.length - online;
  const avgValues = rows.map((row) => row.avg_ms).filter((value) => typeof value === 'number');
  const avgLatency = avgValues.length
    ? Math.round((avgValues.reduce((total, value) => total + value, 0) / avgValues.length) * 100) / 100
    : null;
  const worst = rows
    .filter((row) => typeof row.avg_ms === 'number')
    .sort((a, b) => b.avg_ms - a.avg_ms)[0];

  return { online, failed, avgLatency, worst };
}

function StatusPill({ ok }) {
  return h('span', { className: `status-pill ${ok ? 'is-ok' : 'is-fail'}` }, ok ? 'online' : 'falhou');
}

function MetricCard({ label, value, detail }) {
  return h(
    'article',
    { className: 'metric-card' },
    h('span', null, label),
    h('strong', null, value),
    detail ? h('small', null, detail) : null,
  );
}

function ResultTable({ rows }) {
  return h(
    'div',
    { className: 'table-wrap' },
    h(
      'table',
      null,
      h(
        'thead',
        null,
        h(
          'tr',
          null,
          ['alvo', 'status', 'recv', 'loss', 'avg', 'jitter'].map((label) => h('th', { key: label }, label)),
        ),
      ),
      h(
        'tbody',
        null,
        rows.map((row) =>
          h(
            'tr',
            { key: `${row.target}-${row.started_at}` },
            h('td', null, row.target),
            h('td', null, h(StatusPill, { ok: row.ok })),
            h('td', null, `${row.received ?? 0}/${row.sent ?? '-'}`),
            h('td', null, formatLoss(row.packet_loss)),
            h('td', null, formatMs(row.avg_ms)),
            h('td', null, formatMs(row.jitter_ms)),
          ),
        ),
      ),
    ),
  );
}

function App() {
  const [rows, setRows] = React.useState(sampleRows);
  const [error, setError] = React.useState('');
  const summary = React.useMemo(() => getSummary(rows), [rows]);

  function loadFile(event) {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
      try {
        const parsed = JSON.parse(String(reader.result));
        if (!Array.isArray(parsed)) throw new Error('JSON precisa ser uma lista');
        setRows(parsed);
        setError('');
      } catch (err) {
        setError(err.message || 'nao consegui ler esse arquivo');
      }
    };
    reader.readAsText(file);
  }

  return h(
    'div',
    { className: 'page-shell' },
    h(
      'section',
      { className: 'hero' },
      h('p', { className: 'eyebrow' }, 'ping-lab viewer'),
      h('h1', null, 'resultado do ping, so que mais facil de olhar'),
      h(
        'p',
        { className: 'intro' },
        'O Python faz o ping. Essa tela so pega o JSON e organiza os dados. E simples mesmo, porque a ideia aqui e aprender sem transformar tudo em monstro.',
      ),
      h(
        'label',
        { className: 'upload-button' },
        'carregar JSON',
        h('input', { type: 'file', accept: 'application/json,.json', onChange: loadFile }),
      ),
      error ? h('p', { className: 'error' }, error) : null,
    ),
    h(
      'section',
      { className: 'metrics-grid' },
      h(MetricCard, { label: 'alvos online', value: summary.online, detail: `${rows.length} testados` }),
      h(MetricCard, { label: 'falhas', value: summary.failed, detail: 'algo nao respondeu' }),
      h(MetricCard, { label: 'media geral', value: formatMs(summary.avgLatency), detail: 'so alvos online' }),
      h(MetricCard, {
        label: 'pior media',
        value: summary.worst?.target || '-',
        detail: summary.worst ? formatMs(summary.worst.avg_ms) : 'sem dados',
      }),
    ),
    h(ResultTable, { rows }),
    h(
      'section',
      { className: 'notes' },
      h('h2', null, 'como usar com o script'),
      h('pre', null, 'python ping_lab.py --format json --output resultado.json'),
      h('p', null, 'Depois abre essa pagina e carrega o arquivo resultado.json. Simples, mas ja separa bem backend/CLI e frontend.'),
    ),
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(h(App));
