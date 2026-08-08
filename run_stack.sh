#!/usr/bin/env bash
# ==============================================================================
# THE PEOPLE'S CONGRESS - CORE OPERATING STACK AUTOMATION RUNNER
# ==============================================================================
set -e

# Visual formatting configurations
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Initializing The People's Congress Civic Tech Stack ===${NC}\n"

# Verify environment and execution directory context
if [ ! -d "CAMPAIGN_OPS" ]; then
    echo -e "[-] Error: Run this master script from the repository root directory."
    exit 1
fi

# Step 1: Execute Legislative Policy Actuarial Modeling
echo -e "${YELLOW}[Step 1/2] Launching Healthcare Actuarial Verification Model...${NC}"
if [ -f "CAMPAIGN_OPS/validate_budget.py" ]; then
    python3 CAMPAIGN_OPS/validate_budget.py
else
    echo -e "[-] Error: validate_budget.py missing from CAMPAIGN_OPS."
    exit 1
fi

echo -e ""

# Step 2: Execute Geographic Voter Turnout Analytics & Targeting Engine
echo -e "${YELLOW}[Step 2/2] Launching Precinct Voter Turnout Analytics Engine...${NC}"
if [ -f "CAMPAIGN_OPS/voter_analytics.py" ]; then
    python3 CAMPAIGN_OPS/voter_analytics.py
else
    echo -e "[-] Error: voter_analytics.py missing from CAMPAIGN_OPS."
    exit 1
fi

echo -e "${GREEN}=== All Core Systems Executed and Verified Successfully ===${NC}"

# Step 3: Execute DMV Data Pipeline Simulation
echo -e "${YELLOW}[Step 3/3] Launching DMV Secure Medical Pipeline Simulator...${NC}"
if [ -f "CAMPAIGN_OPS/simulate_dmv_pipeline.py" ]; then
    python3 CAMPAIGN_OPS/simulate_dmv_pipeline.py
else
    echo -e "[-] Error: simulate_dmv_pipeline.py missing from CAMPAIGN_OPS."
    exit 1
fi

echo -e "\n${GREEN}=== All Core Systems Executed and Verified Successfully ===${NC}"

