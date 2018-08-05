import time

import numpy
import keyboard as kbd
import mss
import zmq
from common import pub_port, serialize_blosc, Topics
from logzero import logger
from screeninfo import get_monitors


def main():
    ctx = zmq.Context()
    # noinspection PyUnresolvedReferences
    pub = ctx.socket(zmq.PUB)
    pub.bind('tcp://*:%s' % pub_port)
    logger.info('Publishing on port: %s' % pub_port)

    monitor = get_monitors()[0]
    width, height = monitor.width, monitor.height
    monitor_region = {'top': 0, 'left': 0, 'width': width, 'height': height}

    with mss.mss() as sct:
        while True:
            last_time = time.time() + 0.00001
            img = numpy.array(sct.grab(monitor_region))
            img = serialize_blosc(img)

            pub.send_multipart([Topics.FRAME_EVENT, img])

            if kbd.is_pressed('ctrl+alt+/'):
                logger.info("Exitting due to quit hotkey")
                break

            print('fps: {0}'.format(1 / (time.time() - last_time)))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.debug("Exitting due to Ctrl+C")
