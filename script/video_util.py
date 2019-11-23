import cv2
from enum import Enum
import numpy as np
import threading


class DisplayType(Enum):
    VGA = (640, 480)
    HDTV720p = (1280, 720)
    HDTV1080p = (1920, 1080)


class VideoCaptureParams:
    def __init__(self):
        self.size = DisplayType.VGA.value
        self.fps = 30


def global_video_param():
    return VideoCaptureParams()


def global_frame_shape():
    param = global_video_param()
    return [param.size[1], param.size[0], 3]


class CustomVideoCapture:
    def __init__(self, capture_id=0, debug_mode=False):
        capture_params = global_video_param()
        video_capture = cv2.VideoCapture(capture_id)
        video_capture.set(cv2.CAP_PROP_FPS, capture_params.fps)
        video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, capture_params.size[0])
        video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, capture_params.size[1])
        video_capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.__capture = video_capture
        self.__debug_mode = debug_mode

        # debug print if needed
        self.__print_if_needed()

    def __print_if_needed(self):
        # if debug_mode is true, video capture parameters are printed.
        if self.__debug_mode:
            print("fps : {}, capture width : {}, capture height : {}".format(
                self.__capture.get(cv2.CAP_PROP_FPS),
                self.__capture.get(cv2.CAP_PROP_FRAME_WIDTH),
                self.__capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
            ))

    def get_frame(self, is_rgb=False):
        ret, frame = self.__capture.read()

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        if is_rgb is True:
            frame = frame[:, :, ::-1]
        return frame

    def destroy(self):
        self.__capture.release()
        cv2.destroyAllWindows()


class VideoUtil:
    @classmethod
    def get_scale_frame(cls, frame, reduction_ratio=4):
        return cv2.resize(frame, (0, 0), fx=1 / reduction_ratio, fy=1 / reduction_ratio)

    @classmethod
    def convert_frame_from_bytes(cls, frame_bytes, shape):
        # dtype of frame ndarray is 'uint8'
        tmp_array = np.frombuffer(frame_bytes, dtype="uint8")
        return tmp_array.reshape(shape)

    @classmethod
    def convert_bytes_from_frame(cls, frame):
        return frame.tobytes()

    @classmethod
    def draw_frame(cls, title, frame):
        cv2.imshow(title, frame)
        cv2.waitKey(1)  # need to call waitkey to show image

    @classmethod
    def save_frame(cls, path, frame):
        cv2.imwrite(path, frame)
