# DigiMesh send and receive script

from digi.xbee.devices import *
from digi.xbee.devices import DigiMeshDevice
from digi.xbee.devices import RemoteDigiMeshDevice
from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.devices import XBeeNetwork
from digi.xbee.models.options import DiscoveryOptions
import time
from multiprocessing import *
from threading import *

module_number = 9
port = "COM7"
baud_rate = 38400
data_to_send = "Hello from module " + str(module_number) + "!!!"
freq = {}
freqd = {}

freq2 = [[]]
# declaring a dict for frequencies calculation

device = DigiMeshDevice(port, baud_rate)
# device = XBeeDevice(port, baud_rate)
online_remote_devices = []  # globally declaring the list variable for the remote devices

# Hard coded node identifiers and their addresses 	(although not needed
address_details = {
    '1': '0013A200419A9108',
    '2': '0013A200419A9202',
    '3': '0013A200419A90F0',
    '4': '0013A200419A9136',
    '5': '0013A200419A993B',
    '6': '0013A200419A91DC',
    '7': '0013A200419A983C',
    '8': '0013A200419A9118',
    '9': '0013A200419A9B10',
    '10': '0013A200419A990F',
    '11': '0013A200419A9230',
    '12': '0013A200419A97DA'
}


# returns 64 bit address of modules
def addr_simple(data):
    return (XBee64BitAddress.from_hex_string(data))


# returns a remote device object 	(although not needed)
def create_remote_device(data):
    temp_addr = addr_simple(data)
    return (RemoteDigiMeshDevice(device, temp_addr))


def send_synchronous(data, i):
    pkt_count = 0
    while True:

        time.sleep(0.1)

        try:
            print("Device", [i])
            device.send_data(online_remote_devices[i], data)
            print(" Sending Data packet No ", pkt_count, "to", online_remote_devices[i])
            pkt_count += 1
            ctime = time.time()
            dtime = ctime - ftime
            if dtime > 2:
                if pkt_count/dtime >= 2:
                    time.sleep(0.4)
        except Exception as err:
            print(device, "data not send  ", err, "  ")


def send_asynchronous(data, i):
    pkt_count = 0
    while True:

        time.sleep(0.1)

        try:
            print("Device", [i])
            device.send_data_async(online_remote_devices[i], data)
            # print(" Sending Data packet No ", pkt_count, "to", online_remote_devices[i])
            pkt_count += 1
        except Exception as err:
            print(device, "data not send", err)


def send_broadcast(data):
    try:
        device.send_data_broadcast(data)
    except:
        print("send_broadcast not found")


def receive_data(timeout,address_details):
    freql = [[]] * 13
    while True:
        time.sleep(0.001)
        print("in receive function")
        obj8 = device.read_data(timeout)
        data1 = obj8.data
        remote_device = obj8.remote_device
        is_broadcast = obj8.is_broadcast
        timestamp = obj8.timestamp
        print(data1)
        m1 = str(remote_device)
        x = m1.split(" ")
        hexa = str(x[0])
        print("yoyo", hexa)
        key_list = list(address_details.keys())
        val_list = list(address_details.values())

        node = key_list[val_list.index(hexa)]
        node = int(node)
        print("yoyo1", node)
        freql[node].append(timestamp)
        try:
            x1 = freql[node][-1] - freql[node][-2]
            frequency = 1 / x1
            # appending the dictionary
            print("frequency from ", node, "is ", frequency)
        except Exception as errr1:
            print("may be 1st", errr1)

def recv_data(online_remote_devices, i, timeout):
    digimesh_message = []
    freq_list = []
    k = 0
    while True:
        time.sleep(0.01)
        try:
            # digimesh_message.append(device.read_data_from(online_remote_devices[i], timeout))
            obj = device.read_data_from(online_remote_devices[i], timeout)
            data1 = obj.data
            time_rec = obj.timestamp
            try:

                freq_list.append(time_rec)
                f1 = freq_list[k] - freq_list[k - 1]

            except Exception as err_f1:
                print("maybe 1st time input", err_f1)
            k = k + 1
            f3 = 1 / f1
            print("frequency is ", str(f3), "from ", online_remote_devices[i])

            print("Device ", i, " ", data1)
        except Exception as err:
            print("error in recv_data", err)



def receive_data_specific(timeout):
    try:
        digimesh_message = []
        thrd = []
        print("In recv specific")
        for i in range(0, len(online_remote_devices)):
            thrd.append(threading.Thread(target=recv_data, args=(online_remote_devices, i, timeout)))
        for j in range(0, len(online_remote_devices)):
            thrd[j].start()
            print("starting_thread", j)

        # return (digimesh_message)
    except Exception as err:
        print("digimesh_message not found", err)
    # return (digimesh_message)


# Define callback for data reception
def my_data_received_callback(digimesh_message):
    print("At my_data_received_callback function")
    try:
        if digimesh_message != None:
            address = digimesh_message.remote_device.get_64bit_addr()
            data = digimesh_message.data.decode("utf8")

            print("Received data from " + str(address) + " ie " + str(data))
        else:
            print("data not found")
    except:
        print("my_data_received_callback not found")


def receive_with_callback():
    while True:
        # time.sleep(0.01)
        try:
            device.add_data_received_callback(my_data_received_callback)
            print("At receive_with_callback function")
        except:
            print("receive_with_callback not found")


def sendf1(online_remote_devices, data_to_send, device):
    # send data to each digi seperately and parallely (using multi threading)

    t = []
    for i in range(0, len(online_remote_devices)):
        # time.sleep(0.01)
        t.append(Thread(target=send_asynchronous, args=[data_to_send, i]))
        # t.append(Thread(target=send_asynchronous, args=[data_to_send, i]))
        print("at send function  ")

        '''t[i] = Thread(target=send_asynchronous(data_to_send), args=(data_to_send, i))


        '''

    for j in range(0, len(online_remote_devices)):
        t[j].start()


def printtab(freqd):
    while True:
        print("printing the frequency table")
        print(freqd)
        time.sleep(7)


# Connect with local device
def Main():
    while True:
        try:
            device.open()
            print("Serial communication established")
            break
        except:
            if device.is_open():
                device.close()
            else:
                print("Trying to establish serial communication...")

    # initialize and start node discovery
    digimesh_network = device.get_network()
    digimesh_network.set_discovery_options({DiscoveryOptions.APPEND_DD})
    digimesh_network.set_discovery_timeout(25)
    digimesh_network.start_discovery_process()

    flag = 0
    while digimesh_network.is_discovery_running():
        if flag == 0:
            print('discovering...')
            flag = 1
        else:
            pass

    # Make a list of online remote devices. This list has objects of the remote device type.

    for node_id in address_details:
        addr = addr_simple(address_details[node_id])
        if digimesh_network.get_device_by_64(addr) != None:
            online_remote_devices.append(digimesh_network.get_device_by_64(addr))

    print("Online Remote Devices Found: " + str(len(online_remote_devices)))
    print(online_remote_devices)

    # infinite while loop for sending and receiving
    # receive data 		(choose a method)
    '''message = receive_data()
    if message != None:
        print(message.data)'''

    '''message = receive_data_specific()
    for i in range(0,len(message)):
        if message != None:
            print(message.data)'''
    # processes is list containing each process object
    processes = []
    # process for receiving
    # process = threading.Thread(target=receive_data_specific,args={None})
    '''process = Process(target=receive_data_specific())
    process = process = Process(target=receive_data())
      '''

    # process.start()

    # send data 		(choose a method)
    # send_broadcast(data_to_send)

    # sending data sync or async (please mention in def above of sendf1) using multi processing and threading
    process2 = threading.Thread(target=sendf1, args=(online_remote_devices, data_to_send, device))
    processes.append(process2)
    process = threading.Thread(target=receive_data, args=(3, address_details))
    process.start()
    process2.start()
    process3 = threading.Thread(target=printtab, args=(freqd,))
    process3.start()

    processes.append(process)
    print("Data Sent!!!")
    time.sleep(0.5)

    # device.close()

    print("Serial communication terminated")


if __name__ == '__main__':
    Main()
