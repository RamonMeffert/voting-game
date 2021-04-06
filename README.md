# Voting Game

Some exploratory code for a final project for the AI master course "Computational Social Choice" at the University of Groningen.
The code currently implements the amendment and successive procedures from [Barberà and Salvador (2017)][1].

## Usage

### Creating voting profiles

You can supply a voting profile as a `.csv`, `.txt` or [PrefLib](https://www.preflib.org) [`.soc`](https://www.preflib.org/data/format.php#soc) file.
For the `.csv`, the program expects column headers indicating the voter ids.
Columns indicate the linear order of preferences, e.g. the file

```csv
1, 2, 3
a, b, c
c, a, b
b, c, a
```

represents the profile

```text
1 │ a c b
2 │ b a c
3 │ c b a
```

When using a `.txt` file, the expected format is the following:

```text
1: a c b
2: b a c
3: c b a
```

This represents the same profile as the one in the CSV.

For `.soc` files, the expected format can be found [here](https://www.preflib.org/data/format.php#election-data).

### Running a voting game

To run a sequential voting game, first create a game:

```python
game = Game( type = GameType.AMENDMENT
           , agenda = ['a', 'b', 'c'] 
           , quota = 1
           , profile = Profile.from_txt("profile.txt")
           )
```

Then, compute the outcome:

```python
outcome = game.outcome()
```

### Analysing a voting game

To analyse a voting game, create an `Analysis` object:

```python
profile = Profile.from_soc("profile.soc")

# You can optionally supply an expected winner
expected_outcome = profile.winner(Rule.BORDA)

analysis = Analysis( type = GameType.AMENDMENT
                   , profile = profile
                   , quota = 2
                   , expected_outcome = expected_outcome
                   )
```

Then, find all possible outcomes:

```python
outcomes = analysis.outcomes()
```

If an expected outcome was specified, this will also print how often that outcome occurred. This can be seen as an indication of the manipulability of a game type in some situations: if the expected winner is often different from the winner of the game, then the agenda has a large influence on the outcome. Similarly, if there are many different outcomes for some game, this also indicates the game type could be manipulable.

[1]: <http://doi.wiley.com/10.3982/TE2118>