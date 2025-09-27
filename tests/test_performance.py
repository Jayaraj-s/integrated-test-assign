import pytest
import threading
import time


def _hit_endpoint(client, endpoint, results, idx):
    """Worker function to hit an endpoint and measure latency"""
    start = time.time()
    resp = client.get(endpoint)
    end = time.time()
    results[idx] = {"status_code": resp.status_code, "time": end - start}


@pytest.mark.parametrize("perf_case", [
    {
        "name": "load_root_10_concurrent",
        "endpoint": "/",
        "concurrency": 10,
        "expected_status": 200,
        "max_avg_time": 0.2
    },
    {
        "name": "load_root_50_concurrent",
        "endpoint": "/",
        "concurrency": 50,
        "expected_status": 200,
        "max_avg_time": 0.5   # looser threshold for higher load
    },
    {
        "name": "load_items_list_20_concurrent",
        "endpoint": "/items",  # requires auth in real app, adapt if needed
        "concurrency": 20,
        "expected_status": 403,  # no auth → expect forbidden
        "max_avg_time": 0.2
    }
])
def test_performance_cases(test_client, perf_case):
    """Table-driven concurrent load benchmark tests"""
    threads = []
    results = [None] * perf_case["concurrency"]

    for i in range(perf_case["concurrency"]):
        t = threading.Thread(
            target=_hit_endpoint,
            args=(test_client, perf_case["endpoint"], results, i)
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Validate responses
    status_codes = [r["status_code"] for r in results if r]
    assert all(code == perf_case["expected_status"] for code in status_codes), \
        f"Unexpected status codes: {status_codes}"

    # Benchmark: average response time
    times = [r["time"] for r in results if r]
    avg = sum(times) / len(times)
    print(f"\n[{perf_case['name']}] concurrency={perf_case['concurrency']} "
          f"avg_time={avg:.4f}s")

    assert avg < perf_case["max_avg_time"], \
        f"Average response time {avg:.4f}s exceeded threshold {perf_case['max_avg_time']}s"
