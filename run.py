# Enable switch on/off for single and multi-plot
# Fix value of 100% loss on sell
# Fix relative S&P500 performance calculation.
# Add dividends and sales as returns rather than invested. Invested dividends are not double counted.
# Clean up constants.py code
# Stop running on import. Make each file a def main() with if __name__ == "__main__": n\ main()
# Learn Lambda
# Plot of stock value (owned * price) on lower graph in individual plot window

from analysis.plots_multi_stock import PortfolioCumulativePlot
from analysis.plots_single_stock import PortfolioSinglePlots
from analysis.plots_stacked_portfolio import PortfolioStackedPlot


def run():
    PortfolioCumulativePlot()
    PortfolioSinglePlots()
    PortfolioStackedPlot()


if __name__ == '__main__':
    run()
