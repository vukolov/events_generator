from tqdm import tqdm
import pandas as pd
import requests


class Sender:
    @staticmethod
    def send(url: str, source_file_path: str, headers: dict = {"Content-Type": "application/json"}):
        df = pd.read_csv(source_file_path)

        for _, row in tqdm(df.iterrows(), total=len(df), desc="Sending data"):
            data = {
                "event_time": row["event_time"],
                "metrics": {f"metric_{i + 1}": row[f"metric_{i + 1}"] for i in range(10)},
                "anomalies": {f"anomaly_metric_{i + 1}": row[f"anomaly_metric_{i + 1}"] for i in range(10)}
            }
            response = requests.post(url, json=data, headers=headers)
            # Optionally, handle the response here
            # print(response.status_code, response.text)