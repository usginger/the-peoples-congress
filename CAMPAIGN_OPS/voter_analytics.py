# -*- coding: utf-8 -*-
"""
CAMPAIGN_OPS/voter_analytics.py
Part of 'The People's Congress' open-source campaign infrastructure.

This script parses a standardized public voter registration file (.csv) 
to isolate and score high-priority precincts based on two factors:
1. Historical turnout trends.
2. Proximity to systemic infrastructure bottlenecks (e.g., rural healthcare deficits or long DMV wait lines).

Usage:
    python voter_analytics.py --input voter_file.csv --output priority_precincts.csv
"""

import os
import argparse
import pandas as pd

def load_voter_data(file_path):
    """Loads voter registration data from a CSV file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found at: {file_path}")
    print(f"[*] Reading voter database from {file_path}...")
    return pd.read_csv(file_path)

def score_precincts(df):
    """
    Aggregates data by precinct and applies an actionability score.
    High score = High registration + low historic turnout (prime for grassroots push).
    """
    print("[*] Processing precinct aggregates and calculating priority metrics...")
    
    # Ensure required columns exist, fill with baseline logic if simple schema
    required_cols = ['precinct_id', 'voter_status', 'historic_turnout_score', 'rural_distance_miles']
    for col in required_cols:
        if col not in df.columns:
            if col == 'voter_status': df[col] = 'Active'
            elif col == 'historic_turnout_score': df[col] = 0.5
            elif col == 'rural_distance_miles': df[col] = 5.0
            else: df[col] = df.index

    # Filter strictly to active registered voters
    active_voters = df[df['voter_status'].str.lower() == 'active']

    # Grouping data metrics by unique precinct ID
    precinct_summary = active_voters.groupby('precinct_id').agg(
        total_active_voters=('precinct_id', 'count'),
        avg_historic_turnout=('historic_turnout_score', 'mean'),
        miles_to_nearest_facility=('rural_distance_miles', 'mean')
    ).reset_index()

    # Core Algorithm: Prioritize areas with big active voter pools, low turnouts, and high infrastructure isolation
    precinct_summary['organizing_priority_score'] = (
        precinct_summary['total_active_voters'] * 
        (1.0 - precinct_summary['avg_historic_turnout']) * 
        (1.0 + (precinct_summary['miles_to_nearest_facility'] / 10.0))
    ).round(2)

    # Sort array by highest priority
    sorted_precincts = precinct_summary.sort_values(by='organizing_priority_score', ascending=False)
    return sorted_precincts

def main():
    parser = argparse.ArgumentParser(description="The People's Congress - Voter Data Analytics Tool")
    parser.add_argument('--input', type=str, default='voter_data_sample.csv', help='Path to raw voter registration CSV')
    parser.add_argument('--output', type=str, default='priority_precincts.csv', help='Path to save output priorities')
    args = parser.parse_args()

    # Self-generating sample data framework if user runs script naked to showcase system
    if not os.path.exists(args.input) and args.input == 'voter_data_sample.csv':
        print(f"[!] Input file {args.input} not found. Generating sample data for demonstration...")
        mock_data = pd.DataFrame({
            'voter_id': [f"VOTER_{i:04d}" for i in range(1, 201)],
            'precinct_id': [f"Precinct_{i}" for i in [1, 2, 3, 4] * 50],
            'voter_status': ['Active'] * 180 + ['Inactive'] * 20,
            'historic_turnout_score': [0.3, 0.7, 0.4, 0.8] * 50, 
            'rural_distance_miles': [18.5, 2.1, 14.0, 4.3] * 50 
        })
        mock_data.to_csv(args.input, index=False)

    try:
        raw_data = load_voter_data(args.input)
        priorities = score_precincts(raw_data)
        
        priorities.to_csv(args.output, index=False)
        print(f"[+] Success! Priority targeting metrics saved to: {args.output}")
        print("\n--- TOP PRIORITIES FOR GRASSROOTS FIELD OUTREACH ---")
        print(priorities.head(5).to_string(index=False))
        
    except Exception as e:
        print(f"[-] Operational Error: {e}")

if __name__ == '__main__':
    main()
