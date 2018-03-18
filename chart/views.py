from datetime import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

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

    currency_pair = ['USD_JPY']
    freq_options = ['M1', 'M5', 'M15', 'H1', 'D']

    d = {
        'currency_pair': currency_pair,
        'freq_options': freq_options,
    }

    return render(request, template_path, d)


@ensure_csrf_cookie
def get_selected_fx_data(request):
    """
    postされた条件のfx時系列データを返す
    :param request:
    :return:
    """
    # 取得した条件
    start_date = FormatDatetime.datetime_to_str(datetime.strptime(request.POST['date_from'], '%Y-%m-%d'))
    end_date = FormatDatetime.datetime_to_str(datetime.strptime(request.POST['date_to'], '%Y-%m-%d'))
    instrument = request.POST['instrument']
    granularity = request.POST['granularity']
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

