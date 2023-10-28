import cv2 
import socket 
import pickle

def main(args):

    # setup socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # https information
    client_ip = args.client_ip
    client_port = args.client_port
    s.bind((client_ip, client_port))

    while True:
        # receive the bytes over the stream
        x = s.recvfrom(1000000)
        data = x[0]

        # load the image from encoded stream
        data = pickle.loads(data)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)

        # show the image on the server
        cv2.imshow('Img Server', img)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
    
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
    args = parser.parse_args()

    main(args)
