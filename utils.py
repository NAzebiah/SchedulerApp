import csv
from tempfile import NamedTemporaryFile

import pymysql
import requests

from settings import DB_HOST, DB_USER, DB_PORT, DB_PASSWORD, DB_DATABASE


def get_connection() -> pymysql.Connection:
    """
    Returns a connection to the database

    :return:
    """
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        port=DB_PORT,
        password=DB_PASSWORD,
        db=DB_DATABASE,
        cursorclass=pymysql.cursors.DictCursor
    )


def initialize_table(connection: pymysql.Connection, table_name: str, recreate: bool=False):
    """
    Initializes the remote table.

    When `recreate` parameter is True, it drops the table if it exists.
    :param connection: pymysql.Connection - connection to the database
    :param table_name: str - name of ther table
    :param recreate: bool - whether to drop the table
    :return:
    """

    with connection.cursor() as cursor:
        if recreate:
            cursor.execute(f"""
            DROP TABLE IF EXISTS `{table_name}`
            """)
            connection.commit()

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS `{table_name}` (
            `airline_id` int(11) NOT NULL,
            `name` varchar(100) NOT NULL,
            `alias` varchar(30),
            `iata` varchar(3) NOT NULL,
            `icao` varchar(10) NOT NULL,
            `callsign` varchar(50),
            `country` varchar(50) NOT NULL,
            `active` varchar(1) NOT NULL
        )
        """)
    connection.commit()


def download_file(url: str) -> str:
    """
    Downloads file, returns path under which the file is stored
    :param url: str - source URL
    :return: str - temporary file path
    :raises:
        requests.HTTPError: url returned non-200 code
    """

    temporary_file = NamedTemporaryFile(delete=False)
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        raise requests.HTTPError(f'URL returned {r.status_code} code')

    for chunk in r.iter_content(1024):
        temporary_file.write(chunk)
    temporary_file.close()

    return temporary_file.name


def insert_from_file(connection: pymysql.Connection, table_name: str, file_path: str) -> None:
    """
    Inserts a csv file into database

    :param connection: pymysql.Connection - connection to the database
    :param table_name: str - table name where to insert the data
    :param file_path: str - full file path to the file
    :return:
    """
    with open(file_path, 'r') as file, connection.cursor() as cursor:
        reader = csv.reader(file)
        for line in reader:
            cursor.execute(f"""
            REPLACE INTO {table_name} (airline_id, name, alias, iata, icao, callsign, country, active) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, tuple(line))

    connection.commit()