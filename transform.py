import os
import json
import pandas as pd
from glob import glob

def parse_match_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        match_data = json.load(f)

    match_id = os.path.basename(file_path).replace('.json', '')
    metadata = match_data.get("info", {})
    teams = metadata.get("teams", ["NA", "NA"])
    date = metadata.get("dates", ["NA"])[0]
    venue = metadata.get("venue", "NA")
    match_type = metadata.get("match_type", "NA")
    toss_winner = metadata.get("toss", {}).get("winner", "NA")
    toss_decision = metadata.get("toss", {}).get("decision", "NA")
    winner = metadata.get("outcome", {}).get("winner", "NA")

    records = []

    for innings in match_data.get("innings", []):
        inning_name = innings.get("team", "NA")
        deliveries = innings.get("deliveries", [])
        for delivery in deliveries:
            for ball_key, ball_val in delivery.items():
                over = ball_key
                batter = ball_val.get("batter", "NA")
                bowler = ball_val.get("bowler", "NA")
                runs = ball_val.get("runs", {}).get("batter", 0)
                extras = ball_val.get("runs", {}).get("extras", 0)
                total_runs = ball_val.get("runs", {}).get("total", 0)
                wicket = ball_val.get("wicket", {}).get("kind", None)

                records.append({
                    "match_id": match_id,
                    "date": date,
                    "venue": venue,
                    "match_type": match_type,
                    "team_1": teams[0],
                    "team_2": teams[1],
                    "batting_team": inning_name,
                    "batter": batter,
                    "bowler": bowler,
                    "runs": runs,
                    "extras": extras,
                    "total_runs": total_runs,
                    "wicket": wicket,
                    "over_ball": over,
                    "toss_winner": toss_winner,
                    "toss_decision": toss_decision,
                    "winner": winner
                })

    return records

def process_all_matches(match_type_dir):
    all_data = []
    files = glob(os.path.join(match_type_dir, '*.json'))

    for file in files:
        match_records = parse_match_json(file)
        all_data.extend(match_records)

    return pd.DataFrame(all_data)

# ODI Example
odi_df = process_all_matches('cricsheet/tests_json')
print(odi_df.head())
odi_df.to_csv('odi_matches_cleaned.csv', index=False)

