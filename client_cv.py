import cv2 
import socket 
import pickle

def main(args):
    # create a socket for streaming
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)

    # local host ip and port
    client_ip = args.client_ip
    client_port = args.client_port

    # create video capture object
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.vid_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.vid_height)
    cap.set(cv2.CAP_PROP_FPS, args.fps)

    while True:
        # capture the video
        ret, frame = cap.read()

        # encode video frame as a jpeg
        ret, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])

        # turn it into bytes
        x_as_bytes = pickle.dumps(buffer)

        # send the bytes over the client ip address
        s.sendto((x_as_bytes), (client_ip, client_port))

        if cv2.waitKey(5) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    import argparse

    # setup the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'client_ip', type=str, help='The IP of the client device'
    )
    parser.add_argument(
        'client_port', type=int, help="The port of the client device"
    )
    parser.add_argument(
        '--height', type=int, default=224, help='Height of the camera output'
    )
    parser.add_argument(
        '--width', type=int, default=224, help='Width of the camera output'
    )
    parser.add_argument(
        '--fps', type=int, default=30, help='FPS of the camera live stream'
    )
    args = parser.parse_args()

    main(args)
