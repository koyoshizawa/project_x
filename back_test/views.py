from datetime import datetime
import json
import math
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

    # バックテスト実行
    agent = Agent(start_date, end_date, granularity, instrument)
    data_frame = agent.backtest()

    # 売買のタイミングを計算
    # 1: long_open 2: long_close 3: short_open 4: short_close
    position_list = []
    position_st_list = data_frame['position'].tolist()
    for i in range(len(position_st_list)):
        # 1ループ目
        if i == 0:
            if position_st_list[i] == 1:  # long position
                position_list.append(1)
            elif position_st_list[i] == 2:  # short position
                position_list.append(3)
            else:
                position_list.append(0)

        # 2ループ目以降
        else:
            if position_st_list[i-1] == 0 and position_st_list[i] == 1:
                position_list.append(1)
            elif position_st_list[i-1] == 1 and position_st_list[i] == 0:
                position_list.append(2)
            elif position_st_list[i-1] == 0 and position_st_list[i] == 2:
                position_list.append(3)
            elif position_st_list[i-1] == 2 and position_st_list[i] == 0:
                position_list.append(4)
            else:
                position_list.append(0)

    # float64型はjson.dump()できないので、あらかじめ変換
    # 移動平均の特性上、最初のN個のデータはNaNなので、NaN以降最初の値を全てのNaNに代入する
    first_data_after_nan = 0
    for d in data_frame['technical_index']:
        if math.isnan(d) == False:
            first_data_after_nan = d
            break
    # Nanに上記で取得したデータ代入
    technical_index_float_list = [float(first_data_after_nan) if math.isnan(d) else float(d)
                                  for d in data_frame['technical_index']]

    return HttpResponse(json.dumps({'asset_transition':data_frame['asset'].tolist(), 'time': data_frame['time'].tolist(),
                                    'position': position_list, 'rate': data_frame['rate'].tolist(),
                                    'technical_index': technical_index_float_list}))
