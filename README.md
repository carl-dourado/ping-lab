# ping-lab

Um script pequeno para testar ping sem ficar copiando saida grande do terminal.

A ideia aqui e ver latencia, perda e status de alguns alvos basicos. Nao e ferramenta pronta, e mais um lab para entender ICMP e problema bobo de rede.

## uso

```bash
python ping_lab.py
```

Com um alvo especifico:

```bash
python ping_lab.py --target 1.1.1.1 --count 4
```

Saida em JSON:

```bash
python ping_lab.py --json
```

## notas

- feito pensando em Linux
- usa o comando `ping` do sistema
- sem dependencia externa

