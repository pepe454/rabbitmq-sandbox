import argparse
import threading

import pika_tools

TEST_QUEUE = "hello"
DURABLE = False

def producer():
    channel = pika_tools.get_channel()
    channel.queue_declare(queue=TEST_QUEUE, durable=DURABLE)
    channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
    print(" [x] Sent 'Hello World!'")
    pika_tools.close_channel(channel)

def consumer():
    channel = pika_tools.get_channel()
    channel.queue_declare(queue=TEST_QUEUE, durable=DURABLE)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=TEST_QUEUE, on_message_callback=callback, auto_ack=False)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--producer", action="store_true", help="Run producer")
    parser.add_argument("-o", "--consumer", action="store_true", help="Run consumer")
    args = parser.parse_args()

    # use threads to allow multiple blocking connections
    threads = []
    if args.producer:
        producer_thread = threading.Thread(name="producer-1", target=producer)
        threads.append(producer_thread)
    if args.consumer:
        consumer_thread = threading.Thread(name="consumer-1", target=consumer)
        threads.append(consumer_thread)

    # start and join
    for t in threads:
        t.start()

