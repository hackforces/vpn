import docker
import logging
def arr_to_dict(arr, fields):
    return {fields[i]: arr[i] for i in range(0, len(arr))}

class EasyRSA:
    def __init__(self, container):
        client = docker.from_env()
        self.docker = client.containers.get(container)
        self.locked = False
        self.__fields_certs = ['name', 'begin', 'end', 'status']
        self.__fields_clients = ['name', 'remote', 'recv', 'sent', 'since']
        self.__fields_routing = ['local', 'name', 'remote', 'ref']

    def __call(self, cmd):
        while self.locked:
            continue
        self.locked = True
        result = self.docker.exec_run(cmd)
        self.locked = False
        code, message = result.exit_code, result.output.decode('utf-8')
        return code, message

    def gen(self, name):
        err, message = self.__call(f"easyrsa build-client-full {name} nopass")
        if not err and "Data Base Updated" in message:
            err, id = self.__call(f'cat /etc/openvpn/pki/serial.old')
            return id.rstrip().upper()
        # if err and "already exists" in message:
        #     return 0
        return 0

    def get(self, name):
        return self.__call(f'ovpn_getclient {name}')[1]

    def list(self):
        err, data = self.__call(f'ovpn_listclients')
        out = list()
        for client in data.split('\n')[1:-1]:
            props = client.split(',')
            op = arr_to_dict(props, self.__fields_certs)
            out.append(op)
        return out


    def revoke(self, name):
        code, s = self.__call(f'bash -c "echo -ne \"yes\" | ovpn_revokeclient {name} remove"')
        if "Revocation was successful" in s and "No such file or directory" in s:
            return s
        return 0

    def status(self):
        code, message = self.__call(f'cat /tmp/openvpn-status.log')
        data = message.split('\n')[1:-1]
        out = dict(clients=list(), routing=list(), updated="")
        if len(data) <= 4:
            return out
        out['updated'] = data.pop(0).split(',')[1] # get updated time
        data.pop(0)
        # working with connected clients
        while data[0] != 'ROUTING TABLE':
            out['clients'].append(arr_to_dict(data.pop(0).split(','), self.__fields_clients))
        # routing table for clients connected
        data = data[2:]
        while data[0] != 'GLOBAL STATS':
            out['routing'].append(arr_to_dict(data.pop(0).split(','), self.__fields_clients))
        return out

    def add(self, name):
        id = self.gen(name)
        if id == 0:
            return 0
        return dict(cert=self.get(name), id=id)
