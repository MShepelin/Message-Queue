import asyncio
import grpc
import wikilength_pb2
import wikilength_pb2_grpc
from time import sleep
import pickle
from gui import WikiLengthGUI

def send_task(request_id, url1, url2):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = wikilength_pb2_grpc.WikiLengthStub(channel)
        return stub.CalculateLength(wikilength_pb2.LengthRequest(
            request_id=request_id,
            url1 = url1,#"https://ru.wikipedia.org/wiki/Bro",
            url2 = url2 #"http://www.bro-ids.org/"
        ))

gui_link=None

def on_send(url1, url2):
    global gui_link
    response = send_task("1", url1, url2)
    req_id = response.request_id
    status = response.status
    gui_link.receive_msg('Executing query with python RQ')
    while status == wikilength_pb2.LengthResponse.QueryStatus.PENDING:
        sleep(1)
        gui_link.receive_msg('.')
        response = send_task(req_id, url1, url2)
        status = response.status

    array = pickle.loads(response.payload)

    if len(array) == 0:
        gui_link.receive_msg('\nDidn\'t find path\n')
    else:
        gui_link.receive_msg('\nFound path!\nPath length is {}\n'.format(len(array)))
        for i in array:
            gui_link.receive_msg(i.decode('utf-8') + '\n')

    gui_link.enable_input()

if __name__ == "__main__":
    gui = WikiLengthGUI(on_send)
    gui_link = gui
    gui.start()
