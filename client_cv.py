from obj_seg import *
import time
from torchvision.models.detection import ssdlite320_mobilenet_v3_large as SSDLite
import socket 
import pickle
import ssl

# turn off ssl verification
ssl._create_default_https_context = ssl._create_unverified_context

def main(args):
    # load the model
    model = SSDLite(weights='DEFAULT')
    model.eval()

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

        if ret == True:
            # fps calculation
            start_time = time.time()

            # get the prediction from the model
            box = predict(frame, model, args.detection_threshold)
            
            # fps calculation
            end_time = time.time()
            fps = 1 / (end_time - start_time)
            print(f"{fps: .3f} FPS")

            # encode video frame as a jpeg
            _ , buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])

            # turn it into bytes
            x_as_bytes = pickle.dumps(buffer)

            # send the bytes over the client ip address
            s.sendto((x_as_bytes), (client_ip, client_port))

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
