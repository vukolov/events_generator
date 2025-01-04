import numpy as np
import pandas as pd


class DataGenerator:
    def generate_set_of_metrics(self, steps_number: int):
        # Generate timestamps for 30 days with a step of 1 second
        np.random.seed(42)
        dates = pd.date_range(start="2025-01-01", periods=steps_number, freq='s')

        # Generate primary metric
        primary_metric = self._generate_primary_metric(dates)
        metrics = pd.DataFrame(index=dates)
        metrics['metric_1'] = primary_metric

        anomaly_flags = {}
        anomaly_ranges = {}

        # Add anomalies to the primary metric
        anomaly_flags['metric_1'], anomaly_ranges['metric_1'] = self. _add_anomalies(metrics, 'metric_1')

        # Generate dependent metrics based on the modified primary metric
        metrics['metric_2'] = 50 + np.cos(metrics['metric_1'].shift(5).bfill() / 20) * 30 + np.random.normal(0, 2,
                                                                                                             len(primary_metric))
        metrics['metric_3'] = 70 + np.sin(metrics['metric_1'].shift(7).bfill() / 10) * 40 + np.random.normal(0, 3,
                                                                                                             len(primary_metric))
        metrics['metric_4'] = 90 + np.log1p(metrics['metric_1'].shift(10).bfill()) * 20 + np.random.normal(0, 1.5,
                                                                                                           len(primary_metric))
        metrics['metric_5'] = 75 + np.sqrt(metrics['metric_1'].shift(4).bfill()) * 25 + np.random.normal(0, 2,
                                                                                                         len(primary_metric))
        metrics['metric_6'] = 100 + (metrics['metric_1'].shift(30).bfill() / 2) + np.random.normal(0, 4,
                                                                                                   len(primary_metric))
        metrics['metric_7'] = 30 + np.sin(metrics['metric_2'].shift(2).bfill() / 50) * 15 + np.cos(
            metrics['metric_3'].shift(4).bfill() / 50) * 15 + np.random.normal(0, 5, len(primary_metric))
        metrics['metric_8'] = np.exp(metrics['metric_1'].shift(1).bfill() / 100) + np.random.normal(0, 1,
                                                                                                    len(primary_metric))
        metrics['metric_9'] = 50 + np.clip(100 - metrics['metric_1'].shift(5).bfill(), 0, 100) + np.random.normal(0, 3,
                                                                                                                  len(primary_metric))
        metrics['metric_10'] = 50 + np.abs(np.sin(metrics['metric_1'].shift(5).bfill() / 30) * 70) + np.random.normal(0,
                                                                                                                      2,
                                                                                                                      len(primary_metric))

        # Inject unique anomalies into each dependent metric
        for metric in metrics.columns:
            if metric != 'metric_1':
                anomaly_flags[metric], anomaly_ranges[metric] = self._add_anomalies(metrics, metric)

        # separate columns to store the information about anomalies for each metric
        for m in metrics.columns:
            metrics['anomaly_' + m] = anomaly_flags[m]

    def save_metrics(self, metrics_df, file_path):
        metrics_df.to_csv(file_path, index=True, index_label='event_time')
        print("CSV file saved successfully!")

    def _generate_primary_metric(self, dates):
        # Generate the primary metric (sine wave with hourly oscillation)
        time_in_hour = dates.minute * 60 + dates.second  # Total seconds passed in the hour
        return np.maximum(0, np.sin(time_in_hour * np.pi / 1800) * 50 + np.random.normal(0, 3, len(time_in_hour)))

    def _add_anomalies(self, metrics_df, metric_name, anomaly_rate=0.001, anomaly_magnitude=50, window_size=300):
        anomaly_flags = np.zeros(len(metrics_df), dtype=int)
        anomaly_ranges = []

        num_anomalies = int(len(metrics_df) * anomaly_rate)
        anomaly_indices = np.random.choice(metrics_df.index, num_anomalies, replace=False)

        for idx in anomaly_indices:
            duration = np.random.randint(1, 120)  # Anomalies last between 1 to 120 seconds
            end_idx = min(idx + pd.Timedelta(seconds=duration), metrics_df.index[-1])

            # Randomly choose direction for anomaly (up or down)
            direction = np.random.choice([-1, 1])

            # Generate potential anomaly values
            anomaly_values = metrics_df.loc[idx:end_idx, metric_name] + direction * np.random.normal(anomaly_magnitude,
                                                                                                     15,
                                                                                                     len(metrics_df.loc[
                                                                                                         idx:end_idx]))

            # Apply anomaly only if it exceeds 3 sigma
            # if np.any(anomaly_values > threshold.loc[idx:end_idx]):
            metrics_df.loc[idx:end_idx, metric_name] = anomaly_values
            anomaly_flags[metrics_df.index.get_loc(idx):metrics_df.index.get_loc(end_idx)] = 1
            anomaly_ranges.append((idx, end_idx))  # Store anomaly time ranges

        return anomaly_flags, anomaly_ranges
