import matplotlib

matplotlib.use('TkAgg')  # Set the backend for PyCharm compatibility

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Generate timestamps for 30 days with a step of 1 second
np.random.seed(42)
dates = pd.date_range(start="2025-01-01", periods=30 * 24 * 60 * 60, freq='s')


# Generate the primary metric (sine wave with hourly oscillation)
def generate_primary_metric(dates):
    time_in_hour = dates.minute * 60 + dates.second  # Total seconds passed in the hour
    return np.maximum(0, np.sin(time_in_hour * np.pi / 1800) * 50 + np.random.normal(0, 3, len(time_in_hour)))


# Inject anomalies into a metric
def add_anomalies(metrics_df, metric_name, anomaly_rate=0.001, anomaly_magnitude=50):
    anomaly_flags = np.zeros(len(metrics_df), dtype=int)

    num_anomalies = int(len(metrics_df) * anomaly_rate)
    anomaly_indices = np.random.choice(metrics_df.index, num_anomalies, replace=False)

    for idx in anomaly_indices:
        duration = np.random.randint(1, 120)  # Anomalies last between 1 to 120 seconds
        end_idx = min(idx + pd.Timedelta(seconds=duration), metrics_df.index[-1])

        # Increase the metric values to simulate anomalies
        metrics_df.loc[idx:end_idx, metric_name] += np.random.normal(anomaly_magnitude, 15,
                                                                     len(metrics_df.loc[idx:end_idx]))
        anomaly_flags[metrics_df.index.get_loc(idx)] = 1  # Mark anomaly start

    return anomaly_flags


# Generate primary metric
primary_metric = generate_primary_metric(dates)
metrics = pd.DataFrame(index=dates)
metrics['metric_1'] = primary_metric

# Add anomalies to the primary metric
primary_anomaly_flags = add_anomalies(metrics, 'metric_1')

# Generate dependent metrics based on the modified primary metric
metrics['metric_2'] = np.cos(metrics['metric_1'] / 20) * 30 + np.random.normal(0, 2, len(primary_metric))
metrics['metric_3'] = np.sin(metrics['metric_1'] / 10) * 40 + np.random.normal(0, 3, len(primary_metric))
metrics['metric_4'] = np.log1p(metrics['metric_1']) * 20 + np.random.normal(0, 1.5, len(primary_metric))
metrics['metric_5'] = np.sqrt(metrics['metric_1']) * 25 + np.random.normal(0, 2, len(primary_metric))
metrics['metric_6'] = (metrics['metric_1'] / 2) + np.random.normal(0, 4, len(primary_metric))
metrics['metric_7'] = np.tan(metrics['metric_1'] / 50) * 15 + np.random.normal(0, 5, len(primary_metric))
metrics['metric_8'] = np.exp(metrics['metric_1'] / 100) + np.random.normal(0, 1, len(primary_metric))
metrics['metric_9'] = np.clip(100 - metrics['metric_1'], 0, 100) + np.random.normal(0, 3, len(primary_metric))
metrics['metric_10'] = np.abs(np.sin(metrics['metric_1'] / 30) * 70) + np.random.normal(0, 2, len(primary_metric))

# Inject unique anomalies into each dependent metric
for metric in metrics.columns[1:]:  # Exclude 'metric_1' which already has anomalies
    anomaly_flags = add_anomalies(metrics, metric)
    primary_anomaly_flags = np.logical_or(primary_anomaly_flags, anomaly_flags)

# Combine anomaly flags into one column to mark anomalies for all metrics
metrics['anomaly'] = primary_anomaly_flags.astype(int)

# Plot each metric in a separate subplot
plt.figure(figsize=(12, 20))
for i, column in enumerate(metrics.columns[:-1]):  # Exclude 'anomaly' column
    plt.subplot(5, 2, i + 1)
    plt.plot(metrics.index[:10000], metrics[column][:10000], label=column)

    # Plot anomalies for each metric
    anomalies = metrics[(metrics['anomaly'] == 1) & (metrics.index <= metrics.index[9999])]
    plt.scatter(anomalies.index, anomalies[column].loc[anomalies.index], color='red', s=5, label='Anomaly')

    plt.title(f"{column} with Anomalies")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)

plt.tight_layout()
plt.show()

# Save metrics with anomalies to CSV
metrics.to_csv('data/synthetic_metrics_with_anomalies_seconds.csv')
