# MenuDelivery

My program's purpose is to be a menu messaging kiosk between the kitchen and the counter. It will be installed on two raspberry pis, and each will be come a server and a client. There will be CLI methods to connect, select and send menus to the kitchen, and the server can recieve, view and manage the inputs.

## How to Install and Run

1. Clone this repository to your own computer.
2. Assuming you have python3, install the requirements with pip:

`pip install -r requirements.txt`

3. Launch the app with python:

`python3 menu_delivery.py`

## How the program works 

1. There are 2 different nodes that are selectable in the program. There is the server and the client, where they have the roles of being in the kitchen and the counter. 

2. After launching the program, select a node option between server and client:

3. If selected server, then check your IP address on your machine. Setup is complete on the server.

4. If selected client, there will be a series of questions about what node to tonnect to. Enter the IP address of the server and the port number. 

5. The Client will open up a series of menu selection windows that you can use to select and press enter to send to the server. When you are done, exit with closing the window. 

6. The server will continuously listen for the input of new clients/updates of the orders. As of now, the program is a 1-1 connection. 

## Deployment 

If setting up the program in your local devices and this program is set up on the control, you can use ansible to deploy and manage the code. In the ansible forlder, there is a playbook that installs python, virtualenv, pip and requirements to the ssh enabled nodes (raspberri pis). Launch the playbook after editting the ip addresses and ssh requirements of the endpoints with 

`ansible-playbook playbook.yml`

## Contributions 

To contribute to the project, fork and clone the repository and send a pull request with the feature/bug fix and the functionality that your contributions provide. In the folder "code_review", there is a pdf with the collaboration ethics guide that will help with commenting and working with me. 

## Testing 

There is a test.py file in the repository that currently handles unit tests for the user inputs of IP and port addresses. I potentially will add more tests based on the types of scaling I perform. 