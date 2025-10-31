import pandas as pd


def main():
    df = pd.read_csv('downloaded_reports/amazon_fulfilled_shipments.tsv', sep='\t')
    reduced_columns = df[['amazon-order-id', 'quantity-shipped', 'currency', 'item-price', 'item-tax',
                          'shipping-price', 'shipping-tax', 'ship-country', 'fulfillment-center-id']]
    reduced_columns.to_csv('amazon_fulfilled_reduced.tsv', sep='\t', index=False)

if __name__ == '__main__':
    main()