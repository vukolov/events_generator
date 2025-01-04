import sys
from infrastructure.interactive_shell import InteractiveShell


if __name__ == "__main__":
    # If arguments are passed, execute the command directly
    if len(sys.argv) > 1:
        InteractiveShell().onecmd(" ".join(sys.argv[1:]))
    else:
        # Start interactive mode
        InteractiveShell().cmdloop()
