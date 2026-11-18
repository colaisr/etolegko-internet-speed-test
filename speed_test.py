#!/usr/bin/env python3
"""Console tool: measure download speed with 10 sequential HTTP GET requests."""

from __future__ import annotations

import argparse
import sys
import time
import urllib.error
import urllib.request

REQUEST_COUNT = 10


def download_once(url: str, timeout: float) -> tuple[float, int]:
    started = time.perf_counter()
    with urllib.request.urlopen(url, timeout=timeout) as response:
        body = response.read()
    elapsed = time.perf_counter() - started
    return elapsed, len(body)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download a URL 10 times and print average time and speed.",
    )
    parser.add_argument("url", help="URL to request (e.g. a large static file)")
    parser.add_argument(
        "--timeout",
        type=float,
        default=120.0,
        help="Socket timeout per request in seconds (default: 120)",
    )
    args = parser.parse_args()

    durations: list[float] = []
    total_bytes = 0

    for index in range(1, REQUEST_COUNT + 1):
        try:
            elapsed, size = download_once(args.url, args.timeout)
        except urllib.error.URLError as exc:
            print(f"Request {index}/{REQUEST_COUNT} failed: {exc}", file=sys.stderr)
            return 1

        durations.append(elapsed)
        total_bytes += size
        print(f"  [{index}/{REQUEST_COUNT}] {size:,} bytes in {elapsed:.3f} s")

    avg_time = sum(durations) / len(durations)
    total_time = sum(durations)
    bytes_per_second = total_bytes / total_time if total_time else 0.0

    # Speed unit documented in README: MiB/s (mebibytes per second).
    mebibytes_per_second = bytes_per_second / (1024 * 1024)

    print()
    print(f"Average request time: {avg_time:.3f} s")
    print(f"Total downloaded:     {total_bytes:,} bytes ({total_bytes / (1024**2):.2f} MiB)")
    print(f"Download speed:       {mebibytes_per_second:.2f} MiB/s")

    return 0


if __name__ == "__main__":
    sys.exit(main())