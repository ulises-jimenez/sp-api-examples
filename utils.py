from decouple import config

credentials = dict(
    refresh_token=config('SP_API_REFRESH_TOKEN'),
    lwa_app_id=config('LWA_APP_ID'),
    lwa_client_secret=config('LWA_CLIENT_SECRET')
)

dl_folder = 'downloaded_reports/'
requests_folder = 'report_requests/'

report_mapping = {
    'GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL': {
        'tsv': f'{dl_folder}orders_data.tsv',
        'request_file': f'{requests_folder}orders_request.json'
    },
    'GET_AMAZON_FULFILLED_SHIPMENTS_DATA_GENERAL': {
        'tsv': f'{dl_folder}amazon_fulfilled_shipments.tsv',
        'request_file': f'{requests_folder}afn_fulfilled_shipments_request.json'
    },
    'GET_FBA_FULFILLMENT_CUSTOMER_RETURNS_DATA': {
        'tsv': f'{dl_folder}amazon_fulfilled_returns.tsv',
        'request_file': f'{requests_folder}afn_returns_request.json'
    },
    'GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE': {
        'tsv': f'{dl_folder}all_return_data.tsv',
        'request_file': f'{requests_folder}all_returns_request.json'
    },
    'GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2': {
        'tsv': f'{dl_folder}settlement_data.tsv',
        'request_file': f'{requests_folder}settlement_request.json'
    },
    'GET_LEDGER_SUMMARY_VIEW_DATA': {
        'tsv': f'{dl_folder}afn_inventory_summary.tsv',
        'request_file': f'{requests_folder}afn_inventory_request.json'
    },
}
