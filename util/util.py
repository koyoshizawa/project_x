from datetime import datetime
import pandas


class FormatDatetime(object):

    @staticmethod
    def datetime_to_str(date_time:datetime):
        """
        datetime型をYYYY-MM-DDTMM:SS.Zの文字列に変換
        :param date_time:
        :return:
        """
        return date_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    @staticmethod
    def str_to_datetime(date_time:str):
        """
        YYYY-MM-DDTMM:SS.Zの文字列をdatetime型に変換
        :param str:
        :return:
        """
        return datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S.%fZ")




class TechnicalIndex(object):

    @staticmethod
    def get_simple_moving_average(data: pandas.Series, window: int):
        """

        :param data: データ
        :param window: x日移動平均
        :return:
        """
        return pandas.Series.rolling(data, window=window).mean()

    @staticmethod
    def get_bollinger_band(data: pandas.Series, window: int, deviation: int):
        """
        ボリンジャーバンドを返す
        :param data: データ
        :param deviation: sigma^x
        :return: 上限, 下限
        """
        # 移動平均線の計算
        base = TechnicalIndex.get_simple_moving_average(data, window)
        # シグマの計算
        sigma = pandas.Series.rolling(data, window=window).std(ddof=0)


        print('aaaaaa')
        print(base)
        print(sigma)
        upper_sigma = base + sigma**deviation
        lower_sigma = base - sigma**deviation

        return upper_sigma, lower_sigma