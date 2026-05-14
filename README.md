# ping-lab

Esse repo nasceu porque eu queria parar de olhar para "a internet ta ruim" sem ter numero nenhum.

A ideia e simples: rodar `ping` em um ou mais alvos, pegar a saida do terminal e transformar isso em tabela, JSON, CSV ou numa telinha web.

Nao coloquei isso aqui como produto pronto. E um lab pequeno para treinar rede basica, Python e um pouco de front-end em cima de dado real.

## o que tem aqui

- `ping_lab.py`: CLI em Python
- teste de um ou varios alvos
- perda de pacote
- latencia minima, media e maxima
- jitter simples
- saida em tabela, JSON ou CSV
- viewer web em React para abrir o JSON gerado

## rodando no terminal

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

Gerando CSV:

```bash
python ping_lab.py --format csv --output resultado.csv
```

## viewer web

A parte web fica em:

```bash
web/index.html
```

O navegador nao executa `ping` direto. O fluxo que eu fiz foi:

```text
Python coleta -> salva JSON -> React mostra os dados
```

Fiz assim porque browser nao faz ICMP, e tambem porque separa bem as coisas: Python fica com a coleta e a tela fica so com a visualizacao.

## o que eu treinei

- `argparse`
- `subprocess.run`
- parse da saida do `ping`
- regex para pegar `time=... ms`
- calculo simples com `statistics`
- JSON e CSV
- React lendo arquivo gerado por script

## limites

- depende do comando `ping` do sistema
- pensei primeiro em Linux, entao outro sistema pode exigir ajuste no parse
- o viewer usa React via CDN
- o regex em cima da saida do `ping` ainda e a parte mais fragil

## o que falta

- guardar historico de execucoes
- gerar graficos melhores
- configurar os alvos pela tela
- mostrar comparacao entre rodadas ou dias diferentes
- adicionar testes para o parse da saida do `ping`
- melhorar a mensagem quando o comando `ping` nao existe

## nota

O ponto principal aqui foi treinar a ligacao entre CLI e uma tela simples: o Python coleta os dados e o viewer so apresenta o JSON.
