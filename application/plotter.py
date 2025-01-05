import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')  # Set the backend for PyCharm compatibility


class Plotter:
    @staticmethod
    def plot_metrics(file_path: str):
        df = pd.read_csv(file_path)

        # Ограничение на 10,000 записей
        df = df[:10000]

        # Преобразование столбца времени в datetime
        df['event_time'] = pd.to_datetime(df['event_time'])

        # Определяем количество метрик
        metrics = [col for col in df.columns if 'metric_' in col and 'anomaly' not in col]
        anomalies = [col for col in df.columns if 'anomaly_metric_' in col]

        # Plot each metric in a separate subplot with shaded anomaly regions
        plt.figure(figsize=(12, 20))
        for i, column in enumerate(metrics):
            plt.subplot(5, 2, i + 1)
            plt.plot(df['event_time'], df[column], label=column, color='blue')

            # Добавление зон аномалий
            anomaly_column = f'anomaly_{column}'
            if anomaly_column in df.columns:
                for j in range(len(df)):
                    if df[anomaly_column][j] == 1:
                        plt.axvspan(df['event_time'][j],
                                    df['event_time'][j] + pd.Timedelta(milliseconds=1),
                                    color='red', alpha=0.3)

            plt.title(f"{column} with Anomalies")
            plt.xlabel("Time")
            plt.ylabel("Value")
            plt.legend()
            plt.grid(True)

        plt.tight_layout()
        plt.show()
