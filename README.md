# RabbitMQ Sandbox
This is a personal project to play with RabbitMQ and develop sandbox applications.

## Project Setup Ubuntu 20.04:
```
mkdir rabbitmq-project
cd rabbitmq-project
git init
git pull origin https://github.com/pepe454/rabbitmq-sandbox.git
```
Install python: https://docs.python-guide.org/starting/install3/linux/

Install docker: https://docs.docker.com/engine/install/ubuntu/

Install rabbitmq image: https://registry.hub.docker.com/_/rabbitmq/

### Python Setup
```
pip install virtualenv
virtualenv venv .
. venv/bin/activate
pip install -r requirements.txt
```