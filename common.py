import pickle
import blosc

# host = '0.tcp.ngrok.io'
host = 'localhost'
pub_port = 2223  # the subscriber port may not necessarily be the same as the publisher port
sub_port = pub_port


# sub_port = 19353  # because of the way that ngrok forwards ports


class Topics:  # ALL TOPICS MUST BE BYTES
    FRAME_EVENT = bytes(0)  # differentiate from
    # topics range for televise is from 200-300


# https://pyzmq.readthedocs.io/en/latest/serialization.html#using-your-own-serialization
def send_blosc_pickle(socket, obj, flags=0, protocol=-1):
    p = pickle.dumps(obj, protocol)
    b = blosc.compress(p)
    return socket.send(b, flags=flags)


def recv_blosc_pickle(socket, flags=0):
    cmp = socket.recv(flags)
    b = blosc.decompress(cmp)
    p = pickle.loads(b)
    return p


def serialize_blosc(obj):
    p = pickle.dumps(obj)
    b = blosc.compress(p)
    return b


def deserialize_blosc(obj):
    b = blosc.decompress(obj)
    p = pickle.loads(b)
    return p
