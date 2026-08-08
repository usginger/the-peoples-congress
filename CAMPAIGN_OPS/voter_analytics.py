#!/usr/bin/env python3
import os
import csv
import json

def load_precinct_data(csv_path):
    """Loads raw precinct turnout histories from the campaign data directory."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"[-] Missing precinct database file: {csv_path}")
        
    precincts = []
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            precincts.append({
                "precinct_id": row["precinct_id"],
                "county": row["county"],
                "registered_voters": int(row["registered_voters"]),
                "historical_turnout_2022": int(row["historical_turnout_2022"]),
                "historical_turnout_2024": int(row["historical_turnout_2024"]),
                "demographic_senior_pct": float(row["demographic_senior_pct"])
            })
    return precincts

def calculate_priority_scores(precincts, output_json_path):
    """
    Parses turnouts, detects mobilization opportunities, and scores precincts.
    Higher priority scores point to regions with high senior populations 
    impacted by DMV/Health access issues but historically low turnouts.
    """
    targeted_outputs = []
    
    print(f"[+] Processing {len(precincts)} geographic precincts...")
    print("-" * 65)

    for p in precincts:
        # Calculate historical baseline turnout averages
        avg_turnout_vol = (p["historical_turnout_2022"] + p["historical_turnout_2024"]) / 2
        turnout_rate = avg_turnout_vol / p["registered_voters"]
        
        # Core Analytics Logic: Find high registration pools with weak participation
        unrealized_voter_pool = p["registered_voters"] - avg_turnout_vol
        
        # Priority Multiplier: Weigh heavier in areas with high density of seniors (DMV / Health platform focus)
        priority_score = round((unrealized_voter_pool * (p["demographic_senior_pct"] / 100.0)), 2)
        
        targeted_outputs.append({
            "precinct_id": p["precinct_id"],
            "county": p["county"],
            "metrics": {
                "turnout_rate_pct": round(turnout_rate * 100, 2),
                "unrealized_voters_count": int(unrealized_voter_pool),
                "senior_density_pct": p["demographic_senior_pct"]
            },
            "targeting": {
                "priority_score": priority_score,
                "tier": "TIER_1_URGENT" if priority_score > 500 else "TIER_2_STANDARD"
            }
        })

    # Sort database entries by highest priority first
    targeted_outputs.sort(key=lambda x: x["targeting"]["priority_score"], reverse=True)

    # Save processed analytics ledger
    with open(output_json_path, 'w', encoding='utf-8') as out_file:
        json.dump(targeted_outputs, out_file, indent=2)
        
    return targeted_outputs

def display_top_targets(scored_data, limit=3):
    """Prints out top high-priority targets for volunteer deployments."""
    print(f"[✔] Top {limit} High-Priority Campaign Targets Extracted:")
    for idx, item in enumerate(scored_data[:limit], 1):
        print(f" {idx}. Precinct: {item['precinct_id']} ({item['county']} County)")
        print(f"    - Priority Score: {item['targeting']['priority_score']}")
        print(f"    - Target Tier:    {item['targeting']['tier']}")
        print(f"    - Senior Density: {item['metrics']['senior_density_pct']}%")
        print(f"    - Unused Votes:   {item['metrics']['unrealized_voters_count']} voters")
        print("-" * 65)

if __name__ == "__main__":
    # Relative repository execution pathing
    input_csv = os.path.join("CAMPAIGN_OPS", "data", "voter_precincts_raw.csv")
    output_json = os.path.join("CAMPAIGN_OPS", "data", "voter_priority_analytics.json")
    
    try:
        raw_data = load_precinct_data(input_csv)
        results = calculate_priority_scores(raw_data, output_json)
        display_top_targets(results)
        print(f"[+] Operational data ledger written safely to: {output_json}")
    except Exception as e:
        print(f"[❌] Analytics Engine Error: {e}")


   
