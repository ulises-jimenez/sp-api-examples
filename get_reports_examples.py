import json
from sp_api.api import Reports
from sp_api.base.marketplaces import Marketplaces
from datetime import datetime, timedelta, timezone
from shipping_data_processing import main as process_amazon_fulfilled
from utils import credentials, report_mapping


def get_report_data(report_type: str,
                    file_destination: str):
    report_types = [report_type]
    processing_status = ["DONE"]
    created_since_days = 7
    created_until_days = 6
    created_since = (datetime.now(timezone.utc) - timedelta(days=created_since_days)).isoformat()
    created_until = (datetime.now(timezone.utc) - timedelta(days=created_until_days)).isoformat()
    report_boss = Reports(credentials=credentials,
                          marketplace=Marketplaces.DE)
    res = report_boss.get_reports(reportTypes=report_types,
                                  processingStatuses=processing_status,
                                  dataStartTime=created_since,
                                  dataEndTime=created_until,
                                  marketplaceIds=[Marketplaces.ES.marketplace_id])
    latest_done_report = res.payload['reports'][0]
    report_document_id = latest_done_report['reportDocumentId']
    report_id = latest_done_report['reportId']
    report_boss.get_report_document(reportDocumentId=report_document_id,
                                    download=True,
                                    file=file_destination)


def get_orders_data():
    report_name = 'GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL'
    get_report_data(report_type=report_name,
                    file_destination=report_mapping[report_name])


def get_fulfilled_data():
    report_name = 'GET_AMAZON_FULFILLED_SHIPMENTS_DATA_GENERAL'
    get_report_data(report_type=report_name,
                    file_destination=report_mapping[report_name])


def get_fulfilled_returns_data():
    report_name = 'GET_FBA_FULFILLMENT_CUSTOMER_RETURNS_DATA'
    get_report_data(report_type=report_name,
                    file_destination=report_mapping[report_name])


def get_all_returns_data():
    report_name = 'GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE'
    get_report_data(report_type=report_name,
                    file_destination=report_mapping[report_name])


def get_settlement_data():
    report_name = 'GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2'
    get_report_data(report_type=report_name,
                    file_destination=report_mapping[report_name])


def get_fba_inventory_ledger_data():
    report_name = 'GET_LEDGER_SUMMARY_VIEW_DATA'
    get_report_data(report_type=report_name,
                    file_destination=report_mapping[report_name])


def main():
    get_orders_data()
    print('got orders')
    get_fulfilled_data()  # gets EU wide order data
    print('got fba fulfilled')
    process_amazon_fulfilled()
    print('processed')
    get_fulfilled_returns_data()
    print('got_fba_returns')
    get_all_returns_data()
    print('got all returns')
    get_settlement_data()
    print('got all settlement')
    get_fba_inventory_ledger_data()
    print('got fba inventory ledger')


if __name__ == '__main__':
    main()
