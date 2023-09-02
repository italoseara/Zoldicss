import curses
import threading
from time import sleep
from typing import Self
from datetime import datetime


class State:
    LOGS = 0
    DETAILS = 1
    COMMAND = 2


class Key:
    UP = curses.KEY_UP
    DOWN = curses.KEY_DOWN
    HOME = curses.KEY_HOME
    END = curses.KEY_END
    RESIZE = curses.KEY_RESIZE
    BACKSPACE = ord("\b")
    ENTER = ord("\n")
    ESCAPE = 27
    SPACE = ord(" ")
    SLASH = ord("/")
    CTRL_L = 12

    J = ord("j")
    K = ord("k")


class TextComponent:
    text: str
    _details: str
    _max_width: int

    def __init__(self, content: str, details: str, max_width: int) -> None:
        self.text = content
        self._details = details
        self._max_width = max_width

    @property
    def details(self) -> str:
        lines = []
        for line in self._details.split("\n"):
            while len(line) > self._max_width:
                lines.append(line[:self._max_width])
                line = line[self._max_width:]
            lines.append(line)
        return lines

    @property
    def lines(self) -> list[str]:
        lines = []
        for line in self.text.split("\n"):
            while len(line) > self._max_width:
                lines.append(line[:self._max_width])
                line = line[self._max_width:]
            lines.append(line)

        return lines


class Console:
    # State of the console
    state: int = State.LOGS
    
    # Curses window object
    screen: curses.window

    # Buffer of text to be displayed
    buffer: list[TextComponent]
    buffer_size: int = 1000

    # Dimensions of the console
    width: int 
    height: int

    # Scroll position
    scroll: int = 0

    # Cursor position
    cursor_x: int = 0
    cursor_y: int = 0

    # Bottom text
    command: str = ""

    # Thread
    thread: threading.Thread

    # Logs
    log_path: str

    def __init__(self, screen: curses.window = None, log_path: str = None) -> None:
        self.screen = screen or curses.initscr()
        self.height, self.width = self._getmaxyx()
        self.log_path = log_path
        self.buffer = []

        # Set up curses
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        self.screen.nodelay(True)

        self.render()

    def run(self) -> Self:
        self.thread = threading.Thread(target=self._run)
        self.thread.start()
        return self

    def _run(self) -> None:
        while True:
            self.update()
            sleep(0.001)

    def log(self, *args, details: str = None) -> None:
        date = datetime.now().strftime('%Y-%m-%d')
        time = datetime.now().strftime('%H:%M:%S')

        message = f"[{time}] - {' '.join(map(str, args))}"
        
        with open(self.log_path or f"logs/{date}.log", "a+") as f:
            f.write(message + "\n")

        text = TextComponent(
            content=message,
            details=details or "No details",
            max_width=self.width
        )

        if len(self.buffer) > self.buffer_size:
            self.buffer.pop(0)
            self.scroll -= 1

        self.buffer.append(text)
        
        if self.cursor_y == self.lines - self.scroll - 2 and self.cursor_y < self.height - 1:
            self._move_cursor(0, 1)

        if len(self.buffer) > self.height:
            self.scroll += len(text.lines)

        self.render()

    def update(self) -> None:
        k = self._getch()
        if k != -1:
            self.on_keypress(k)

    def clear(self) -> None:
        self.buffer.clear()
        self.scroll = 0
        self.cursor_x = 0
        self.cursor_y = 0

    def quit(self) -> None:
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()
        exit()

    def on_command(self, command: str) -> None:
        self.log(f"Command executed: /{self.command}")

    def on_keypress(self, key: str) -> None:
        match self.state:
            case State.COMMAND:
                match key:
                    case Key.ESCAPE:
                        self.state = State.LOGS
                        self.command = ""
                    case Key.BACKSPACE:
                        if len(self.command) > 0:
                            self.command = self.command[:-1]
                    case Key.ENTER:
                        self.on_command(self.command)
                        self.state = State.LOGS
                        self.command = ""
                    case _:
                        if len(self.command) < self.width - 2 and 32 <= key <= 126:
                            self.command += chr(key)
            case State.DETAILS:
                match key:
                    case Key.ESCAPE:
                        self.state = State.LOGS
            case _:
                match key:
                    case Key.ESCAPE:
                        self.quit()
                    case Key.CTRL_L:
                        self.clear()
                    case Key.END:
                        self._move_cursor(0, len(self.buffer))
                    case Key.HOME:
                        self._move_cursor(0, -len(self.buffer))
                    case Key.ENTER:
                        self.state = State.DETAILS
                    case Key.SLASH:
                        self.state = State.COMMAND
                    case Key.UP | Key.K:
                        self._move_cursor(0, -1)
                    case Key.DOWN | Key.J:
                        self._move_cursor(0, 1)
                    case Key.RESIZE:
                        self.on_resize()
                    case _:
                        pass

        self.render()
            
    def on_resize(self) -> None:
        self.height, self.width = self._getmaxyx()
        self.scroll = max(0, len(self.buffer) - self.height)
        self.cursor_x = max(0, min(self.width - 1, self.cursor_x))
        self.cursor_y = max(0, min(self.height - 1, self.cursor_y))

    def render(self) -> None:
        # Top text
        self.screen.clear()

        match self.state:
            case State.DETAILS:
                for i, line in enumerate(self._get_text(self.current_line).details):
                    self.screen.addstr(i, 0, line)
            case _:
                lines = 0
                for i in range(self.height):
                    if i + self.scroll < len(self.buffer):
                        for line in self.buffer[i + self.scroll].lines:
                            self.screen.addstr(lines, 0, line)
                            lines += 1

        # Bottom text
        match self.state:
            case State.COMMAND:
                text = f"/{self.command}"
            case State.DETAILS:
                text = "[ESC]quit"
            case _:
                text = "[ESC]quit | [^L]clear | [ENTER]details | [/]command"

        self.screen.addstr(self.height, 0, text)

        # Move cursor
        match self.state:
            case State.COMMAND:
                self.screen.move(self.height, len(self.command) + 1)
            case State.DETAILS:
                self.screen.move(self.height - 1, 0)
            case _:
                self.screen.move(self.cursor_y, self.cursor_x)
        self.screen.refresh()

    @property
    def current_line(self) -> int:
        return self.cursor_y + self.scroll

    @property
    def lines(self) -> int:
        lines = 0
        for text in self.buffer:
            lines += len(text.lines)
        return lines

    def _getmaxyx(self) -> tuple[int, int]:
        rows, cols = self.screen.getmaxyx()
        return rows - 1, cols

    def _getch(self) -> str | None:
        return self.screen.getch()

    def _move_cursor(self, x: int, y: int) -> None:
        if self.cursor_y + y < 0:
            self.scroll = max(0, self.scroll + y)
        elif self.cursor_y + y >= self.height:
            self.scroll = min(self.lines - self.height, self.scroll + y)

        self.cursor_x = max(0, min(self.width - 1, self.cursor_x + x))
        self.cursor_y = max(0, min(self.lines - self.scroll - 1, self.cursor_y + y, self.height - 1))

    def _get_text(self, line: int) -> TextComponent:
        current = 0
        for text in self.buffer:
            current += len(text.lines)
            if current > line:
                return text
        return None


console = Console()
console.run()