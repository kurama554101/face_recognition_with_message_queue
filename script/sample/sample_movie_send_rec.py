import faust
import cv2

app = faust.App(
    'sample-movie',
    broker='kafka://localhost:9092',
    value_serializer='raw',
)


image_topic = app.topic('image_topic', value_type=bytes)


@app.agent(image_topic)
async def consume_images(records):
    async for record in records:
        print("image byte length is {}".format(len(record)))


@app.task()
async def send_image_from_camera():
    # get capture
    capture = get_capture()

    while True:
        ret, frame = capture.read()
        frame = frame[:, :, ::-1]

        # create record
        await image_topic.send(
            value=frame.tobytes(),
        )

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def get_capture():
    video_capture = cv2.VideoCapture(0)
    video_capture.set(cv2.CAP_PROP_FPS, 30)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    video_capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    return video_capture


if __name__ == "__main__":
    # start worker
    app.main()

    # destroy
    cv2.destroyAllWindows()
