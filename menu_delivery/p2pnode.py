import time
import socket
from p2pnetwork.node import Node
from rich.live import Live
from rich.table import Table


class P2PNode(Node):
    """P2P Node Module extended from p2pnetwork.nodem with a few changes
    to the run function where it updates the server visuals every loop

    Args:
        Node (Node): extends the node class from p2pnetwork
    """

    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        """initializes the Node for connecting from/to.
        generates the Table for the server's output and the message sent.

        Args:
            host (string): host IP
            port (string): host Port
            id (string, optional): host id. Defaults to None.
            callback (function, optional): callback function. Defaults to None.
            max_connections (int, optional): number of max connections. Defaults to 0.
        """
        super(P2PNode, self).__init__(host, port, id, callback, max_connections)
        self.msg = None
        self.server_table = Table()

    def node_message(self, node, data):
        """Determines how the messages sent by the nodes will be formatted

        Args:
            node (Node): the node that is related to the sent message
            data (string): data that is being sent between the nodes in string format
        """
        self.msg = (self.id, node.id, data)

    def run(self):
        """The main loop of the thread that deals with connections from other
        nodes on the network. When a node is connected it will exchange the
        node id's. First we receive the id of the connected node and secondly
        we will send our node id to the connected node. When connected the method
        inbound_node_connected is invoked."""

        with Live(self.server_table, refresh_per_second=4):
            prior_order = ""
            while (
                not self.terminate_flag.is_set()
            ):  # Check whether the thread needs to be closed
                try:
                    time.sleep(0.4)
                    if self.msg is not None:
                        order_number = self.msg[2]["order_number"]
                        if prior_order != order_number:
                            order_description = {
                                k: self.msg[2][k]
                                for k in set(list(self.msg[2].keys()))
                                - set(["order_number"])
                            }
                            self.server_table.add_row(
                                f"{order_number}", f"""{order_description}"""
                            )
                            prior_order = order_number

                    self.debug_print("Node: Wait for incoming connection")
                    connection, client_address = self.sock.accept()

                    self.debug_print(
                        "Total inbound connections:" + str(len(self.nodes_inbound))
                    )

                    # When the maximum connections is reached, it disconnects the connection
                    if (
                        self.max_connections == 0
                        or len(self.nodes_inbound) < self.max_connections
                    ):

                        # Basic information exchange (not secure) of the id's of the nodes!
                        connected_node_port = client_address[1]  # backward compatibilty
                        connected_node_id = connection.recv(4096).decode("utf-8")
                        if ":" in connected_node_id:
                            (
                                connected_node_id,
                                connected_node_port,
                            ) = connected_node_id.split(
                                ":"
                            )  # When a node is connected, it sends it id!
                        connection.send(
                            self.id.encode("utf-8")
                        )  # Send my id to the connected node!

                        thread_client = self.create_new_connection(
                            connection,
                            connected_node_id,
                            client_address[0],
                            connected_node_port,
                        )
                        thread_client.start()

                        self.nodes_inbound.append(thread_client)
                        self.inbound_node_connected(thread_client)

                    else:
                        self.debug_print(
                            "New connection is closed. You have reached the maximum connection limit!"
                        )
                        connection.close()

                except socket.timeout:
                    self.debug_print("Node: Connection timeout!")

                except Exception as exception:
                    self.inbound_node_connection_error(exception)
                    raise exception

                self.reconnect_nodes()

                time.sleep(0.01)

            print("Node stopping...")
            for node in self.all_nodes:
                node.stop()

            time.sleep(1)

            for node in self.all_nodes:
                node.join()

            self.sock.settimeout(None)
            self.sock.close()
            print("Node stopped")
