from typing import Optional

import pandas as pd
import pandas_gbq
from google.oauth2 import service_account

from nmml import config


def get_results(query: str, types: Optional[dict] = None) -> pd.DataFrame:
    credentials = service_account.Credentials.from_service_account_file(
        config.GOOGLE_ACCOUNT_FILE(),
    )

    return pandas_gbq.read_gbq(query, credentials=credentials, dtypes=types)
