from AlgorithmImports import *

class MovingAverageMomentum(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2024, 1, 1)
        self.SetCash(100000)

        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol

        self.fast = self.SMA(self.symbol, 50)
        self.slow = self.SMA(self.symbol, 200)

        self.SetWarmUp(200)

    def OnData(self, data):

        if self.IsWarmingUp:
            return

        if self.fast.Current.Value > self.slow.Current.Value:
            self.SetHoldings(self.symbol, 1)

        elif self.fast.Current.Value < self.slow.Current.Value:
            self.SetHoldings(self.symbol, -1)