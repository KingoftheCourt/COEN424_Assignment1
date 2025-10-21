import grpc
import nobel_prize_service_pb2 as pb2
import nobel_prize_service_pb2_grpc as pb2_grpc

def main():
    channel = grpc.insecure_channel("localhost:50051")
    stub = pb2_grpc.NobelPrizeServiceStub(channel)

    # Q1
    q1 = stub.GetLaureatesByCategory(
        pb2.CategoryYearRequest(category="physics", start_year=2013, end_year=2023)
    )
    print("Q1:", q1.total_laureates, q1.success, q1.error_message)

    # Q2
    q2 = stub.GetLaureatesByMotivation(pb2.MotivationRequest(keyword="neutrino"))
    print("Q2:", q2.total_laureates, q2.success, q2.error_message)

    # Q3
    q3 = stub.GetLaureateByName(pb2.NameRequest(firstname="Peter", surname="Higgs"))
    print("Q3 success:", q3.success, q3.error_message)
    for i, d in enumerate(q3.laureates, 1):
        print(f"  [{i}] {d.year} | {d.category} | {d.motivation}")

if __name__ == "__main__":
    main()
