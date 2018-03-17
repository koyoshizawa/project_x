from datetime import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render
import oandapy

from util.util import FormatDatetime
from util.const import ACCESS_TOKEN


def chart_select(request):
    """
    チャートの表示
    :param request:
    :return:
    """

    template_path = 'chart/chart-select.html'

    currency_pair = ['JPY/USD']
    freq_options = ['1m', '5m', '15m', '1h']

    d = {
        'currency_pair': currency_pair,
        'freq_options': freq_options,
    }

    return render(request, template_path, d)


def get_selected_fx_data(request):
    """
    postされた条件のfx時系列データを返す
    :param request:
    :return:
    """
    # 取得した条件
    start_date = FormatDatetime.datetime_to_str(datetime(2018, 1, 1))
    end_date = FormatDatetime.datetime_to_str(datetime(2018, 1, 31))
    instrument = 'USD_JPY'
    granularity = 'D'
    # oanda apiで時系列fx価格データ取得
    oanda = oandapy.API(environment="practice",
                        access_token=ACCESS_TOKEN)
    response = oanda.get_history(instrument=instrument,
                                 granularity=granularity,
                                 start=start_date,
                                 end=end_date,
                                 candleFormat='midpoint')
    time_list = [d['time'] for d in response['candles']]
    price_list = [d['openMid'] for d in response['candles']]
    return HttpResponse(json.dumps({'time':time_list, 'price':price_list}))

from strategy.simple_bollinger_band import Agent
def test_view(request):

    from_datetime = datetime(2010, 1, 1)
    to_datetime = datetime(2011, 1, 1)

    agent = Agent(from_datetime, to_datetime, 'D', 'USD_JPY')
    result, count_win, count_lose = agent.backtest()

    return HttpResponse('勝ち'+str(count_win)+'負け'+str(count_lose))