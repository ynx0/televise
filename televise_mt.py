# from queue import Queue
#
# import threading
# import mss
# import numpy
# import time
# import zmq
# from logzero import logger
# from screeninfo import get_monitors
#
# from common import pub_port, serialize_blosc, Topics
#
# monitor = get_monitors()[0]
# width, height = monitor.width, monitor.height
# monitor_region = {'top': 0, 'left': 0, 'width': width, 'height': height}
#
# num_threads = 5
# buffer_length = 5
# frame_buffer = Queue(maxsize=buffer_length)
#
# # DON"T USE, it SUCKS
#
#
# def gimme_screen():
#     with mss.mss() as sct:
#         while True:
#             img = numpy.array(sct.grab(monitor_region))
#             img = serialize_blosc(img)
#             if not frame_buffer.full():
#                 frame_buffer.put(img)
#             else:
#                 logger.warn("Skipped sending frame")
#             time.sleep(0.001)
#
#
# def main():
#     ctx = zmq.Context()
#     # noinspection PyUnresolvedReferences
#     pub = ctx.socket(zmq.PUB)
#     pub.bind('tcp://*:%s' % pub_port)
#     logger.info('Publishing on port: %s' % pub_port)
#
#     for i in range(num_threads):
#         t = threading.Thread(target=gimme_screen)
#         t.daemon = True
#         t.start()
#
#     while True:
#         last_time = time.time() + 0.00001
#         if not frame_buffer.empty():
#             pub.send_multipart([Topics.FRAME_EVENT, frame_buffer.get()])
#
#         print('fps: {0}'.format(1 / (time.time() - last_time)))
#
#
# if __name__ == '__main__':
#     try:
#         main()
#     except KeyboardInterrupt:
#         logger.debug("Exitting due to Ctrl+C")
