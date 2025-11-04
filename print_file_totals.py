import pandas as pd
from utils import report_mapping

currency_conversion = [
    {
        'currency': 'EUR',
        'exchange_rate': 1
    },
    {
        'currency': 'GBP',
        'exchange_rate': 1.14
    }]
currency_df = pd.DataFrame(currency_conversion)


def main():
    # df_pre_merge = pd.read_csv(report_mapping['GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL'], sep='\t')
    df_pre_merge = pd.read_csv('downloaded_reports/orders_data.tsv', sep='\t')
    df = pd.merge(df_pre_merge, currency_df, on='currency')
    df['item_price_as_eur'] = round(df['item-price'] * df['exchange_rate'], 2)
    df = df[df['sales-channel'] == 'Amazon.de']
    shipped = df[df['item-status'] == 'Shipped']
    unshipped = df[df['item-status'] == 'Unshipped']
    print(f'all orders EUR: {df["item_price_as_eur"].sum().round(2)}')
    print(f'shipped orders EUR: {shipped["item_price_as_eur"].sum().round(2)}')
    print(f'unshipped orders EUR: {unshipped["item_price_as_eur"].sum().round(2)}')


if __name__ == '__main__':
    main()
