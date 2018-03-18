from datetime import datetime
import json
from django.shortcuts import render
from django.http import HttpResponse
from strategy.agent_simple_bollinger_band import Agent
from util.util import FormatDatetime

def index(request):

    template_name = 'back_test/index.html'

    currency_pair = ['USD_JPY']
    freq_options = ['M1', 'M5', 'M15', 'H1', 'D']

    d = {
        'currency_pair': currency_pair,
        'freq_options': freq_options,
    }

    return render(request, template_name, d)

def exec_back_test(request):
    """
    back_testの実行
    :param request:
    :return:
    """

    # 取得した条件
    start_date = datetime.strptime(request.POST['date_from'], '%Y-%m-%d')
    end_date = datetime.strptime(request.POST['date_to'], '%Y-%m-%d')
    instrument = request.POST['instrument']
    granularity = request.POST['granularity']

    agent = Agent(start_date, end_date, granularity, instrument)
    time, result, count_win, count_lose = agent.backtest()

    return HttpResponse(json.dumps({'count_win':count_win, 'count_lose': count_lose, 'asset_transition':result, 'time': time}))
