from utils import credentials
from sp_api.api import Sellers
from pprint import pprint


def main():
    # needs authorization
    res = Sellers(credentials=credentials).get_account()
    pprint(res.payload)


if __name__ == '__main__':
    main()
