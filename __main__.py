import sys
import argparse
import logging
from application import app
from migrations import migrate

LOG_FORMAT = ('%(asctime)-15s %(levelname)s: '
              '%(message)s [%(filename)s:%(lineno)d]')


logger = logging.getLogger(__name__)


def main(argv):

    logging.basicConfig(
        level=logging.DEBUG,
        format=LOG_FORMAT,
    )

    logger.info('Starting seventweets with parameters: %s', ', '.join(argv))

    parser = argparse.ArgumentParser(
        description=__doc__)
    subparsers = parser.add_subparsers(dest="command")
    run_parser = subparsers.add_parser('runserver')
    run_parser.add_argument('-p', '--port', dest='port', default='5000',
                            type=int,
                            metavar='PORT', help='Port to listen on.')
    run_parser.add_argument('-i', '--interface', dest='interface',
                            default='127.0.0.1', metavar='HOST',
                            help='Interface to listen on.')
    migrate_parser = subparsers.add_parser('migrate')

    migrate_parser.add_argument('-d', '--direction', dest='direction',
                                choices=['up', 'down'], default='up',
                                metavar='DIRECTION',
                                help='To perform up or down migrations.')

    args = parser.parse_args(argv)
    if args.command == 'migrate':
        migrate(args.direction)
    elif args.command == 'runserver':
        app.run(host=args.interface, port=args.port)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
