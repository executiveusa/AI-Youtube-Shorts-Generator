#!/usr/bin/env python3
"""
Cost Monitoring and Free Tier Protection Script

This script monitors Railway usage and triggers maintenance mode
when free-tier limits are approached.

Usage:
    python cost_monitor.py --check
    python cost_monitor.py --trigger-maintenance
"""

import os
import sys
import json
from datetime import datetime

# Configuration
FREE_TIER_LIMITS = {
    "monthly_hours": 500,
    "egress_gb": 100,
    "build_minutes": 100
}

MAINTENANCE_TRIGGER_THRESHOLD = 0.80  # 80% of free tier

def get_environment_mode():
    """Check if we're in free tier mode"""
    return os.getenv("FREE_TIER_MODE", "true").lower() == "true"

def check_cost_monitoring_enabled():
    """Check if cost monitoring is enabled"""
    return os.getenv("ENABLE_COST_MONITORING", "true").lower() == "true"

def log_message(level, message):
    """Log messages with timestamp"""
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] [{level}] {message}", file=sys.stderr)

def check_railway_usage():
    """
    Check Railway usage metrics.
    
    Note: This is a placeholder. In production, you would:
    1. Use Railway API to fetch actual usage
    2. Parse response and extract metrics
    3. Compare against FREE_TIER_LIMITS
    
    For now, this simulates the check.
    """
    log_message("INFO", "Checking Railway usage metrics...")
    
    if not check_cost_monitoring_enabled():
        log_message("INFO", "Cost monitoring is disabled")
        return {"status": "monitoring_disabled"}
    
    # Placeholder: In real implementation, call Railway API
    # import requests
    # response = requests.get("https://api.railway.app/usage", headers={"Authorization": f"Bearer {token}"})
    # usage_data = response.json()
    
    # Simulated usage data
    usage_data = {
        "monthly_hours_used": 0,  # Would be populated from API
        "egress_gb_used": 0,      # Would be populated from API
        "build_minutes_used": 0,  # Would be populated from API
        "timestamp": datetime.now().isoformat()
    }
    
    log_message("INFO", f"Current usage: {json.dumps(usage_data)}")
    
    return usage_data

def calculate_usage_percentage(usage_data):
    """Calculate percentage of free tier used"""
    percentages = {
        "hours": (usage_data.get("monthly_hours_used", 0) / FREE_TIER_LIMITS["monthly_hours"]) * 100,
        "egress": (usage_data.get("egress_gb_used", 0) / FREE_TIER_LIMITS["egress_gb"]) * 100,
        "build": (usage_data.get("build_minutes_used", 0) / FREE_TIER_LIMITS["build_minutes"]) * 100
    }
    
    max_percentage = max(percentages.values())
    
    log_message("INFO", f"Usage percentages: {json.dumps(percentages)}")
    log_message("INFO", f"Maximum usage: {max_percentage:.2f}%")
    
    return max_percentage, percentages

def should_trigger_maintenance(usage_percentage):
    """Determine if maintenance mode should be triggered"""
    threshold_percentage = MAINTENANCE_TRIGGER_THRESHOLD * 100
    
    if usage_percentage >= threshold_percentage:
        log_message("WARNING", f"Usage ({usage_percentage:.2f}%) exceeds threshold ({threshold_percentage:.2f}%)")
        return True
    else:
        log_message("INFO", f"Usage ({usage_percentage:.2f}%) is below threshold ({threshold_percentage:.2f}%)")
        return False

def trigger_maintenance_mode():
    """
    Trigger maintenance mode:
    1. Create maintenance marker file
    2. Log event
    3. Return success status
    
    Note: Actual deployment of maintenance.html would be handled by Railway or CI/CD
    """
    log_message("WARNING", "⚠️  TRIGGERING MAINTENANCE MODE")
    
    # Create maintenance marker
    marker_file = "MAINTENANCE_MODE_ACTIVE"
    with open(marker_file, "w") as f:
        f.write(json.dumps({
            "triggered_at": datetime.now().isoformat(),
            "reason": "free_tier_protection",
            "threshold": MAINTENANCE_TRIGGER_THRESHOLD,
            "action_required": "Manual intervention needed - upgrade plan or migrate to Coolify"
        }, indent=2))
    
    log_message("WARNING", f"Maintenance marker created: {marker_file}")
    log_message("WARNING", "To restore service:")
    log_message("WARNING", "  1. Upgrade Railway plan, OR")
    log_message("WARNING", "  2. Migrate to Coolify (see COOLIFY_MIGRATION.md), OR")
    log_message("WARNING", "  3. Wait for monthly reset")
    
    # In production, this would also:
    # - Call Railway API to pause service
    # - Deploy maintenance.html as static site
    # - Send notifications
    
    return True

def main():
    """Main execution"""
    if len(sys.argv) < 2:
        print("Usage: python cost_monitor.py [--check|--trigger-maintenance]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if not get_environment_mode():
        log_message("INFO", "Not in free tier mode - cost monitoring skipped")
        sys.exit(0)
    
    if command == "--check":
        log_message("INFO", "=== Railway Cost Monitor Check ===")
        
        usage_data = check_railway_usage()
        
        if usage_data.get("status") == "monitoring_disabled":
            sys.exit(0)
        
        max_percentage, percentages = calculate_usage_percentage(usage_data)
        
        if should_trigger_maintenance(max_percentage):
            log_message("ERROR", "🚨 FREE TIER LIMIT APPROACHING - MAINTENANCE MODE RECOMMENDED")
            trigger_maintenance_mode()
            sys.exit(2)  # Exit code 2 = maintenance required
        else:
            log_message("INFO", "✅ Usage within acceptable limits")
            sys.exit(0)
    
    elif command == "--trigger-maintenance":
        log_message("WARNING", "Manual maintenance mode trigger requested")
        trigger_maintenance_mode()
        sys.exit(0)
    
    else:
        log_message("ERROR", f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
