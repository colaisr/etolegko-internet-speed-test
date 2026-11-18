# Internet download speed check (ETOLEGKO test task)

Console script that downloads a given URL **10 times in a row**, waits for each full response, then prints:

- average time per request;
- total bytes downloaded;
- **download speed in MiB/s** (mebibytes per second: 1 MiB = 1024² bytes).

Only the Python standard library is used (`urllib`, no extra packages).

## Requirements

- Python 3.9+

## Run

```bash
python3 speed_test.py "https://example.com/path/to/large-file.bin"
```

Optional per-request timeout (seconds):

```bash
python3 speed_test.py "https://example.com/file.jpg" --timeout 60
```

### Example URL

Any stable direct link to a sizable file works, for example a public test asset from your CDN or a well-known large static file. Avoid login walls and redirects to HTML pages.

## Speed units

Throughput is computed as:

`total_bytes / sum(request_durations)`

because requests run **sequentially**. The result is shown as **MiB/s** (binary megabytes per second).

## AI usage (for the application form)

Cursor (Claude) helped draft the script structure and README wording; logic was reviewed and kept minimal on purpose — sequential downloads, `perf_counter()` timing, explicit MiB/s in the output.