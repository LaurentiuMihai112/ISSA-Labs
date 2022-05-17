import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 55000  # Port to listen on (non-privileged ports are > 1023)
MESSAGE_SIZE = 3 * 4 + 500


class Package:
    def __init__(self, message_id, sequence_counter, payload, crc32):
        self.message_id = message_id
        self.sequence_counter = sequence_counter
        self.payload = payload
        self.crc32 = crc32

    def __repr__(self):
        return f"\nid={self.message_id} ; sequence_counter={self.sequence_counter} ; payload[500] ; crc={self.crc32}"


def is_ordered(package_list):
    if len(package_list) != 3:
        return False
    return package_list[0].message_id == 1 and package_list[1].message_id == 2 and package_list[2].message_id == 3


def show(item_list):
    for item in item_list:
        print(item)
        print()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((HOST, PORT))
    synchronized_packages = []
    packages = {}
    while True:
        data = server.recv(MESSAGE_SIZE)
        message_id = int.from_bytes(data[:4], 'big')
        sequence_counter = int.from_bytes(data[4:8], 'big')
        payload = []
        for i in range(8, 508, 4):
            payload.append(int.from_bytes(data[i:i + 4], 'big'))
        crc32 = int.from_bytes(data[-4:], 'big')
        package = Package(message_id, sequence_counter, payload, crc32)
        if packages.get(sequence_counter):
            packages[sequence_counter].append(package)
        else:
            packages[sequence_counter] = [package]
        package_list = packages[sequence_counter]
        if is_ordered(package_list):
            synchronized_packages.append(package_list)
        if len(synchronized_packages) == 4:
            synchronized_packages = synchronized_packages[-3:]
        print(f"Synchronized packages : ")
        show(synchronized_packages)


if __name__ == '__main__':
    main()
