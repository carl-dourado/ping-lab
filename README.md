# ping-lab

Um lab pequeno para testar `ping`, ver latencia/perda e transformar a saida do terminal em algo mais facil de olhar.

Nao e uma ferramenta profissional de monitoramento. Fiz mais para estudar rede basica, Python e um pouco de front-end sem complicar demais.

## o que tem

- CLI em Python
- teste de um ou varios alvos
- latencia minima, media, maxima e jitter
- perda de pacote
- saida em tabela, JSON ou CSV
- viewer simples em React para abrir o JSON

## uso rapido

```bash
python ping_lab.py
```

Com alvos especificos:

```bash
python ping_lab.py --target 1.1.1.1 --target github.com --count 4
```

Gerando JSON:

```bash
python ping_lab.py --format json --output resultado.json
```

## viewer web

A parte web fica em:

```bash
web/index.html
```

Ela nao executa ping pelo navegador. O fluxo e:

```text
Python faz o ping -> gera JSON -> React mostra os dados
```

Fiz assim porque o navegador nao faz ICMP direto, e tambem porque separa bem as coisas: Python coleta, React visualiza.

## formatos

Tabela:

```bash
python ping_lab.py --format table
```

JSON:

```bash
python ping_lab.py --format json
```

CSV:

```bash
python ping_lab.py --format csv
```

## o que eu treinei aqui

- `argparse`
- `subprocess.run`
- regex para pegar `time=... ms`
- media e jitter com `statistics`
- JSON/CSV
- React lendo um arquivo gerado pelo Python

## limites

- pensado primeiro para Linux
- depende do comando `ping` do sistema
- o viewer usa React via CDN
- nao guarda historico ainda
