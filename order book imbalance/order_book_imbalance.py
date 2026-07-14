from AlgorithmImports import *

class OrderBookImbalanceAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2024, 1, 1)
        self.SetCash(100000)

        self.symbol = self.AddEquity("SPY", Resolution.Tick).Symbol

    def OnData(self, slice):

        if not slice.QuoteBars.ContainsKey(self.symbol):
            return

        # Placeholder: obtain bid/ask depth from your Level 2 feed.
        # The exact API depends on the dataset you subscribe to.

        bid_volume = ...
        ask_volume = ...

        imbalance = (bid_volume - ask_volume) / (bid_volume + ask_volume)

        if imbalance > 0.30:
            self.SetHoldings(self.symbol, 1)

        elif imbalance < -0.30:
            self.SetHoldings(self.symbol, -1)

        elif abs(imbalance) < 0.10:
            self.Liquidate()