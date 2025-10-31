from sp_api.api import Reports, Tokens
from decouple import config
from sp_api.base import SellingApiException
from sp_api.base.reportTypes import ReportType
from sp_api.base.marketplaces import Marketplaces
from datetime import datetime, timedelta, timezone

credentials = dict(
    refresh_token=config('SP_API_REFRESH_TOKEN'),
    lwa_app_id=config('LWA_APP_ID'),
    lwa_client_secret=config('LWA_CLIENT_SECRET')
)


def get_rdt(report_document_id: str):
    result = Tokens(credentials=credentials,
                    marketplace=Marketplaces.IT).create_restricted_data_token(restrictedResources=[
        {
            "method": "GET",
            "path": f"/reports/2021-06-30/documents/{report_document_id}"
        }
    ])
    print('hi')


# orders API

def get_amz_fulfilled_shipments():
    report_types = ["GET_AMAZON_FULFILLED_SHIPMENTS_DATA_GENERAL"]
    processing_status = ["DONE"]
    created_since_days = 3
    created_since = (datetime.now(timezone.utc) - timedelta(days=created_since_days)).isoformat()
    report_boss = Reports(credentials=credentials,
                          marketplace=Marketplaces.IT)
    res = report_boss.get_reports(reportTypes=report_types,
                                  processingStatuses=processing_status,
                                  createdSince=created_since)
    latest_done_report = res.payload['reports'][0]
    report_document_id = latest_done_report['reportDocumentId']
    report_id = latest_done_report['reportId']
    report_boss.get_report_document(reportDocumentId=report_document_id,
                                    download=True,
                                    file='downloaded_reports/amazon_fulfilled_shipments.tsv')

def get_orders_data():
    report_types = ["GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL"]
    processing_status = ["DONE"]
    created_since_days = 3
    created_since = (datetime.now(timezone.utc) - timedelta(days=created_since_days)).isoformat()
    report_boss = Reports(credentials=credentials,
                          marketplace=Marketplaces.IT)
    res = report_boss.get_reports(reportTypes=report_types,
                                  processingStatuses=processing_status,
                                  createdSince=created_since)
    latest_done_report = res.payload['reports'][0]
    report_document_id = latest_done_report['reportDocumentId']
    report_id = latest_done_report['reportId']
    report_boss.get_report_document(reportDocumentId=report_document_id,
                                    download=True,
                                    file='downloaded_reports/orders_data.tsv')



def main():
    # get_amz_fulfilled_shipments()
    get_orders_data()


# report request
# create_report_response = Reports().create_report(reportType=ReportType.GET_MERCHANT_LISTINGS_ALL_DATA)


# PII Data

# Orders(restricted_data_token='<token>').get_orders(CreatedAfter=(datetime.utcnow() - timedelta(days=7)).isoformat())

if __name__ == '__main__':
    main()
