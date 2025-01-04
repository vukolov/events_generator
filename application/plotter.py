import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')  # Set the backend for PyCharm compatibility


class Plotter:
    @staticmethod
    def plot_metrics(metrics: pd.DataFrame, anomaly_ranges: dict):
        # Plot each metric in a separate subplot with shaded anomaly regions
        plt.figure(figsize=(12, 20))
        for i, column in enumerate(metrics.columns[:-1]):  # Exclude 'anomaly' column
            plt.subplot(5, 2, i + 1)
            plt.plot(metrics.index[:10000], metrics[column][:10000], label=column)

            # Plot shaded areas for anomalies within the first 10,000 points
            for start, end in anomaly_ranges[column]:
                if start <= metrics.index[9999]:
                    plt.axvspan(start, min(end, metrics.index[9999]), color='red', alpha=0.3)

            plt.title(f"{column} with Anomalies")
            plt.xlabel("Time")
            plt.ylabel("Value")
            plt.legend()
            plt.grid(True)

        plt.tight_layout()
        plt.show()
