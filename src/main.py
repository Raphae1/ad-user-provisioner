import argparse
from provisioner import ADProvisioner

def main():
    parser = argparse.ArgumentParser(description="Automated Active Directory User Provisioner CLI")
    parser.add_argument("--csv", required=True, help="Path to input CSV file containing user records")
    parser.add_argument("--config", default="config/settings.json", help="Path to configuration JSON")
    parser.add_argument("--live", action="store_true", help="Execute live AD changes (disables dry-run simulation)")

    args = parser.parse_args()

    provisioner = ADProvisioner(args.config)
    dry_run_mode = not args.live
    provisioner.process_csv(args.csv, dry_run=dry_run_mode)

if __name__ == "__main__":
    main()
