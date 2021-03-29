# Voting Game

Some exploratory code for a final project for the AI master course "Computational Social Choice" at the University of Groningen.
The code currently implements the amendment procedure from [Barberà and Salvador (2017)][1].

## Usage

### Creating voting profiles

You can supply a voting profile as a `.csv` or `.txt` file.
For the `.csv`, the program expects column headers indicating the voter ids.
Columns indicate the linear order of preferences, e.g. the file

```
1, 2, 3
a, b, c
c, a, b
b, c, a
```

represents the profile

```
1 │ a c b
2 │ b a c
3 │ c b a
```

When using a `.txt` file, the expected format is the following:

```
1: a c b
2: b a c
3: c b a
```

This represents the same profile as the one in the CSV.

### Running a voting game

To run a sequential voting game, first create a game:

```python
game = Game( game_type = GameType.AMENDMENT
           , agenda = ['a', 'b', 'c'] 
           , quota = 1
           , profile = Profile.from_txt("profile.txt")
           )
```

Then, compute the outcome:

```python
outcome = game.outcome()
```

[1]: <http://doi.wiley.com/10.3982/TE2118>