from utils import predict, load_capture, load_jit_model
import cv2
import time
    
def main(args):
    model = load_jit_model()

    # create video capture object
    cap = load_capture(args.vid_width, args.vid_height, args.fps)

    while True:
        # capture the video
        ret, frame = cap.read()

        if ret == True:
            # get the boxes from model prediction
            coord = predict(frame, model, args.detection_threshold)

            # if len(coord) != 1 then don't move
            # else then move the servo by arcsin(relative-distance)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
 
        else:
            print("Not reading the camera input.")
            break
    
    cap.release()

if __name__ == "__main__":
    import argparse

    # setup the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--detection_threshold', type=float, default=0.8, help='The minimum scores before output'
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
