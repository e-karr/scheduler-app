from pathlib import Path
import random
import pandas as pd

def get_file_path() -> Path:
    # Read file with team names and ranks
    print('Enter file path to csv with teams and ranks:')

    file_path = input()
    file_path = Path(file_path)

    if file_path.suffix != '.csv':
        print('File path must be to a csv. Try again')
        file_path = get_file_path()

    return file_path

def get_schedule_length() -> int:
    print('Entered desired schedule length:')
    length = input()

    try:
        length = int(length)
    except Exception:
        print('Schedule length must be a valid integer')
        length = get_schedule_length()
    
    return length

file_path = get_file_path()

team_ranks_df = pd.read_csv(file_path)
total_teams = len(team_ranks_df)

# Validate Rank and Name columns
if 'rank' not in team_ranks_df.columns or 'name' not in team_ranks_df.columns:
    raise ValueError('ERROR: csv must contain "rank" and "name" columns')

# Enter how many weeks of matchups to create
num_weeks = get_schedule_length()

while num_weeks == 0 or num_weeks >= total_teams:
    print('Schedule length must be between 0 and the total number of teams in your csv')
    num_weeks = get_schedule_length()

print(f'Building a {num_weeks} week schedule for you!')

# get all available matchups & matchup ranks
# 1. Create the Cross Join (Every team paired with every team)
matchup_df = team_ranks_df.merge(team_ranks_df, how='cross', suffixes=('_a', '_b'))

# 2. Filter: Keep only unique pairs (A vs B, not B vs A) and remove self-matchups
# Using '<' ensures we only keep one version of the pair and no team plays itself
matchup_df = matchup_df[matchup_df['name_a'] < matchup_df['name_b']].copy()

# 3. Calculate Weight (Higher weight for closer ranks)
matchup_df['diff'] = (matchup_df['rank_a'] - matchup_df['rank_b']).abs()
matchup_df['weight'] = (total_teams - matchup_df['diff'])

# print(matchup_df)

# 4. Convert to a list of records for easier manipulation during scheduling
matchup_pool = matchup_df.to_dict('records')

# generate schedule
full_schedule = {}
all_teams = team_ranks_df['name'].to_list()
total_games_per_week = len(all_teams) / 2

for week in range(1, num_weeks + 1):
    success = False

    while not success:
        # Create a temporary copy of the pool to test selections
        # We only permanently remove matchups from the master pool once the week is VALID
        temp_pool = matchup_pool.copy()
        temp_week_games = []
        teams_available_this_week = all_teams.copy()

        while len(teams_available_this_week) > 1:
            # Filter pool for teams available THIS week
            valid_options = [
                m for m in temp_pool 
                if m['name_a'] in teams_available_this_week 
                and m['name_b'] in teams_available_this_week
            ]
            
            if not valid_options:
                # STUCK: No valid matchups left for remaining teams
                # The 'while not success' loop will now restart this week from scratch
                break

            weights = [m['weight'] for m in valid_options]
            chosen = random.choices(valid_options, weights=weights, k=1)[0]

            temp_week_games.append(chosen)
            teams_available_this_week.remove(chosen['name_a'])
            teams_available_this_week.remove(chosen['name_b'])
            temp_pool.remove(chosen)

            # Check if we successfully filled the week
        if len(temp_week_games) == total_games_per_week:
            # SUCCESS: Permanent updates
            matchup_pool = temp_pool # The master pool now reflects the games played
            full_schedule[f"Week {week}"] = temp_week_games
            success = True
            print(f"Week {week} generated successfully.")

# --- VALIDATION BLOCK ---
all_checks_passed = True
teams_list = team_ranks_df['name'].to_list()
num_teams = len(teams_list)
expected_games_per_week = num_teams // 2

# Track all matchups to check for repeats
master_matchup_tracker = set()

for week, games in full_schedule.items():
    teams_this_week = []
    
    # Check 1: Correct number of games
    if len(games) != expected_games_per_week:
        print(f"❌ {week} error: Expected {expected_games_per_week} games, found {len(games)}.")
        all_checks_passed = False

    for game in games:
        # Create a sorted tuple to track the matchup regardless of order
        matchup = tuple(sorted([game['name_a'], game['name_b']]))
        
        # Check 2: No repeat matchups across the whole season
        if matchup in master_matchup_tracker:
            print(f"❌ Repeat Matchup error: {matchup} found in {week} but they already played!")
            all_checks_passed = False
        master_matchup_tracker.add(matchup)
        
        # Add teams to our weekly participation list
        teams_this_week.extend([game['name_a'], game['name_b']])

    # Check 3: Every team plays exactly once per week
    if len(set(teams_this_week)) != num_teams:
        print(f"❌ {week} error: Some teams are missing or playing twice. (Unique teams: {len(set(teams_this_week))})")
        all_checks_passed = False

if all_checks_passed:
    print("✅ Schedule Validation Passed: All constraints met!")

    # Create easy to read final schedule
    export_data = []

    for week_name, games in full_schedule.items():
        # Since we saved 'temp_week_games' as a list of dicts in the previous step...
        for game in games:
            # If games are strings, you'd split them; 
            # but it's cleaner to save the actual dicts during the loop.
            export_data.append({
                "Week": week_name,
                "Team A": game['name_a'],
                "Rank A": game['rank_a'],
                "Team B": game['name_b'],
                "Rank B": game['rank_b']
            })

    # Convert to DataFrame
    schedule_df = pd.DataFrame(export_data)
    # print(schedule_df)

    # Save to CSV
    schedule_df.to_csv("final_schedule.csv", index=False)
else:
    print("⚠️ Schedule Validation Failed. Please check the errors above.")

# --- SEASON BALANCE CHECK WITH DYNAMIC INTERPRETATION ---
print("\n" + "="*40)
print("       SEASON BALANCE REPORT")
print("="*40)

total_diff = 0
total_games = 0
num_teams = len(all_teams)
max_possible_diff = num_teams - 1

for week_name, games in full_schedule.items():
    # Calculate the rank difference for every game in this specific week
    # 'games' contains the dictionaries with 'rank_a' and 'rank_b'
    week_diffs = [abs(g['rank_a'] - g['rank_b']) for g in games]
    
    avg_week_diff = sum(week_diffs) / len(week_diffs)
    total_diff += sum(week_diffs)
    total_games += len(games)
    
    print(f"{week_name:8} | Avg Rank Diff: {avg_week_diff:.2f}")

# Final Calculation
season_avg_diff = total_diff / total_games

# Dynamic Thresholds based on league size
# We compare the actual average diff to the max possible diff
quality_ratio = season_avg_diff / max_possible_diff

print("-" * 40)
print(f"Total Teams:           {num_teams}")
print(f"Max Possible Diff:     {max_possible_diff}")
print(f"Season Avg Diff:       {season_avg_diff:.2f}")
print("-" * 40)

# Interpretation Logic
if quality_ratio <= 0.25:
    status = "EXCELLENT: Highly competitive. Teams are playing very close seeds."
elif quality_ratio <= 0.40:
    status = "GOOD: Balanced matchups. The weighting is clearly working."
elif quality_ratio <= 0.55:
    status = "MODERATE: Fairly spread out. Close to a standard random draw."
else:
    status = "LOW: High rank disparity. Consider increasing your weight exponent."

print(f"STATUS: {status}")
print("="*40)

