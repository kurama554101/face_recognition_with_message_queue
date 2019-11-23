from abc import ABCMeta, abstractmethod
import cv2
import os
import csv
import numpy as np
import face_recognition
from face_recognition_util import get_face_information
from enum import Enum


class FaceModelUtil:
    @classmethod
    def draw_boxes_into_frame(cls, frame, face_locations, face_names, reduction_ratio):
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= reduction_ratio
            right *= reduction_ratio
            bottom *= reduction_ratio
            left *= reduction_ratio

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


class FaceModelType(Enum):
    REMOTE = 0,
    LOCAL = 1


class FaceRecognitionResultOfOneFrame:
    def __init__(self, face_locations, face_names):
        self.face_locations = face_locations
        self.face_names = face_names


class AbstractFaceModel:
    __metaclass__ = ABCMeta

    def __init__(self):
        # TODO : imp
        pass

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def run(self, frames):
        pass


class LocalFaceModel(AbstractFaceModel):
    def __init__(self,
                 face_image_folder=os.path.join("data", "face_data"),
                 face_csv=os.path.join("data", "face_list.csv"),
                 debug_mode=False):
        super(LocalFaceModel, self).__init__()
        self.__face_image_folder = face_image_folder
        self.__face_csv = face_csv
        self.__debug_mode = debug_mode

        # local values
        self.__known_face_encodings = []
        self.__known_face_names = []

    def setup(self):
        self.__load_face_image()

    def __load_face_image(self):
        # read csv to load face image
        with open(self.__face_csv, "r") as f:
            reader = csv.reader(f, delimiter=",", quotechar='"')
            for row in reader:
                face_file_name = row[0]
                face_name = row[1]
                face_file_path = os.path.join(self.__face_image_folder, face_file_name)

                # check the cache data of face encoding
                face_encoding_cache_path_without_ext = \
                    os.path.join(self.__face_image_folder, os.path.splitext(os.path.basename(face_file_name))[0])
                face_encoding_cache_path = face_encoding_cache_path_without_ext + ".npy"
                if os.path.exists(face_encoding_cache_path):
                    if self.__debug_mode:
                        print(
                            "{} file is exist! face encoding data is loaded from it.".format(face_encoding_cache_path))

                    # load face encoding from cache data
                    encoding = np.load(face_encoding_cache_path)
                else:
                    # create face encoding
                    image = face_recognition.load_image_file(face_file_path)
                    encoding = face_recognition.face_encodings(image)[0]

                    # save cache data
                    np.save(face_encoding_cache_path_without_ext, encoding)

                # set face data into list
                self.__known_face_encodings.append(encoding)
                self.__known_face_names.append(face_name)

        # print face list if debug_mode is true
        if self.__debug_mode:
            print("face data count is {}".format(len(self.__known_face_names)))

    def run(self, frames):
        results = []
        for frame in frames:
            face_locations, face_names = get_face_information(frame,
                                                              self.__known_face_encodings,
                                                              self.__known_face_names)
            result = FaceRecognitionResultOfOneFrame(face_locations=face_locations, face_names=face_names)
            results.append(result)
        return results

