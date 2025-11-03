import pandas as pd
from utils import report_mapping


def main():
    df = pd.read_csv(report_mapping['GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL'], sep='\t')
    print('hello')


if __name__ == '__main__':
    main()
