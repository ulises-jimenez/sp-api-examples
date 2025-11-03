from decouple import config

credentials = dict(
    refresh_token=config('SP_API_REFRESH_TOKEN'),
    lwa_app_id=config('LWA_APP_ID'),
    lwa_client_secret=config('LWA_CLIENT_SECRET')
)

dl_folder = 'downloaded_reports/'

report_mapping = {
    'GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL': f'{dl_folder}orders_data.tsv',
    'GET_AMAZON_FULFILLED_SHIPMENTS_DATA_GENERAL': f'{dl_folder}amazon_fulfilled_shipments.tsv',
    'GET_FBA_FULFILLMENT_CUSTOMER_RETURNS_DATA': f'{dl_folder}fba_returns_data.tsv',
    'GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE': f'{dl_folder}all_return_data.tsv',
    'GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2': f'{dl_folder}settlement_report.tsv',
    'GET_LEDGER_SUMMARY_VIEW_DATA': f'{dl_folder}afn_inventory_summary.tsv'
}
