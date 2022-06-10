from typing import Optional

import pandas as pd
import pymysql
from sshtunnel import open_tunnel

from nmml import config


def get_results(query: str, types: Optional[dict] = None, database_name: str = None) -> pd.DataFrame:
    if database_name is None:
        ssh_host = config.DB_SSH_URL()
        ssh_username = config.DB_SSH_USER()
        ssh_key_path = config.SSH_KEY_PATH()
        db_user = config.DB_USER()
        db_password = config.DB_PASSWORD()
        db_db = config.DB_DB()
    else:
        ssh_host = config.get_variable(f"{database_name}_SSH_URL")
        ssh_username = config.get_variable(f"{database_name}_SSH_USER")
        ssh_key_path = config.get_variable(f"{database_name}_SSH_KEY_PATH")
        db_user = config.get_variable(f"{database_name}_DB_USER")
        db_password = config.get_variable(f"{database_name}_DB_PASSWORD")
        db_db = config.get_variable(f"{database_name}_DB_DB")

    with open_tunnel(
            (ssh_host, 22),
            ssh_username=ssh_username,
            ssh_pkey=ssh_key_path,
            remote_bind_address=('localhost', 3306)) as server:
        conn = pymysql.connect(host='localhost', user=db_user, passwd=db_password, db=db_db,
                               port=server.local_bind_port)

        df = pd.read_sql_query(query, conn, dtype=types)

        conn.close()

    return df
