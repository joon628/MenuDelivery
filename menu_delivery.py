import json
import time
from p2pnetwork.node import Node

class initialization():
    def __init__(self):
        self.window_type = self.window_type_selection()
        self.menu_list = self.import_menu_from_json()
        
    def window_type_selection(self):
        user_selection = input("Select Window Type: 1. Server, 2. Client")
        try:
            if user_selection.lower() == "server":
                return 0
            elif user_selection.lower() == "client":
                return 1
        except(TypeError):
            print("Input error")
            
    def import_menu_from_json(self):
        pass

class server():
    def __init__(self, host_ip, port) -> None:
        self.host_ip = host_ip
        self.port = port
        self.node = Node(self.host_ip, self.port, callback=node_callback)
        self.node.start()
    
    def node_callback(self, event, main_node, connected_node, data):
        """The big callback method that gets all the events that happen inside the p2p network.
        Implement here your own application logic. The event holds the event that occurred within
        the network. The main_node contains the node that is handling the connection with and from
        other nodes. An event is most probably triggered by the connected_node! If there is data
        it is represented by the data variable."""
        try:
            # node_request_to_stop does not have any connected_node, while it is the main_node that is stopping!
            if event != 'node_request_to_stop':
                print('Event: {} from main node {}: connected node {}: {}'.format(event, main_node.id, connected_node.id,
                                                                                data))

        except Exception as e:
            print(e)
    
    def send_data(self, msg):
        self.node.send_to_nodes(msg)
    
    def terminate_server(self):
        self.node.stop()
        
    
class client():
    def __init__(self) -> None:
        pass
    
    
    
    

    
    