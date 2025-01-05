import pandas as pd
from application.data_generator import DataGenerator
from application.plotter import Plotter


class Commander:
    @staticmethod
    def generate_data(start_time: str, steps_number: int, file_path: str):
        generator = DataGenerator()
        metrics_data_frame = generator.generate_set_of_metrics(start_time, steps_number)
        generator.save_metrics(metrics_data_frame, file_path)

    @staticmethod
    def plot_data(file_path: str):
        plotter = Plotter()
        plotter.plot_metrics(file_path)

    @staticmethod
    def send_data(file_path: str, url: str, start_time: str, time_interval_seconds: int, max_messages: int):
        print(f"Sending data from {file_path} to {url}")
