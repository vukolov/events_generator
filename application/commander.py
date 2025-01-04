from application.data_generator import DataGenerator


class Commander:
    @staticmethod
    def generate_data(steps_number: int, file_path: str):
        generator = DataGenerator()
        data_frame = generator.generate_set_of_metrics(steps_number)
        generator.save_metrics(data_frame, file_path)

    @staticmethod
    def plot_data(file_path: str):
        print(f"Plotting data from file: {file_path}")

    @staticmethod
    def send_data(file_path: str, url: str, start_time: str, time_interval_seconds: int, max_messages: int):
        print(f"Sending data from {file_path} to {url}")
