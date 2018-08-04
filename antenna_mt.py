import sys
import time
from queue import Queue, Empty
import cv2
import zmq
from logzero import logger
import threading
from common import Topics, host, sub_port, deserialize_blosc

passive = False
port = None
buffer_length = 5
frame_num = 0
frame_buffer = Queue(maxsize=buffer_length)
num_threads = 5

try:
    port = int(sys.argv[0])
except ValueError:
    port = sub_port
    logger.warn("No port provided, falling back to port %s set in common.py file" % port)


# worker

def recv_and_process():
    global frame_num
    ctx = zmq.Context.instance()
    # noinspection PyUnresolvedReferences
    sub = ctx.socket(zmq.SUB)
    sub.connect('tcp://%s:%s' % (host, port))
    sub.subscribe(topic=Topics.FRAME_EVENT)
    logger.info("Subscribing to to: %s:%s" % (host, sub_port))

    while True:
        # noinspection PyUnusedLocal
        [topic, frame] = sub.recv_multipart()  # multipart appears to have better performance
        frame_num += 1
        logger.info("Recieved frame no" + str(frame_num))

        if not frame_buffer.full():  # safety check
            frame_buffer.put(frame)
        else:
            logger.warn("Oh no, frame %s skipped" % frame_num)

        time.sleep(0.01)


def show_img():
    for i in range(num_threads):
        thread = threading.Thread(target=recv_and_process)
        thread.daemon = True  # fixes control c https://stackoverflow.com/a/11816038/3807967
        thread.start()  # however, this is not best b/c doesn't always clean up resources/handles etc.

    while True:
        global frame_num
        last_time = time.time() + 0.000001
        if not frame_buffer.empty():
            # while not frame_buffer.empty(): # can't use nested loop b/c it interferes with cv2.waitkey,
            # which is needed other wise it screws everything up.
            # here, we keep the frame serialized to save memory
            # until we really need it, then we unserialize it/decompress it
            try:
                b = frame_buffer.get(block=False)
                img = deserialize_blosc(b)
                cv2.imshow('OpenCV/Numpy normal', img)
            except Empty:
                logger.warn("No frames in framebuffer when expected")

        print('fps: {0}'.format(1 / (time.time()-last_time)))

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    try:
        show_img()
    except KeyboardInterrupt:

        logger.debug("Quitting due to Ctrl+C")
