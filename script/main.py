import faust
from face_model import LocalFaceModel, FaceModelUtil
from video_util import CustomVideoCapture, VideoUtil, global_frame_shape
from aiostream import stream

# setup App
app = faust.App(
    'stream-process-with-ml',
    broker='kafka://localhost:9092',
    value_serializer='raw',
)

# setup Topic
img_frame_topic = app.topic('img_frame_topic', value_type=bytes)
trans_img_frame_topic = app.topic('trans_img_frame_topic', value_type=bytes)

# setup model
model = LocalFaceModel()
video_capture = CustomVideoCapture()
frame_shape = global_frame_shape()


# setup Function
@app.agent(img_frame_topic)
async def process_data(frame_stream):
    print("process_data : data type is {}".format(type(frame_stream)))

    # convert frames from bytes
    frame_queue = []
    async for frame_of_byte in frame_stream:
        frame = VideoUtil.convert_frame_from_bytes(frame_of_byte, shape=frame_shape)
        frame_queue.append(frame)

        # inference
        results = model.run(frame_queue)

        # draw frame with bounding box
        async for key, frame in stream.enumerate(stream.iterate(frame_queue)):
            # draw box
            face_locations = results[key].face_locations
            face_names = results[key].face_names
            FaceModelUtil.draw_boxes_into_frame(frame,
                                                face_locations=face_locations,
                                                face_names=face_names,
                                                reduction_ratio=1)  # TODO : get reduction_ratio
            await trans_img_frame_topic.send(value=VideoUtil.convert_bytes_from_frame(frame))
        frame_queue.clear()


@app.task
async def capture_from_camera():
    while True:
        try:
            frame = video_capture.get_frame()
            frame_bytes = VideoUtil.convert_bytes_from_frame(frame)
            await img_frame_topic.send(value=frame_bytes)
        except Exception as e:
            print(e.args)
            break

        if 0xFF == ord('q'):
            break


if __name__ == "__main__":
    # setup
    model.setup()

    # start main loop
    app.main()
