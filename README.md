# ping-lab

Um script pequeno em Python para testar ping em alguns alvos e transformar aquela saida grande do terminal em uma tabela mais facil de ler.

A ideia nao foi criar uma ferramenta gigante de rede. Fiz mais como um lab mesmo, para entender melhor latencia, perda de pacote, timeout e tambem treinar leitura de saida de comando no Python.

## o que ele faz

- testa um ou mais alvos com o comando `ping`
- mostra se respondeu ou nao
- calcula pacotes recebidos, perda, menor tempo, media, maior tempo e jitter
- permite mudar quantidade de pacotes e timeout
- gera saida em tabela, JSON ou CSV
- salva a saida em arquivo com `--output`
- tem um viewer web simples em React para abrir o JSON
- nao usa dependencia externa

## por que fiz

Eu uso Linux no dia a dia e muita coisa de rede aparece primeiro como comando solto no terminal. O `ping` parece simples, mas ele ja mostra bastante coisa: se o alvo responde, se tem perda, se a latencia esta alta e se a conexao esta oscilando.

Esse projeto foi um jeito de pegar um comando que eu ja usava e transformar em um script organizado. Nao e uma solucao profissional de monitoramento, mas e uma boa base para aprender automacao, subprocess, regex, argparse e saida em formatos diferentes.

Depois adicionei uma parte web com React, mas sem tentar fazer o navegador executar ping. Browser nao faz ICMP direto. Entao a separacao ficou assim: o Python coleta os dados e o React so mostra o JSON de um jeito mais visual.

## como rodar

```bash
python ping_lab.py
```

Por padrao ele testa:

- `1.1.1.1`
- `8.8.8.8`
- `github.com`

## testando um alvo especifico

```bash
python ping_lab.py --target github.com
```

Tambem da para passar mais de um:

```bash
python ping_lab.py --target 1.1.1.1 --target github.com --target example.com
```

## mudando quantidade e timeout

```bash
python ping_lab.py --target github.com --count 5 --timeout 2
```

Onde:

- `--count` e a quantidade de pacotes
- `--timeout` e o tempo maximo de espera por pacote

## saida em JSON

```bash
python ping_lab.py --format json
```

Ou usando o atalho:

```bash
python ping_lab.py --json
```

Exemplo do tipo de informacao que aparece:

```json
[
  {
    "target": "github.com",
    "ok": true,
    "sent": 3,
    "received": 3,
    "packet_loss": 0.0,
    "min_ms": 31.2,
    "avg_ms": 32.8,
    "max_ms": 34.1,
    "jitter_ms": 1.19
  }
]
```

Tambem da para salvar em arquivo:

```bash
python ping_lab.py --format json --output resultado.json
```

## saida em CSV

```bash
python ping_lab.py --format csv
```

Essa parte e util se eu quiser jogar o resultado em outro lugar depois, tipo planilha, log ou algum script maior.

## viewer web com React

Tem uma tela simples em `web/index.html`.

Ela nao roda ping. Ela so carrega um JSON gerado pelo Python e mostra:

- quantos alvos responderam
- quantos falharam
- media geral dos alvos online
- pior alvo pela media de latencia
- tabela com perda, media e jitter

Para testar:

```bash
python ping_lab.py --format json --output resultado.json
```

Depois abre:

```bash
web/index.html
```

E carrega o arquivo `resultado.json` no botao da tela.

Fiz assim porque e um passo bom para iniciante/intermediario: tem Python, tem JSON, tem JavaScript e tem React, mas cada parte faz uma coisa bem clara.

## o que aprendi aqui

- usar `argparse` para criar uma CLI simples
- chamar comando externo com `subprocess.run`
- capturar `stdout` e `stderr`
- usar regex para encontrar `time=... ms` e `packet loss`
- calcular media e jitter com `statistics`
- retornar JSON e CSV sem instalar biblioteca
- salvar resultado em arquivo
- usar React para visualizar dados que vieram do Python
- cuidar de erro quando o `ping` nao existe ou o alvo nao responde

## limites

- foi pensado primeiro para Linux
- depende do comando `ping` do sistema
- a parte web depende do React via CDN
- o navegador nao executa ping de verdade
- nao substitui monitoramento real
- a saida do `ping` pode mudar dependendo do sistema operacional

## proximas ideias

- salvar historico em arquivo
- rodar varias vezes em intervalo
- gerar um resumo final dizendo qual alvo ficou pior
- separar funcoes para facilitar testes automatizados
- trocar o React via CDN por Vite quando fizer sentido
- talvez gerar um historico que o viewer consiga comparar por horario
