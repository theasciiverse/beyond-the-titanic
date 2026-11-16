#!/usr/bin/env python3
"""Records asciiverse/beyond-the-titanic.cast, the catalog preview, at
100x30 (hub/RECORDING.md): the title, the night of April 14, 1912 on the
Titanic's deck, a walk to the lifeboats, the iceberg, and the survival kit,
typed at a human pace, with a throwaway HOME so a fresh game starts. Run
after asciiverse/build.sh and asciiverse/package.sh:
    python3 asciiverse/record-preview.py stage/beyond-the-titanic"""
import fcntl, json, os, pty, select, shutil, struct, sys, tempfile, termios, time

MOVES = [("examine rail", 3.0), ("e", 4.0), ("examine lifeboats", 2.5),
         ("n", 7.0), ("open kit", 2.0), ("examine kit", 3.0), ("get all", 3.0)]

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
game_dir = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else f"{root}/stage/beyond-the-titanic")
cast = f"{root}/asciiverse/beyond-the-titanic.cast"
home = tempfile.mkdtemp()
env = dict(os.environ, HOME=home, TERM="xterm-256color", LANG="C.UTF-8",
           USER="player", LOGNAME="player",
           PATH=game_dir + os.pathsep + os.environ.get("PATH", ""))
for k in ("XDG_STATE_HOME", "NO_COLOR", "BEYOND_THE_TITANIC_LOG"):
    env.pop(k, None)

pid, fd = pty.fork()
if pid == 0:
    os.execvpe("asciinema", ["asciinema", "rec", "--overwrite", "-q", "-i", "2",
        "--window-size", "100x30", "--capture-env", "TERM,LANG",
        "--title", "Beyond the Titanic", "-c", "beyond-the-titanic", cast], env)
fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", 30, 100, 0, 0))


def pump(t):
    end = time.time() + t
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 0.03)
        if r:
            try:
                os.read(fd, 65536)
            except OSError:
                return


def type_line(line, after):
    for c in line:
        os.write(fd, c.encode()); pump(0.09)
    os.write(fd, b"\r"); pump(after)


pump(3.0)                       # the title screen
os.write(fd, b" "); pump(7.0)   # time to read the opening
for move, after in MOVES:
    type_line(move, after)
type_line("quit", 1.0)
os.write(fd, b"n"); pump(0.8)
os.write(fd, b"y"); pump(2.0)
for _ in range(50):
    if os.waitpid(pid, os.WNOHANG)[0]:
        break
    time.sleep(0.2)
shutil.rmtree(home, ignore_errors=True)

# asciinema writes the command it ran into the header; players never use
# it, so it is taken out
with open(cast) as f:
    lines = f.read().split("\n")
head = json.loads(lines[0])
head.pop("command", None)
lines[0] = json.dumps(head, separators=(",", ":"))
with open(cast, "w") as f:
    f.write("\n".join(lines))
print(cast, os.path.getsize(cast), "bytes")
