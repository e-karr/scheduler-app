# Kaw Valley Kickball League Schedule Generator

The goal of this project is to create an interactive UI for the [Kaw Valley Kickball League](kawvalleykickball.com)
to generate a season schedule.

The projects incorporates different scheduling algorithms to help users generate a schedule that takes into account competitive matchups and allows for variety in teams played.

## User Input

The project aims to be dynamic to the user needs. The user inputs the following values:

- Team names with corresponding ranks
- Number of weeks desired for season
- (Future) Desired scheduling algorithm

## Available Schedule Algorithms

- Weighted Random
  - Weights are generated for possible matchups based on the team rank difference
  - Schedule is random, but matchups with a lower rank difference have a higher chance of being selected

The goal is to add multiple schedule algorithms for the user to select from, based on the type of schedule they aim to generate.

## Validations

- Check that desired season length is over 0 but fewer than the number of total teams, as a team cannot play themselves.

To ensure a valid schedule, the program does the following checks:

- Each team has one game per week
- No repeat matchups across the whole season

## Season Balance Report

The program gives feedback to the user on the matchup balance for the season. The balance report:

1. Calculates the rank difference for each matchup in a week
2. Calculates the average rank difference for each week
3. Calculates the season average rank difference
4. Determines the quality ratio with `season_avg_diff / max_possible_diff`

- Quality ratio <= .25 is Excellent
- Quality ratio > .25 and <= .40 is Good
- Quality ratio >.40 and <= .55 is Moderate
- Quality ratio >.55 is Low

Example report:

```
========================================
       SEASON BALANCE REPORT
========================================
Week 1   | Avg Rank Diff: 7.11
Week 2   | Avg Rank Diff: 10.11
Week 3   | Avg Rank Diff: 10.00
Week 4   | Avg Rank Diff: 10.00
Week 5   | Avg Rank Diff: 11.44
Week 6   | Avg Rank Diff: 9.22
Week 7   | Avg Rank Diff: 11.22
Week 8   | Avg Rank Diff: 10.78
Week 9   | Avg Rank Diff: 9.56
Week 10  | Avg Rank Diff: 10.11
----------------------------------------
Total Teams:           36
Max Possible Diff:     35
Season Avg Diff:       9.96
----------------------------------------
STATUS: GOOD: Balanced matchups. The weighting is clearly working.
========================================
```

## Upcoming Features

- Better organized and DRY code
- Additional schedule algorithms
- UI
  - Form to enter number of teams, ranks, and team names
  - Enter desired season length
  - Choose schedule algorithm
  - Reveal schedule week by week, matchup by matchup, or all at once
  - Save schedule generation history
- CICD
- Hosted in AWS
