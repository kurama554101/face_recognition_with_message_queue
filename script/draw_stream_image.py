from aiokafka import AIOKafkaConsumer
import asyncio
from video_util import VideoUtil, global_frame_shape


async def consume_frame_stream(loop):
    consumer = AIOKafkaConsumer(
        'trans_img_frame_topic',
        loop=loop, bootstrap_servers='localhost:9092')
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            frame_shape = global_frame_shape()
            frame = VideoUtil.convert_frame_from_bytes(msg.value, shape=frame_shape)
            VideoUtil.draw_frame("test", frame)

            # if input data is q, end the process
            if 0xFF == ord('q'):
                break
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume_frame_stream(loop))


if __name__ == "__main__":
    main()
