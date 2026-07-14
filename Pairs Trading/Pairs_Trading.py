from AlgorithmImports import *
import numpy as np

class PairsTradingAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2024, 1, 1)
        self.SetCash(100000)

        self.symbol1 = self.AddEquity("KO", Resolution.Daily).Symbol
        self.symbol2 = self.AddEquity("PEP", Resolution.Daily).Symbol

        self.lookback = 30

        self.spreadWindow = RollingWindow[float](self.lookback)

        self.SetWarmUp(self.lookback)

    def OnData(self, data):

        if self.symbol1 not in data or self.symbol2 not in data:
            return

        p1 = data[self.symbol1].Close
        p2 = data[self.symbol2].Close

        spread = float(p1 - p2)

        self.spreadWindow.Add(spread)

        if self.IsWarmingUp or not self.spreadWindow.IsReady:
            return

        spreads = np.array([self.spreadWindow[i] for i in range(self.lookback)])

        mean = np.mean(spreads)
        std = np.std(spreads)

        if std == 0:
            return

        z = (spread - mean) / std

        invested = (
            self.Portfolio[self.symbol1].Invested or
            self.Portfolio[self.symbol2].Invested
        )

        if not invested:

            if z > 2:
                # KO expensive relative to PEP
                self.SetHoldings(self.symbol1, -0.5)
                self.SetHoldings(self.symbol2, 0.5)

            elif z < -2:
                # KO cheap relative to PEP
                self.SetHoldings(self.symbol1, 0.5)
                self.SetHoldings(self.symbol2, -0.5)

        else:

            if abs(z) < 0.25:
                self.Liquidate()