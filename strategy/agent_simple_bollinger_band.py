import pandas as pd
from .agent_base import BaseAgent
from util.util import TechnicalIndex

class Agent(BaseAgent):

    def backtest(self, spread=2, lots=0.1):
        """
        backtestの実行

        DIFF_PRICE以上の変化があったら強制的に損切りor利確
        :return:
        """

        have_position = self.NO_POSITION
        order_price = 0
        count_win = 0
        count_lose = 0
        asset = self.ASSET

        result = []
        time = []
        position = []
        price = []

        # bollinger_band取得
        upper_sigma, lower_sigma = TechnicalIndex.get_bollinger_band(self.data_frame['openMid'], window=25,
                                                                     deviation=2)
        for i, rate in enumerate(self.data_frame['openMid']):

            if have_position == self.NO_POSITION:
                if rate >= upper_sigma[i]:
                    # 売り注文
                    have_position, order_price = super(Agent, self).open_order(rate, self.SHORT_POSITION)
                elif rate <= lower_sigma[i]:
                    # 買い注文
                    have_position, order_price = super(Agent, self).open_order(rate, self.LONG_POSITION)

            else:
                # 利益確定 or 損切り
                if abs(order_price - rate) > self.DIFF_PRICE:
                    have_position, order_price, count_win, count_lose, asset = \
                        super(Agent, self).close_order(rate, order_price, have_position, count_win, count_lose, asset)

            # 資産状態をリストに保持
            result.append(int(asset))
            # 時間情報をリストに保持
            time.append(self.data_frame.index[i].to_pydatetime().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
            # ポジションをリストに保持
            position.append(have_position)
            # rateをジスとに保持
            price.append(rate)

        data_frame = pd.DataFrame({'time': time,
                                   'rate': price,
                                   'asset': result,
                                   'position': position,
                                   'technical_index': upper_sigma})

        return data_frame