import io
import pandas as pd
from starlette.responses import StreamingResponse

from core.database.connection import db
from core.middlewares.catch_exceptions import logger


def fetch_data():
    database_data = db.client["candidate"].users.find()
    data_list = list(database_data)
    logger.info(f"Fetched {len(data_list)} records from database.")
    return data_list


def generate_report():
    data = fetch_data()

    if not data:
        logger.warning("No data available to generate report.")
        return None

    df = pd.DataFrame(data)
    logger.info(f"DataFrame created with {len(df)} rows.")

    stream = io.StringIO()
    df.to_csv(stream, index=False)
    stream.seek(0)

    logger.info("CSV data prepared for streaming.")

    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=report.csv"
    df.to_csv("candidate_report", index=False)
    return response
