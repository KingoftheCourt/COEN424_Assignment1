# assignment_2.2.py  — gRPC server
import os
import grpc
from concurrent import futures

import nobel_prize_service_pb2 as pb2
import nobel_prize_service_pb2_grpc as pb2_grpc

# Reuse your Task 1.3 functions
from assignment_1_3 import (
    query_laureates_by_category_and_year_range,
    query_laureates_by_motivation_keyword,
    query_laureate_by_name,
)

class NobelPrizeService(pb2_grpc.NobelPrizeServiceServicer):
    def GetLaureatesByCategory(self, request, context):
        try:
            count = query_laureates_by_category_and_year_range(
                request.category, request.start_year, request.end_year
            )
            return pb2.LaureateCountResponse(
                total_laureates=count, success=True, error_message=""
            )
        except Exception as e:
            return pb2.LaureateCountResponse(
                total_laureates=0, success=False, error_message=str(e)
            )

    def GetLaureatesByMotivation(self, request, context):
        try:
            count = query_laureates_by_motivation_keyword(request.keyword)
            return pb2.LaureateCountResponse(
                total_laureates=count, success=True, error_message=""
            )
        except Exception as e:
            return pb2.LaureateCountResponse(
                total_laureates=0, success=False, error_message=str(e)
            )

    def GetLaureateByName(self, request, context):
        try:
            rows = query_laureate_by_name(request.firstname, request.surname)
            details = [
                pb2.LaureateDetail(
                    year=str(row.get("year", "")),
                    category=row.get("category", ""),
                    motivation=row.get("motivation", ""),
                )
                for row in rows
            ]
            return pb2.LaureateDetailsResponse(
                laureates=details, success=True, error_message=""
            )
        except Exception as e:
            return pb2.LaureateDetailsResponse(
                laureates=[], success=False, error_message=str(e)
            )

def serve():
    port = os.getenv("GRPC_PORT", "50051")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    pb2_grpc.add_NobelPrizeServiceServicer_to_server(NobelPrizeService(), server)
    server.add_insecure_port(f"[::]:{port}")
    print(f"gRPC server listening on {port} ...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    # Make sure your index exists (run assignment_1.2.py once if needed)
    serve()
