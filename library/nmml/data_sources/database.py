from typing import Optional

import pandas as pd
import pymysql
from sshtunnel import open_tunnel

from nmml import config


def get_results(query: str, types: Optional[dict] = None) -> pd.DataFrame:
    with open_tunnel(
            (config.DB_SSH_URL(), 22),
            ssh_username=config.DB_SSH_USER(),
            ssh_pkey=config.SSH_KEY_PATH(),
            remote_bind_address=('localhost', 3306)) as server:
        conn = pymysql.connect(host='localhost', user=config.DB_USER(), passwd=config.DB_PASSWORD(), db=config.DB_DB(),
                               port=server.local_bind_port)

        df = pd.read_sql_query(query, conn, dtype=types)

        conn.close()

    return df
