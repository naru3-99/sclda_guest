import socket


class UDPClient:
    """
    UDP client.

    Attributes:
        _sock (socket.socket): The socket object used for communication.
        _host_ports_dict (dict): A dictionary mapping host addresses to a list of port numbers.

    Methods:
        add_destination(host: str, port: int): Adds a destination to the host_ports_dict.
        remove_destination(host: str, port: int) -> bool: Removes a destination from the host_ports_dict.
        send_message(message, host, port, encoding) -> bool: Sends a message to a specific host and port.
        send_message_to_all(message: str, encoding: str = "ascii") -> None: Sends a message to all destinations in the host_ports_dict.
    """

    def __init__(self) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._host_ports_dict = {}

    def add_destination(self, host: str, port: int):
        """
        Adds a destination to the host_ports_dict.

        Args:
            host (str): The host address.
            port (int): The port number.
        """
        if host in self._host_ports_dict.keys():
            self._host_ports_dict[host].append(port)
        else:
            self._host_ports_dict[host] = [port]

    def remove_destination(self, host: str, port: int) -> bool:
        """
        Removes a destination from the host_ports_dict.

        Args:
            host (str): The host address.
            port (int): The port number.

        Returns:
            bool: True if the destination was successfully removed, False otherwise.
        """
        if not (host in self._host_ports_dict.keys()):
            return False
        if not (port in self._host_ports_dict[host]):
            return False
        self._host_ports_dict[host].remove(port)
        return True

    def send_message(
        self, host: str, port: int, message: str, encoding: str = "ascii"
    ) -> bool:
        """
        Sends a message to a specific host and port.

        Args:
            message: The message to send.
            host (str): The host address.
            port (int): The port number.
            encoding (str): The encoding to use for the message.

        Returns:
            bool: True if the message was successfully sent, False otherwise.
        """
        try:
            self._sock.sendto(message.encode(encoding), (host, port))
            return True
        except Exception as e:
            print(f"Error while sending message: {str(e)}")
            return False

    def send_message_to_all(self, message: str, encoding: str = "ascii") -> None:
        """
        Sends a message to all destinations in the host_ports_dict.

        Args:
            message (str): The message to send.
            encoding (str): The encoding to use for the message.
        """
        for host, ports in self._host_ports_dict.items():
            for port in ports:
                self.send_message(message, host, port, encoding)
