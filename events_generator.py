import matplotlib

matplotlib.use('TkAgg')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Time metrics generation for 30 days with a step of 1 second
np.random.seed(42)
dates = pd.date_range(start="2025-01-01", periods=30 * 24 * 60 * 60, freq='s')


# Generate a primary metric (dependency on time of day)
def generate_primary_metric(dates):
    hours = dates.hour + dates.minute / 60 + dates.second / 3600
    return np.maximum(0, np.sin((hours - 6) * np.pi / 12) * 50 + np.random.normal(0, 3, len(hours)))


primary_metric = generate_primary_metric(dates)

# Dependency on the primary metric with some noise
metrics = pd.DataFrame(index=dates)
metrics['metric_1'] = primary_metric
metrics['metric_2'] = np.cos(primary_metric / 20) * 30 + np.random.normal(0, 2, len(primary_metric))
metrics['metric_3'] = np.sin(primary_metric / 10) * 40 + np.random.normal(0, 3, len(primary_metric))
metrics['metric_4'] = np.log1p(primary_metric) * 20 + np.random.normal(0, 1.5, len(primary_metric))
metrics['metric_5'] = np.sqrt(primary_metric) * 25 + np.random.normal(0, 2, len(primary_metric))
metrics['metric_6'] = (primary_metric / 2) + np.random.normal(0, 4, len(primary_metric))
metrics['metric_7'] = np.tan(primary_metric / 50) * 15 + np.random.normal(0, 5, len(primary_metric))
metrics['metric_8'] = np.exp(primary_metric / 100) + np.random.normal(0, 1, len(primary_metric))
metrics['metric_9'] = np.clip(100 - primary_metric, 0, 100) + np.random.normal(0, 3, len(primary_metric))
metrics['metric_10'] = np.abs(np.sin(primary_metric / 30) * 70) + np.random.normal(0, 2, len(primary_metric))

# Anomalies are added to the metrics with a given rate and magnitude
def add_anomalies(metrics_df, anomaly_rate=0.001, anomaly_magnitude=3):
    anomaly_flags = np.zeros(len(metrics_df), dtype=int)

    for metric in metrics_df.columns:
        num_anomalies = int(len(metrics_df) * anomaly_rate)
        anomaly_indices = np.random.choice(metrics_df.index, num_anomalies, replace=False)

        for idx in anomaly_indices:
            duration = np.random.randint(1, 120)  # Length of the anomaly in seconds (from 1 to 120)
            end_idx = min(idx + pd.Timedelta(seconds=duration), metrics_df.index[-1])

            # Increase the value of the metric
            metrics_df.loc[idx:end_idx, metric] += np.random.normal(50, 15, len(metrics_df.loc[idx:end_idx]))
            anomaly_flags[metrics_df.index.get_loc(idx)] = 1  # Mark the start of the anomaly

    metrics_df['anomaly'] = anomaly_flags
    return metrics_df

# Add anomalies to metrics
metrics = add_anomalies(metrics)

# Metrics visualization
plt.figure(figsize=(12, 8))
for column in metrics.columns[:-1]:  # Исключаем колонку 'anomaly'
    plt.plot(metrics.index[:10000], metrics[column][:10000], label=column)  # Визуализируем первые 10,000 секунд

# Correct selection of anomalies within the first 10,000 seconds
anomalies = metrics[(metrics['anomaly'] == 1) & (metrics.index <= metrics.index[9999])]
plt.scatter(anomalies.index, anomalies['metric_1'].loc[anomalies.index], color='red', label='Anomaly', s=5)

plt.title("Synthetic Metrics with Anomalies (First 10,000 points)")
plt.xlabel("Time")
plt.ylabel("Metric Values")
plt.legend()
plt.grid(True)
plt.show()

metrics.to_csv('data/synthetic_metrics_with_anomalies_seconds.csv')