import faust
import random

app = faust.App(
    'sample-stream-process',
    broker='kafka://localhost:9092',
    value_serializer='raw',
)

topic_a = app.topic('topic_a', value_type=str)
topic_b = app.topic('topic_b', value_type=str)


@app.agent(topic_a)
async def process_data(records):
    async for record in records:
        await topic_b.send(value=record)


@app.agent(topic_b)
async def consume_final_output(records):
    async for record in records:
        data = int(record) + random.randint(1, 100)
        print("data is {}".format(data))


#@app.timer(1)
#async def send_data_interval():
#    await topic_a.send(value="1")


@app.task
async def producer():
    while True:
        try:
            await topic_a.send(value="1")
        except Exception as e:
            print(e.args)
            break

        if 0xFF == ord('q'):
            break


if __name__ == "__main__":
    app.main()
