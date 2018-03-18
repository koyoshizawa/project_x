import pandas as pd
from datetime import datetime
import oandapy

from util.const import ACCESS_TOKEN
from util.util import FormatDatetime
from util.util import TechnicalIndex


class BaseAgent(object):

    def __init__(self, from_datetime: datetime, to_datetime: datetime, granularity: str, instrument: str):
        self.ASSET = 100000
        self.NO_POSITION = 0
        self.LONG_POSITION = 1
        self.SHORT_POSITION = 2
        self.DIFF_PRICE = 0.10   #価格差30pipsで利確or損切
        self.UNIT = 10000  # 通貨単位
        self.from_datetime = from_datetime  # 開始日時
        self.to_datetime = to_datetime  # 終了日時
        self.granularity = granularity  # 間隔
        self.instrument = instrument  # 通貨ペア
        self.__get_fx_data()
        self.__format_fx_data_to_data_frame()



    def open_order(self, price, order_type):

        have_position = order_type
        order_price = price

        return have_position, order_price


    def close_order(self, price, order_price, have_position, count_win, count_lose, asset):

        if have_position == self.LONG_POSITION:
            diff_price = price - order_price
        elif have_position == self.SHORT_POSITION:
            diff_price = order_price - price
        else:
            diff_price = 0

        # 勝敗のカウント
        if diff_price > 0:
            count_win += 1
        else:
            count_lose += 1

        # 資産の増減
        asset = asset + round(diff_price*self.UNIT)

        # ポジション解除
        have_position = self.NO_POSITION

        return have_position, order_price, count_win, count_lose, asset


    def __get_fx_data(self):
        """
        oanda apiからjson fxデータを取得
        :return:
        """
        # 日時をapiのフォーマットに変換
        from_datetime = FormatDatetime.datetime_to_str(self.from_datetime)
        to_datetime = FormatDatetime.datetime_to_str(self.to_datetime)

        # oanda apiで時系列fx価格データ取得
        oanda = oandapy.API(environment="practice", access_token=ACCESS_TOKEN)
        self.json_fx_data = oanda.get_history(instrument=self.instrument,
                                              granularity=self.granularity,
                                              start=from_datetime,
                                              end=to_datetime,
                                              candleFormat='midpoint')

    def __format_fx_data_to_data_frame(self):
        """
        jsonのfxデータをpd.DataFameに変換
        :return:
        """
        # TODO 他に必要な列を追加
        d = [{'time': FormatDatetime.str_to_datetime(d['time']),
              'openMid': d['openMid']}
             for d in self.json_fx_data['candles']]

        # DataFrame型に変更
        data_frame = pd.DataFrame(d)
        data_frame = data_frame.set_index('time')
        self.data_frame = data_frame

