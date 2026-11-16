# Beyond the Titanic

April 14, 1912, 11:43 PM. You are on the starboard deck of the Titanic,
gazing at the stars over an icy sea, and the ship everyone calls
unsinkable is minutes from the iceberg. Survive the night, and the
lifeboat is only the beginning: a whirlpool, caverns under the sea, an
alien saucer buried by an ancient rockfall, and a long way home
to San Francisco.

Scott Miller's text adventure, begun in 1984 and published in 1986,
before he founded Apogee. Type what you want to do, in plain English,
as many commands to a line as you like: **open hatch then climb down
the ladder. read screen.**

## Play

With [av](https://asciiverse.sh), the Asciiverse client:

```
av install beyond-the-titanic
av play beyond-the-titanic
```

- Type a command and press Enter. Several commands on one line, with
  periods or THEN between them. INSTRUCT.TXT has the game's own
  instructions and the words it knows.
- **Up** and **Down** bring back earlier commands; **Left**, **Right**,
  **Home**, **End**, **Backspace** and **Delete** edit the line.
- **PgUp** and **PgDn** (or with Shift) page back through the story.
- **SAVE** and **RESTORE** ask for a name. Saved games are kept in
  `$XDG_STATE_HOME/beyond-the-titanic` (usually
  `~/.local/state/beyond-the-titanic`), or
  `%LOCALAPPDATA%\beyond-the-titanic` on Windows.
- **QUIT** ends the game, **RESTART** begins it again.
- Set `NO_COLOR` for the game's black and white scheme, and
  `BEYOND_THE_TITANIC_LOG=1` to keep a log of the session in
  `beyond-the-titanic.log` in the state folder.

The game fills the terminal, whatever its size (80x24 or more), and lays
its text out again when the terminal is resized.

## Credits

Scott Miller wrote Beyond the Titanic in Turbo Pascal, beginning on May
12, 1984; it was published in 1986 as shareware, then sold by Apogee
Software. Apogee made it freeware in March 1998 and released its source
code under the GNU GPL (version 2 or later) on March 20, 2009. In 2014
Jason Self brought the source to Free Pascal so it builds and runs on
modern systems without an emulator (https://jxself.org/beyond-the-titanic.shtml,
https://jxself.org/git/beyond-the-titanic.git); his history of the
release is in `History/`.

Licence: the game is GPL-3.0-or-later (`gpl-3.0.txt`), Jason Self's
changes and ours are AGPL-3.0-or-later (`agpl-3.0.txt`), so the program
as a whole is AGPL-3.0-or-later.

This is the build for the Asciiverse catalog: the game is unchanged, and
what changed around it (the screen, line editing, saves, logging) is in
PATCHES.md. To build it yourself you need Free Pascal 3.2.2:
`asciiverse/build.sh` makes `out/beyond-the-titanic`, which looks for its
data files (ROOMS1, ROOMS2, SPECIAL1, SPECIAL2, LINE, from `src/`) beside
itself.
