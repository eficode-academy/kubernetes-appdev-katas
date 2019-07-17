
import argparse
import flask
import random
import requests
import prometheus_client

age_app = flask.Flask('age')
name_app = flask.Flask('name')
sentence_app = flask.Flask('sentence')

@age_app.route('/')
def get_age():
    m_requests.labels('age').inc()
    return str(random.randint(0,100))

@name_app.route('/')
def get_name():
    m_requests.labels('name').inc()
    return random.choice(['Graham', 'John', 'Terry', 'Eric', 'Michael'])

@sentence_app.route('/')
def get_sentence():
    age = requests.get(sentence_app.config['age-service'], timeout=1).text
    name = requests.get(sentence_app.config['name-service'], timeout=1).text
    m_requests.labels('sentence').inc()
    return '{} is {} years'.format(name, age)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['sentence', 'age', 'name'], help="Select role for the program")
    parser.add_argument('--delay', default=0, type=int)
    parser.add_argument('--age-service', default='http://127.0.0.1:8888')
    parser.add_argument('--name-service', default='http://127.0.0.1:8889')
    parser.add_argument('--server-address', default='0.0.0.0:5000')

    args = parser.parse_args()

    host, port = args.server_address.split(':')
    port = int(port)

    # See for naming: https://prometheus.io/docs/practices/naming/
    m_requests = prometheus_client.Counter('sentence_requests_total',
                                           'Number of requests', ['type'])
    # Metrics will be served on port 8000
    prometheus_client.start_http_server(8000)

    if args.mode=='age':
        age_app.run(host=host, port=port)
    elif args.mode=='name':
        name_app.run(host=host, port=port)
    elif args.mode=='sentence':
        sentence_app.config['name-service'] = args.name_service
        sentence_app.config['age-service'] = args.age_service
        sentence_app.run(host=host, port=port)
