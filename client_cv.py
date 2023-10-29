import cv2
import socket 
import pickle
import torch
from obj_seg import load_model, predict

def load_capture(vid_width, vid_height, fps):
    # create video capture object
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, vid_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, vid_height)
    cap.set(cv2.CAP_PROP_FPS, fps)

    return cap

def send_data(box, buffer, socket, ip, port):
    # turn it into bytes
    data_dict = {
        'frame': buffer,
        'box': box
    }

    x_as_bytes = pickle.dumps(data_dict)

    # send the bytes over the client ip address
    socket.sendto((x_as_bytes), (ip, port))

def main(args):
    model = load_model()

    # create a socket for streaming
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)

    # local host ip and port
    client_ip = args.client_ip
    client_port = args.client_port

    # create video capture object
    cap = load_capture(args.vid_width, args.vid_height, args.fps)

    while True:
        # capture the video
        ret, frame = cap.read()

        if ret == True:
            # encode video frame as a jpeg
            _ , buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), args.fps])
            with torch.no_grad():
                box = predict(frame, model, args.detection_threshold)

            # send data
            send_data(box, buffer, s, client_ip, client_port)

            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
 
        else:
            print("Not reading the camera input.")
            break
    
    cap.release()
    cv2.destroyAllWindows()

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
        '--detection_threshold', type=float, default=0.6, help='The minimum scores before output'
    )
    parser.add_argument(
        '--vid_height', type=int, default=224, help='Height of the camera output'
    )
    parser.add_argument(
        '--vid_width', type=int, default=224, help='Width of the camera output'
    )
    parser.add_argument(
        '--fps', type=int, default=30, help='FPS of the camera live stream'
    )
    args = parser.parse_args()

    main(args)
