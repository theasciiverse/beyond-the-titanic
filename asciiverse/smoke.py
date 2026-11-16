#!/usr/bin/env python3
"""Plays a few turns of the game in a 100x30 pseudo-terminal and checks
what it shows: the title, the first room, a move, a save in the state
folder, the session log, and a clean quit.

  python3 asciiverse/smoke.py out/beyond-the-titanic
"""
import fcntl, os, pty, select, struct, sys, tempfile, termios, time

GAME = sys.argv[1]
STEPS = [  # wait for this, then send that
    ("Press any key", "x"),
    ("Ship's Fore", "e\r"),
    ("Ship Mid-Deck", "save\r"),
    ("what name", "smoke\r"),
    ("SAVED", "quit\r"),
    ("SAVE your game first", "n"),
    ("still sure", "y"),
]
TIMEOUT = 60  # seconds for each step: CI machines can be slow

state = tempfile.mkdtemp()
env = dict(os.environ, TERM="xterm-256color", XDG_STATE_HOME=state,
           BEYOND_THE_TITANIC_LOG="1", LANG="C.UTF-8")
env.pop("NO_COLOR", None)
pid, fd = pty.fork()
if pid == 0:
    os.execve(GAME, [GAME], env)
fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", 30, 100, 0, 0))

seen = b""


def read_for(seconds):
    global seen
    end = time.time() + seconds
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 0.1)
        if r:
            try:
                data = os.read(fd, 65536)
            except OSError:
                return False
            if not data:
                return False
            seen = (seen + data)[-200000:]
    return True


for want, send in STEPS:
    end = time.time() + TIMEOUT
    while want.encode() not in seen:
        if time.time() > end or not read_for(0.2):
            sys.exit(f"smoke: never saw {want!r}")
    seen = b""
    os.write(fd, send.encode())
    read_for(0.3)

end = time.time() + TIMEOUT
while time.time() < end:
    done, status = os.waitpid(pid, os.WNOHANG)
    if done:
        break
    read_for(0.2)
else:
    sys.exit("smoke: the game did not end after QUIT")
if os.waitstatus_to_exitcode(status) != 0:
    sys.exit(f"smoke: exit status {status}")
folder = os.path.join(state, "beyond-the-titanic")
for name in ("smoke.a", "smoke.b", "smoke.c", "smoke.d", "beyond-the-titanic.log"):
    if not os.path.exists(os.path.join(folder, name)):
        sys.exit(f"smoke: {name} missing from the state folder")
print("smoke: ok")
