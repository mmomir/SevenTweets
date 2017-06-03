from fabric.api import local, env

# env.host = ["import.sedamcvrkuta.com"]
# env.host = ["http://192.168.99.100"]
# env.user = "root"

name = "SevenTweets"
port = 5000
repository = "SevenTweets"
network = "radionica"
db_container_name = "radionica-postgres"
db_user = "radionica"
db_name = "radionica"
image_tag = "testim"
db_port = 5432
app_interface = '0.0.0.0'
app_port = 80

service_container_name = 'seventweets'


def build(tag=""):
    # if tag is not "" :
    #     tag = ":" + tag
    local("docker build . -t {}".format(tag))


def run(docker, image):
    local("docker run -d --name {} --net radionica -p 0.0.0.0:5000:5000 {}".format(docker, image))


def create_network():
    local("docker network crate {}".format(network))


def migrate(image=image_tag):
    local('docker run '
          '--rm '
          '--net {} '
          '-e ST_DB_USER={} -e ST_DB_PASS={} '
          '-e ST_DB_HOST={} '
          '-e ST_DB_NAME={} '
          '{} '
          'python3 __main__.py migrate'.format(network, db_user, None, db_container_name, db_name, image))


def start_service(image):
    local('docker run -d '
          '--name {} '
          '--net {} '
          '-e ST_DB_USER={} '
          '-e ST_DB_HOST={} '
          '-e ST_DB_NAME={} '
          '-e ST_DB_PORT={} '
          '-e ST_DB_PASS={} '
          '-e ST_API_TOKEN={} '
          '-p {}:{}:{} '
          '{} '
          'python3 __main__.py runserver -i {} -p {}'.format(
        service_container_name, network, db_user,
        db_container_name, db_name, db_port, None, 1234, app_interface, port,
        port, image, app_interface, port))

def start_service1(image):
    local('docker run -d '
          '--name {} '
          '--net {} '
          '-e ST_DB_USER={} '
          '-e ST_DB_HOST={} '
          '-e ST_DB_NAME={} '
          '-e ST_DB_PORT={} '
          '-e ST_DB_PASS={} '
          '-e ST_API_TOKEN={} '
          '-p {}:{}:{} '
          '{} '
          'python3 __main__.py runserver -i {} -p {}'.format(
        'docker_1', 'radionica_1', 'radionica_1',
        'radionica-postgres_1', 'radionica_1', 5432, None, 1234, app_interface, 6000,
        6000, image, app_interface, 6000))

def start_service2(image):
    local('docker run -d '
          '--name {} '
          '--net {} '
          '-e ST_DB_USER={} '
          '-e ST_DB_HOST={} '
          '-e ST_DB_NAME={} '
          '-e ST_DB_PORT={} '
          '-e ST_DB_PASS={} '
          '-e ST_API_TOKEN={} '
          '-p {}:{}:{} '
          '{} '
          'python3 __main__.py runserver -i {} -p {}'.format(
        'docker_2', 'radionica_2', 'radionica_2',
        'radionica-postgres_2', 'radionica_2', 5432, None, 1234, app_interface, port,
        port, image, app_interface, port))

def migrate_1(image=image_tag):
    local('docker run '
          '--rm '
          '--net {} '
          '-e ST_DB_USER={} -e ST_DB_PASS={} '
          '-e ST_DB_HOST={} '
          '-e ST_DB_NAME={} '
          '{} '
          'python3 __main__.py migrate'.format('radionica_1', 'radionica_1', None, 'radionica-postgres_1', 'radionica_1', image))

def migrate_2(image=image_tag):
    local('docker run '
          '--rm '
          '--net {} '
          '-e ST_DB_USER={} -e ST_DB_PASS={} '
          '-e ST_DB_HOST={} '
          '-e ST_DB_NAME={} '
          '{} '
          'python3 __main__.py migrate'.format('radionica_2', 'radionica_2', None, 'radionica-postgres_2', 'radionica_2', image))

def db_create_1():
    local('docker run '
          '-d '
          '--name {} '
          '--net {} '
          '-e POSTGRES_USER={} '
          '-e POSTGRES_PASSWORD={} '
          '-p 127.0.0.1:5432:5432 '
          'postgres:9.6.2'.format('radionica-postgres_1', 'radionica_1','radionica_1',None)
          )

def db_create_2():
    local('docker run '
          '-d '
          '--name {} '
          '--net {} '
          '-e POSTGRES_USER={} '
          '-e POSTGRES_PASSWORD={} '
          '-p 127.0.0.1:5431:5432 '
          'postgres:9.6.2'.format('radionica-postgres_2', 'radionica_2','radionica_2',None)
          )

def create_network_1():
    local("docker network create radionica_1")

def create_network_2():
    local("docker network create radionica_2")