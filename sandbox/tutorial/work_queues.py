from random import randint
import time
import pika
import argparse
import threading

import tools

QUEUE_NAME = "task_queue"
DURABLE = True


def boss(num_tasks):
    channel = tools.get_channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=DURABLE)

    for _ in range(num_tasks):
        task_length = randint(1, 5)
        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=str(task_length),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(" [x] Sent task of length %d" % task_length)

    tools.close_channel(channel)

def worker(worker_name):
    channel = tools.get_channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    print(' [*] %s started, reporting for duty!' % worker_name)

    def callback(ch, method, properties, body):
        print(" [x] %s received %r" % (worker_name, body.decode()))
        time.sleep(int(body))
        print(" [x] Done")

        # acknowledge that task has been completed
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # distribute to the next available connsumer, no round robin bs
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    channel.start_consuming()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tasks", type=int, default=1, help="Number of tasks for workers to complete")
    parser.add_argument("-w", "--workers", type=int, default=1, help="Number of workers to run a time")
    args = parser.parse_args()

    if args.workers <= 0:
        raise ValueError("There must be at least one worker running in this example")
    elif args.tasks <= 0:
        raise ValueError("You must assign at least one task")

    # use threads to allow multiple blocking connections
    threads = []
    boss_thread = threading.Thread(name="producer-1", target=boss, args=(args.tasks,))
    threads.append(boss_thread)

    for i in range(args.workers):
        worker_name = f"worker-{i}"
        worker_thread = threading.Thread(name=worker_name, target=worker, args=(worker_name,))
        threads.append(worker_thread)

    for t in threads:
        t.start()