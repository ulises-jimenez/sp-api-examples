import json
import time
from typing import List, Tuple
from sp_api.api import Reports, ReportsV2
from sp_api.base.reportTypes import ReportType
from sp_api.base.marketplaces import Marketplaces
from datetime import datetime, timedelta, timezone, date
from utils import report_mapping, credentials, requests_folder
from pprint import pprint


def create_monthly_retrieval_dates(start_date: date,
                                   end_date: date,
                                   create_report_intervals: int) -> List[Tuple]:
    period_length = (end_date - start_date).days
    number_of_periods = period_length / create_report_intervals
    number_of_periods_as_int = int(number_of_periods)
    if number_of_periods > number_of_periods_as_int:
        number_of_periods_as_int += 1
    days_list = []
    for period_count in range(number_of_periods_as_int):
        end_of_period = start_date + timedelta(days=create_report_intervals)
        if end_of_period >= end_date:
            current_tuple = start_date, end_date
            days_list.append(current_tuple)
            break
        current_tuple = start_date, end_of_period
        days_list.append(current_tuple)
        start_date = end_of_period + timedelta(days=1)
    return days_list


def create_reports() -> None:
    data_start_time = datetime(2025, 10, 27, 0, 0, 0, 0, tzinfo=timezone.utc).isoformat()
    data_end_time = datetime(2025, 10, 28, 0, 0, 0, 0, tzinfo=timezone.utc).isoformat()
    result = ReportsV2(credentials=credentials,
                       marketplace=Marketplaces.DE).create_report(
        reportType=ReportType.GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL,
        # optionally, you can set a start and end time for your report
        dataStartTime=data_start_time,
        dataEndTime=data_end_time)
    with open(requests_folder + 'create_report_id.json', 'w') as jf:
        json.dump(result.payload, jf)


def retrieve_ordered_report(report_type: ReportType):
    with open(report_mapping[report_type]['request_file']) as jf:
        retrieved_response = json.load(jf)
    if 'reportId' in retrieved_response:
        get_report_by_id(report_id=retrieved_response['reportId'],
                         retries=10,
                         retry_len_in_seconds=5)


def get_report_by_id(report_id: str, retries: int, retry_len_in_seconds: int):
    report_boss = Reports(credentials=credentials,
                          marketplace=Marketplaces.DE)
    result = report_boss.get_report(report_id)
    report_status = result.payload['processingStatus']
    for attempt in range(retries):
        if report_status == 'DONE':
            report_type = result.payload['reportType']
            document_id = result.payload['reportDocumentId']
            report_boss.get_report_document(reportDocumentId=document_id,
                                            download=True,
                                            file=report_mapping[report_type]['tsv'])
            print(f'report downloaded to {report_mapping[report_type]["tsv"]}')
            return
        elif report_status in ['PROCESSING', 'IN_QUEUE']:
            # have to wait before checking again
            time.sleep(retry_len_in_seconds)
        elif report_status in ['CANCELLED', 'FATAL']:
            # There was some kind of error, use report id to get error if it's present
            print('there was some kind of error')
            raise AssertionError(f'Report generation failed for id: {report_id}')
    raise AssertionError(
        f'Took too long, ran out of retries with {retries} retries with a len of {retry_len_in_seconds} seconds')


def main():
    start_date = date(year=2025, month=7, day=1)
    end_date = date(year=2025, month=9, day=30)
    dates = create_monthly_retrieval_dates(start_date=start_date,
                                           end_date=end_date,
                                           create_report_intervals=10)
    pprint(dates)


if __name__ == '__main__':
    main()
