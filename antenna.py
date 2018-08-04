import sys
import time

import cv2
import zmq
from logzero import logger

from common import Topics, host, sub_port, deserialize_blosc

passive = False
port: int = None
try:
    port = int(sys.argv[0])
except ValueError:
    port = sub_port
    logger.warn("No port provided, falling back to port %s set in common.py file" % port)


def main():
    ctx = zmq.Context()
    sub = ctx.socket(zmq.SUB)

    logger.info("Subscribing to to: %s:%s" % (host, sub_port))

    sub.connect('tcp://%s:%s' % (host, port))
    sub.subscribe(topic=Topics.FRAME_EVENT)
    while True:

        last_time = time.time()
        [topic, frame] = sub.recv_multipart()  # appears to have better performance
        frame = deserialize_blosc(frame)

        # logger.info("Recieved frame")
        # print(str(frame))
        cv2.imshow('OpenCV/Numpy normal', frame)
        print('fps: {0}'.format(1 / (time.time()-last_time)))

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.debug("Quitting due to Ctrl+C")
