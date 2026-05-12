#!/usr/bin/env python3
import argparse
import json
import re
import statistics
import subprocess
from datetime import datetime, timezone


DEFAULT_TARGETS = ["1.1.1.1", "8.8.8.8", "github.com"]


def run_ping(target, count, timeout):
    command = ["ping", "-c", str(count), "-W", str(timeout), target]
    started_at = datetime.now(timezone.utc).isoformat()

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
    except FileNotFoundError:
        return {
            "target": target,
            "ok": False,
            "error": "ping nao encontrado",
            "started_at": started_at,
        }

    output = f"{result.stdout}\n{result.stderr}"
    times = [float(value) for value in re.findall(r"time[=<]([0-9.]+)\s*ms", output)]
    loss_match = re.search(r"([0-9.]+)%\s*packet loss", output)
    packet_loss = float(loss_match.group(1)) if loss_match else None

    summary = {
        "target": target,
        "ok": result.returncode == 0,
        "sent": count,
        "received": len(times),
        "packet_loss": packet_loss,
        "min_ms": min(times) if times else None,
        "avg_ms": round(statistics.mean(times), 2) if times else None,
        "max_ms": max(times) if times else None,
        "started_at": started_at,
        "command": " ".join(command),
    }

    return summary


def print_table(rows):
    print("target               ok   recv  loss     avg")
    print("-" * 48)
    for row in rows:
        ok = "sim" if row["ok"] else "nao"
        loss = "-" if row["packet_loss"] is None else f"{row['packet_loss']:.0f}%"
        avg = "-" if row["avg_ms"] is None else f"{row['avg_ms']}ms"
        print(f"{row['target']:<20} {ok:<4} {row.get('received', 0):<5} {loss:<8} {avg}")


def main():
    parser = argparse.ArgumentParser(description="ping pequeno para olhar rede")
    parser.add_argument("--target", action="append", help="alvo para testar")
    parser.add_argument("--count", type=int, default=3, help="quantidade de pacotes")
    parser.add_argument("--timeout", type=int, default=2, help="timeout por pacote")
    parser.add_argument("--json", action="store_true", help="mostrar JSON")
    args = parser.parse_args()

    targets = args.target or DEFAULT_TARGETS
    rows = [run_ping(target, args.count, args.timeout) for target in targets]

    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return

    print_table(rows)


if __name__ == "__main__":
    main()

