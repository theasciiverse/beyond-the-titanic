# Changes from upstream

This is the Asciiverse packaging of Beyond the Titanic, Scott Miller's
text adventure (begun in 1984, published in 1986). Upstream is Jason
Self's free-software revival, https://jxself.org/git/beyond-the-titanic.git,
the `upstream` remote: its first commit is Apogee Software's source
release of March 20, 2009 (GPL-2.0-or-later), and his commits of May and
June 2014 bring it to Free Pascal so it builds and runs on modern
systems. This build is his `master` at `6cb4785` (2014-06-09). Upstream
names no version, so releases here are tagged `v1.0+20140609-av.N`. The
`asciiverse` branch carries the changes below, one commit each.

Licence: Apogee released the game under GPL-2.0-or-later; Jason Self
took it to GPL-3.0-or-later (`gpl-3.0.txt`) and put his changes under
AGPL-3.0-or-later (`agpl-3.0.txt`), as permitted by section 13 of each
licence. Our changes are AGPL-3.0-or-later too, so the program as a
whole is AGPL-3.0-or-later.

## The game

Unchanged: the parser, the vocabulary, the rooms, puzzles, timers,
scoring and every text, in `src/*.PAS` and the data files ROOMS1,
ROOMS2, SPECIAL1, SPECIAL2 and LINE. The resource editors (ROOMRITE,
LINERITE, SPECIAL) are not built.

## Ours

- **Any terminal, through avcrt.** `src/avcrt.pas`, new, stands in for
  Turbo Pascal's Crt unit: the same calls (Window, GotoXY, TextColor,
  ReadKey and the rest), drawn on a terminal of any size on Linux, macOS
  and Windows. The PC's characters are written as UTF-8 and its colours
  as ANSI colours, on the alternate screen, which is restored on exit,
  also after Ctrl+C. Text written to the story window is word-wrapped at
  its edge; rows that scroll off its top are kept, so the player can page
  back (Shift+PgUp, Shift+PgDn) and the story is laid out again at the
  new width when the terminal is resized. The PC speaker is silent:
  `Sound` and `NoSound` do nothing. In the game the status bar spans the
  top row and the story the rest (it was 80x25), the death and victory
  banners span the width at the same rows from the bottom, and centred
  text is centred in the actual width. `BEYOND.PAS`, `COMMANDS.PAS`.
- **The game's texts laid out to the width.** The descriptions and
  messages in the data files were laid out for 80 columns by padding
  lines with spaces, and some words met at the edge with no space
  between them ("arethe"). RR, RS and RL write them through AvShowText,
  which takes the padding out and keeps the breaks the author meant
  (indented lines, empty lines, lines ending well before the edge).
  `ADPARSER.PAS`.
- **A line editor for commands**, with earlier commands on Up and Down,
  in place of ReadLn; at most 77 characters, as before. `BEYOND.PAS`.
- **Data beside the program, saves in the state folder.** The game
  opened its data files in the current folder, so it had to be started
  from `src`, and saved to a SAVE/RESTORE disk in drive B: (a file named
  `B:name.a` in the current folder). It now finds the data beside the
  program, saying so plainly when it cannot, and keeps saved games in
  `$XDG_STATE_HOME/beyond-the-titanic`, else
  `~/.local/state/beyond-the-titanic` (Linux and macOS), or
  `%LOCALAPPDATA%\beyond-the-titanic` on Windows. SAVE and RESTORE ask
  for a name (letters, digits, `-` and `_`) and act at once, with no disk
  to swap; RESTORE lists the saved games first. `COMMANDS.PAS`.
- **Restart, quit and the ending.** RESTART, and "play again" after a
  death, started a second copy of the game (`ExecuteProcess('beyond')`)
  from inside the first, which kept running underneath; now the game
  starts again in place of the running one. Declining to play again said
  goodbye and then carried on (the jump to MENU.COM never happened); now
  it ends. After winning the game looped forever; now it waits for a key
  and ends. `BEYOND.PAS`, `COMMANDS.PAS`.
- **Colour, and the title screen.** The game opened with two questions
  for 1980s hardware, a colour screen and the number of disk drives,
  which the 2014 version answered itself (monochrome, two drives) while
  the title and shareware screens flashed past unseen. Now it plays in
  the original's colour scheme (its monochrome one when `NO_COLOR` is
  set), the questions are not shown, and the title screen waits for a
  key. The shareware screen, which asked for a $5 or $10 cheque, is left
  out: Apogee ended registration. `COMMANDS.PAS`.
- **Session log behind `BEYOND_THE_TITANIC_LOG`.** Set it to anything
  and `beyond-the-titanic.log` in the state folder gets, appended, every
  key as it arrives, every command line, the story as it is written,
  each turn's move, score, room and number of things carried, saves and
  restores, deaths, the win and resizes. Without it nothing is written.
  `BEYOND.PAS`, `COMMANDS.PAS`, `avcrt.pas`.
- **A README.md** on playing it with av.

## Packaging (new files)

- `asciiverse/build.sh`: builds `out/beyond-the-titanic` with Free
  Pascal 3.2.2 (`-Sg` for the game's gotos, stripped, smart-linked); the
  compiler and target flags come from the environment. Linux binaries
  are static.
- `asciiverse/package.sh`: lays out each av archive (the program, its
  five data files, README.md, PATCHES.md, INSTRUCT.TXT and the two
  licences).
- `asciiverse/smoke.py`: plays a few turns in a 100x30 pseudo-terminal
  (title, first room, a move, a save, the log, QUIT); run on every Linux
  and macOS build.
- `asciiverse/beyond-the-titanic.cast` and `asciiverse/record-preview.py`:
  the catalog preview and the script that records it.
- `.github/workflows/release.yml`: builds, tests and releases all of it
  on a tag.
- `.gitignore`: build output of the above.
