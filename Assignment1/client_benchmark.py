import os, csv, time, statistics, grpc
from pathlib import Path

import nobel_prize_service_pb2 as pb2
import nobel_prize_service_pb2_grpc as pb2_grpc  # <- use this alias consistently

OUTDIR = Path("benchmarks")
OUTDIR.mkdir(exist_ok=True)

N_RUNS = 100
SERVER_ADDR = os.getenv("GRPC_ADDR", "localhost:50051")

def time_calls(fn, n=N_RUNS):
    times_ms = []
    for _ in range(n):
        t0 = time.perf_counter()
        fn()
        t1 = time.perf_counter()
        times_ms.append((t1 - t0) * 1000.0)
    return times_ms

def write_csv(path, arr):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["run", "latency_ms"])
        for i, v in enumerate(arr, 1):
            w.writerow([i, f"{v:.3f}"])

def main():
    # one channel + stub, using the alias
    channel = grpc.insecure_channel(SERVER_ADDR)
    stub = pb2_grpc.NobelPrizeServiceStub(channel)

    # Define the three callables so timing only measures RPC, not setup
    def q1():
        stub.GetLaureatesByCategory(
            pb2.CategoryYearRequest(category="physics", start_year=2013, end_year=2023)
        )

    def q2():
        stub.GetLaureatesByMotivation(pb2.MotivationRequest(keyword="neutrino"))

    def q3():
        stub.GetLaureateByName(pb2.NameRequest(firstname="Peter", surname="Higgs"))

    # Warm-up
    for _ in range(5):
        q1(); q2(); q3()

    t1 = time_calls(q1)
    t2 = time_calls(q2)
    t3 = time_calls(q3)

    write_csv(OUTDIR / "q1_category_year.csv", t1)
    write_csv(OUTDIR / "q2_motivation.csv", t2)
    write_csv(OUTDIR / "q3_name.csv", t3)

    def stats(name, arr):
        print(f"{name}: mean={statistics.mean(arr):.2f} ms, "
              f"p95={sorted(arr)[int(0.95*len(arr))-1]:.2f} ms, "
              f"min={min(arr):.2f} ms, max={max(arr):.2f} ms")

    stats("Q1", t1); stats("Q2", t2); stats("Q3", t3)
    print(f"\nSaved CSVs in: {OUTDIR.resolve()}")

if __name__ == "__main__":
    main()
