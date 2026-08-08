#!/usr/bin/env python3
import os
import json

def calculate_and_verify_budget(json_path):
    # Verify file existence
    if not os.path.exists(json_path):
        print(f"[-] Error: Target data file not found at {json_path}")
        return

    # Load the mock actuarial JSON data
    with open(json_path, 'r') as file:
        data = json.load(file)

    print(f"[+] Successfully loaded: {data['target_facility']['name']}")
    print(f"[+] Modeling Fiscal Year: {data['fiscal_year']}")
    print("-" * 60)

    # Extract formula parameters from JSON
    params = data['formula_parameters']
    baselines = params['historical_baseline_costs_base_p']
    scaling = params['scaling_factors']
    
    delta_pop = scaling['delta_pop']
    delta_cmi = scaling['delta_cmi']
    floor_rural = params['fixed_insulation']['floor_rural_usd']
    kappa_bonus = params['performance_modifiers']['metrics']['performance_bonus_earned_usd']

    # Step 1: Calculate the Sum of Base_p
    sum_base_p = sum(payer['historical_3yr_rolling_average_usd'] for payer in baselines)
    print(f"[*] Combined Payer Baseline (Sum of Base_p): ${sum_base_p:,.2f}")

    # Step 2: Apply Demographic and Case-Mix Scaling Factors
    # Formula Component: Base_p * (1 + Delta_Pop + Delta_CMI)
    scaling_multiplier = 1 + delta_pop + delta_cmi
    scaled_base = sum_base_p * scaling_multiplier
    print(f"[*] Applied Scaling Multiplier ({scaling_multiplier:.3f}): ${scaled_base:,.2f}")

    # Step 3: Integrate Fixed Insulation Floor and Performance Modifiers
    # Formula: B_t = Scaled_Base + Floor_Rural + Kappa_Quality
    calculated_bt = scaled_base + floor_rural + kappa_bonus
    print(f"[*] Rural Insulation Floor Added: +${floor_rural:,.2f}")
    print(f"[*] Performance Quality Bonus Added: +${kappa_bonus:,.2f}")
    print("-" * 60)

    # Step 4: Validate against the JSON's recorded actuarial output
    expected_bt = data['actuarial_output']['calculated_global_budget_bt_usd']
    print(f"[=] Expected Budget from Ledger: ${expected_bt:,.2f}")
    print(f"[=] Computed Formula Output:    ${calculated_bt:,.2f}")

    if abs(calculated_bt - expected_bt) < 0.01:
        print("\n[✔] SUCCESS: Actuarial output matches formula parameters perfectly!")
        print(f"[✔] Quarterly Disbursement Target: ${data['actuarial_output']['disbursement_per_quarter_usd']:,.2f}")
    else:
        print("\n[❌] ERROR: Calculated budget mismatch. Please audit parameter values.")

if __name__ == "__main__":
    # Point directly to the new operations data path
    target_json = os.path.join("CAMPAIGN_OPS", "data", "global_budget_mock.json")
    calculate_and_verify_budget(target_json)
