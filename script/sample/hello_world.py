import faust

app = faust.App(
    'hello-world',
    #broker='kafka://172.17.0.3:9092',
    broker='kafka://localhost:9092',
    value_serializer='raw',
)

greetings_topic = app.topic('greetings')


# TOPICにデータが格納された実行される（Consumer処理）
@app.agent(greetings_topic)
async def greet(greetings):
    async for greeting in greetings:
        print(greeting)


# 定期的に実行する処理
@app.timer(1)
async def greet_send():
    await greetings_topic.send(key="fuga", value="hoge")


if __name__ == "__main__":
    # appに登録した処理（agent, timer）をまとめて実行
    app.main()
