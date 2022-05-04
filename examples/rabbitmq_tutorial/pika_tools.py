import pika

credentials = pika.PlainCredentials(
    username='user',
    password='pass',
    erase_on_connect=True
)
connection_params = pika.ConnectionParameters(
    host="localhost",
    port=5672,
    credentials=credentials,
)


def get_channel():
    connection = pika.BlockingConnection(connection_params)
    return connection.channel()

def close_channel(channel):
    return channel.connection.close()

