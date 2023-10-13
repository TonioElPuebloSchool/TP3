import os
import pandas as pd
import itertools

property_id = "407510831"
starting_date = "28daysAgo"
ending_date = "yesterday"
dimensions = ["sessionSource"]
metrics = ["newUsers", "totalUsers"]

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'datasource.json'

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
client = BetaAnalyticsDataClient()

request_api = RunReportRequest(
    property=f"properties/{property_id}",
    dimensions=[
        Dimension(name=dim) for dim in dimensions
        ],
        metrics=[
            Metric(name=metr) for metr in metrics
        ],
        date_ranges=[DateRange(start_date=starting_date, end_date=ending_date)],
    )
response = client.run_report(request_api)

# retreive value of metric header totalUsers
metric_header = [header.name for header in response.metric_headers]
metrics = [0 for i in metric_header]
for i in range(len(metric_header)):
    for row in response.rows :
        metrics[i]  += (int(row.metric_values[i].value))
# now metrics[0] is new users and metrics[1] is total users