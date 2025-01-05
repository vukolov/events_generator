import argparse
import cmd
from application.commander import Commander


class InteractiveShell(cmd.Cmd):
    intro = "Type 'help' for a list of commands or 'quit/exit' to exit."
    prompt = "(app) "

    def do_help(self, arg):
        if arg:
            super().do_help(arg)
        else:
            print("""Available commands:
  help                     - Show this message
  quit                     - Exit the application
  exit                     - Exit the application
  generate-data            - Generate data
                            example: generate-data --start-time 2025-01-01 --steps-number 1000 --time-period 1ms --file-path data/group_1.csv
  plot-data                - Plot data from a file
  send-data                - Send data to a server
  """)

    def do_quit(self, arg):
        print("Exiting...")
        return True

    def do_exit(self, arg):
        return self.do_quit(arg)

    def do_generate_data(self, arg):
        parser = argparse.ArgumentParser(prog='generate-data')
        parser.add_argument('--steps-number', type=int, required=True)
        parser.add_argument('--file-path', type=str, required=True)
        self.parse_and_run(parser, arg, 'generate_data')

    def do_plot_data(self, arg):
        parser = argparse.ArgumentParser(prog='plot-data')
        parser.add_argument('--file-path', type=str, required=True)
        self.parse_and_run(parser, arg, 'plot_data')

    def do_send_data(self, arg):
        parser = argparse.ArgumentParser(prog='send-data')
        parser.add_argument('--file-path', type=str, required=True)
        parser.add_argument('--url', type=str, required=True)
        parser.add_argument('--time-period', type=str, required=True)
        parser.add_argument('--max-messages', type=int, required=True)
        self.parse_and_run(parser, arg, 'send_data')

    def emptyline(self):
        pass

    def default(self, line):
        command_map = {
            'generate-data': self.do_generate_data,
            'plot-data': self.do_plot_data,
            'send-data': self.do_send_data
        }

        command, *args = line.split(" ", 1)
        if command in command_map:
            command_map[command](" ".join(args))
        else:
            print(f"Unknown command: {line}")

    def parse_and_run(self, parser, arg, command_name):
        try:
            print("Processing command...")
            args = parser.parse_args(arg.split())
            getattr(Commander, command_name)(**vars(args))
            print("Done!")
        except SystemExit:
            print(f"Error: Invalid arguments for '{command_name}'. Use '--help' for usage.")
        except Exception as e:
            print(f"Unexpected error: {e}")
