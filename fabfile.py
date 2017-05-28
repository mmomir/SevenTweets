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
            '-e ST_DB_USER={} '
            '-e ST_DB_HOST={} '
            '-e ST_DB_NAME={} '
            '{} '
            'python3 -m migrate'.format(network, db_user, db_container_name, db_name, image))
