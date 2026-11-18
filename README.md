# Internet download speed check (ETOLEGKO test task)

Console script that downloads a given URL **10 times in a row**, waits for each full response, then prints:

- average time per request;
- total bytes downloaded;
- **download speed in MiB/s** (mebibytes per second: 1 MiB = 1024² bytes).

Uses `urllib` from the standard library plus **certifi** for HTTPS certificates (fixes `CERTIFICATE_VERIFY_FAILED` on macOS with python.org builds).

## Requirements

- Python 3.9+

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python3 speed_test.py "https://placehold.co/4000x3000.jpg"
```

The URL must be a **direct** link to the file (not Google `imgres` or a HTML page). The example above is a public JPEG (~97 KiB).

Optional per-request timeout (seconds):

```bash
python3 speed_test.py "https://placehold.co/4000x3000.jpg" --timeout 60
```

## Speed units

Throughput is computed as:

`total_bytes / sum(request_durations)`

because requests run **sequentially**. The result is shown as **MiB/s** (binary megabytes per second).

## AI usage (for the application form)

Задание по сути простое — написал бы и без нейросети, но с ИИ (Cursor / Claude) получилось заметно быстрее: скелет скрипта и README, потом сам прошёлся по коду. Прогнал локально, проверил вывод построчно, убрал лишнее, для HTTPS на macOS добавил только certifi.