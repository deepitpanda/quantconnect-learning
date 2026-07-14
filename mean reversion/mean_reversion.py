from AlgorithmImports import *
import numpy as np

class MeanReversionAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2024, 1, 1)
        self.SetCash(100000)

        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol

        self.lookback = 20
        self.history_window = RollingWindow[float](self.lookback)

        self.SetWarmUp(self.lookback)

    def OnData(self, data):

        if self.symbol not in data:
            return

        self.history_window.Add(float(data[self.symbol].Close))

        if self.IsWarmingUp or not self.history_window.IsReady:
            return

        prices = np.array([self.history_window[i] for i in range(self.lookback)])

        mean = np.mean(prices)
        std = np.std(prices)

        if std == 0:
            return

        current = prices[0]
        z = (current - mean) / std

        invested = self.Portfolio[self.symbol].Invested

        # Entry
        if not invested:
            if z < -2:
                self.SetHoldings(self.symbol, 1)
            elif z > 2:
                self.SetHoldings(self.symbol, -1)

        # Exit
        else:
            if abs(z) < 0.25:
                self.Liquidate(self.symbol)