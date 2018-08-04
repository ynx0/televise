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
            img = numpy.array(sct.grab(monitor_region))
            img = serialize_blosc(img)
            # pub.send_pyobj(img)
            pub.send_multipart([Topics.FRAME_EVENT, img])
            # print("Sending img" + str(img))
            if kbd.is_pressed('ctrl+alt+/'):
                logger.info("Exitting due to quit hotkey")
                break


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.debug("Exitting due to Ctrl+C")
