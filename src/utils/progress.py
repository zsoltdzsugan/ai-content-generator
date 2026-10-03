import sys
import time
import threading

class Progress:
    def __init__(self, total: int) -> None:
        self.total: int = total
        self.current: int = 0
        self.message: str = ""
        self.running: bool = False
        self.thread: threading.Thread | None = None

    def start(self, message: str) -> None:
        self.current += 1
        self.message = message
        self.running = True

        self.thread = threading.Thread(target=self._spin, daemon=True)
        self.thread.start()

    def finish(self, message: str = "Done") -> None:
        self.running = False

        if self.thread is not None:
            self.thread.join()

        sys.stdout.write("\r\033[K")
        sys.stdout.write(f"\rProcess [{self.current}/{self.total}]: {message} ✓\n")
        sys.stdout.flush()


    def _spin(self) -> None:
        spinner: list[str] = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        index: int = 0

        while self.running:
            char: str = spinner[index % len(spinner)]

            sys.stdout.write(f"\rProcess [{self.current}/{self.total}]: {self.message} {char}")
            sys.stdout.flush()

            index += 1
            time.sleep(0.1)
