from __future__ import print_function, unicode_literals
from datetime import datetime
import json
import sys

from PyInquirer import style_from_dict, Token, prompt, Separator
from PyInquirer import Validator, ValidationError
from pyfiglet import Figlet

from p2pnode import P2PNode
import regex


class initialization(P2PNode):
    """Initializes the Program and creates either a server or client instance.
    For servers, it also creates the CLI interface for updates from the client."""

    def __init__(self, node_type):
        self.node_type = node_type

    def initialize_node(self):
        """Initializes and starts the node by taking the node_type
            from the class variable. It also creates the CLI interface
            for updates from the client.

        Returns:
            node: client or server node, which is a Node Object from p2pnode
        """
        if self.node_type["Node_Type"] == "Client":
            client = P2PNode("127.0.0.1", 10001, 1)
            print("Client node initialized")
            return client

        server = P2PNode("127.0.0.1", 10002, 2)
        server.debug = True
        server.server_table.add_column("Order Number")
        server.server_table.add_column("Order Description")
        print("Server node initialized")
        server.start()
        return server


class CLI:
    """Creates multiple Command Line Interface, starting from connecting to
    nodes and selecting menus.
    """

    def __init__(self):
        """Styles the Command Line Interface, and adds the Title of the CLI
        Imports the menu options from a json file.
        """
        self.style = style_from_dict(
            {
                Token.Separator: "#cc5454",
                Token.QuestionMark: "#673ab7 bold",
                Token.Selected: "#cc5454",  # default
                Token.Pointer: "#673ab7 bold",
                Token.Instruction: "",  # default
                Token.Answer: "#f44336 bold",
                Token.Question: "",
            }
        )
        f = Figlet(font="slant")
        print(f.renderText("Menu Delivery v0.1"))
        self.json = "./menu.json"
        self.menu = self.import_menu_from_json()

    def import_menu_from_json(self):
        """Imports the menu from the user editable json file and
        adds it as a dictionary for the CLI to implement.

        Returns:
            menu: dictionary of menus converted from the json file.
        """
        with open(self.json) as json_file:
            menu = json.load(json_file)
        return menu

    def add_choices(self, questions, category):
        choices = questions[0]["choices"]
        choices.append((Separator(f"= The {category} =")))
        for i in self.menu[f"{category}"]:
            choices.append(i)
        return questions

    def window_type_selection_cli(self):
        """Creates the list of questions for selecting
        which node to initialize

        Returns:
            answers: result of the selection in document format
        """
        questions = [
            {
                "type": "list",
                "message": "Select Node Type",
                "name": "Node_Type",
                "choices": [Separator("Node Type"), "Server", "Client"],
                "validate": lambda answer: "You must choose at a node type"
                if len(answer) == 0
                else True,
            }
        ]

        answers = prompt(questions, style=self.style)
        return answers

    def initialize_node_client_cli(self):
        """Creates a list of questions for required
        Ip addresses and Port numbers needed for the client to
        connect to the server.

        Returns:
            answers: result of the selection in document format
        """
        questions = [
            {
                "type": "input",
                "name": "outbound_ip",
                "message": "Enter the outbound IP address",
                "validate": IPValidator,
            },
            {
                "type": "input",
                "name": "outbound_port",
                "message": "Enter the outbound IP Port",
                "validate": PortValidator,
            },
        ]
        answers = prompt(questions, style=self.style)
        return answers

    def client_menu_selection_cli(self):
        """Creates a list of questions for the user to
        select their menu from the menu imported in the initialization.

        Returns:
            answers: result of the menu selection in document format
        """
        order_number = str(datetime.now())
        print(self.menu["noodles"])
        questions = [
            {
                "type": "checkbox",
                "message": "Select toppings",
                "name": "toppings",
                "choices": [],
                "validate": lambda answer: "You must choose at least one topping."
                if len(answer) == 0
                else True,
            }
        ]

        self.add_choices(questions, "noodles")
        self.add_choices(questions, "soup")
        self.add_choices(questions, "toppings")
        self.add_choices(questions, "garlic")
        self.add_choices(questions, "spice")

        answers = prompt(questions, style=self.style)
        answers["order_number"] = order_number
        return answers

    def run(self):
        """Runs the program, starting from the CLI and listens for messages to
        send to the server.
        """
        node_type = self.window_type_selection_cli()
        init = initialization(node_type)
        if node_type["Node_Type"] == "Client":
            outbound_connection_info = self.initialize_node_client_cli()
            init.node = init.initialize_node()
            init.node.connect_with_node(
                outbound_connection_info["outbound_ip"],
                int(outbound_connection_info["outbound_port"]),
            )
            try:
                while True:
                    menu_selection = self.client_menu_selection_cli()
                    init.node.send_to_nodes(menu_selection)
            except KeyboardInterrupt:
                sys.exit(1)
        else:
            init.node = init.initialize_node()


class IPValidator(Validator):
    """Validates the integrity of user inputted IP address

    Args:
        Validator: extends Validation from PyInquirer
    """

    def validate(self, document):
        """Validates the integrity of user inputted IP address

        Args:
            document: format of data in PyInquirer with the Ip address

        Raises:
            ValidationError: If the IP is not correctly formatted, throw an error

        Returns:
            Bool: Check if validated
        """
        ip = regex.match(
            "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
            document.text,
        )
        if not ip:
            raise ValidationError(
                message="Please enter a valid IPv4 number",
                cursor_position=len(document.text),
            )  # Move cursor to end
        return True


class PortValidator(Validator):
    """Validates the integrity of user inputted Port address

    Args:
        Validator: extends Validation from PyInquirer
    """

    def validate(self, document):
        """Validates the integrity of user inputted Port address

        Args:
            document: format of data in PyInquirer with the Port address

        Raises:
            ValidationError: If the Port is not correctly formatted, throw an error

        Returns:
            Bool: Check if validated
        """
        if int(document.text) > 25565 or int(document.text) < 1:
            raise ValidationError(
                message="Please enter a valid IPv4 number",
                cursor_position=len(document.text),
            )  # Move cursor to end


if __name__ == "__main__":
    cli = CLI()
    cli.run()
