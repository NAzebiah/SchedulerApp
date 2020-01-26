import argparse
import logging
import os

from settings import DB_TABLE
from utils import get_connection, initialize_table, download_file, insert_from_file

logging.getLogger().addHandler(logging.StreamHandler())
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pull file from URL and add content to database.')
    parser.add_argument('--initialize-table', dest='initialize_table', action='store_true',
                        help='Non-destructive table initialization - if table exists, nothing happens.')
    parser.add_argument('--initialize-table-recreate', dest='initialize_table_recreate', action='store_true',
                        help='WARNING: deletes the table and creates it once again.')
    parser.add_argument('--url', dest='url', help='URL from which to pull the file', required=True)

    args = parser.parse_args()

    connection = get_connection()

    if args.initialize_table or args.initialize_table_recreate:
        logger.info(f'Initializing table, recreating: {args.initialize_table_recreate}')
        initialize_table(connection, DB_TABLE, args.initialize_table_recreate)

    temporary_file_path = download_file(args.url)
    insert_from_file(connection, DB_TABLE, temporary_file_path)

    # cleanup
    if os.path.exists(temporary_file_path):
        os.remove(temporary_file_path)
