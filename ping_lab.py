#!/usr/bin/env python3
import argparse
import csv
import json
import sys
import re
import statistics
import subprocess
from datetime import datetime, timezone


DEFAULT_TARGETS = ["1.1.1.1", "8.8.8.8", "github.com"]


def positive_int(value):
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("precisa ser um numero inteiro") from exc

    if number <= 0:
        raise argparse.ArgumentTypeError("precisa ser maior que zero")

    return number


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
        "jitter_ms": round(statistics.pstdev(times), 2) if len(times) > 1 else 0 if times else None,
        "started_at": started_at,
        "command": " ".join(command),
    }

    if result.returncode != 0 and not times:
        summary["error"] = output.strip().splitlines()[-1] if output.strip() else "ping falhou"

    return summary


def print_table(rows):
    print("target               ok   recv  loss     min      avg      max      jitter")
    print("-" * 78)
    for row in rows:
        ok = "sim" if row["ok"] else "nao"
        loss = "-" if row["packet_loss"] is None else f"{row['packet_loss']:.0f}%"
        min_ms = "-" if row["min_ms"] is None else f"{row['min_ms']}ms"
        avg = "-" if row["avg_ms"] is None else f"{row['avg_ms']}ms"
        max_ms = "-" if row["max_ms"] is None else f"{row['max_ms']}ms"
        jitter = "-" if row["jitter_ms"] is None else f"{row['jitter_ms']}ms"
        print(f"{row['target']:<20} {ok:<4} {row.get('received', 0):<5} {loss:<8} {min_ms:<8} {avg:<8} {max_ms:<8} {jitter}")


def print_csv(rows):
    fields = [
        "target",
        "ok",
        "sent",
        "received",
        "packet_loss",
        "min_ms",
        "avg_ms",
        "max_ms",
        "jitter_ms",
        "started_at",
    ]
    writer = csv.DictWriter(sys.stdout, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="ping pequeno para olhar rede")
    parser.add_argument("--target", action="append", help="alvo para testar")
    parser.add_argument("--count", type=positive_int, default=3, help="quantidade de pacotes")
    parser.add_argument("--timeout", type=positive_int, default=2, help="timeout por pacote")
    parser.add_argument("--format", choices=["table", "json", "csv"], default="table", help="formato da saida")
    parser.add_argument("--json", action="store_true", help="atalho para --format json")
    args = parser.parse_args()

    targets = args.target or DEFAULT_TARGETS
    rows = [run_ping(target, args.count, args.timeout) for target in targets]
    output_format = "json" if args.json else args.format

    if output_format == "json":
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    elif output_format == "csv":
        print_csv(rows)
    else:
        print_table(rows)

    if any(not row["ok"] for row in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
