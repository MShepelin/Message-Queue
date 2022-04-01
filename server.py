from webrowsing import search_path

from time import sleep

from concurrent import futures

from redis import Redis
from rq import Queue

import wikilength_pb2
import wikilength_pb2_grpc

import grpc

import pickle

class WikiLengthServer(wikilength_pb2_grpc.WikiLengthServicer):
    def __init__(self):
        self.redis = Redis(host='localhost', port='6379')
        self.q = Queue(connection=self.redis)

    def CalculateLength(
            self, request: wikilength_pb2.LengthRequest,
            context: grpc.aio.ServicerContext):

        request_id = request.request_id
        job = self.q.fetch_job(request_id)
        payload = b""
        status=None

        if job is None:
            job = self.q.enqueue(search_path, request.url1, request.url2, 100)
            request_id = job.id
        
        if job.get_status() in ['queued', 'started', 'deferred']:
            status=wikilength_pb2.LengthResponse.QueryStatus.PENDING
        elif job.get_status() == 'finished':
            status=wikilength_pb2.LengthResponse.QueryStatus.OK
            # to-do: add packaging (pickle, json, etc)
            payload=pickle.dumps(job.result, 2)
        else:
            status=wikilength_pb2.LengthResponse.QueryStatus.ERROR
        
        return wikilength_pb2.LengthResponse(
            request_id=request_id, 
            status=status,
            payload=payload
        )

def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    wikilength_pb2_grpc.add_WikiLengthServicer_to_server(
        WikiLengthServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__=="__main__":
    main()
