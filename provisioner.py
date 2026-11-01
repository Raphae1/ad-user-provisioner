import argparse
import sys
import time

# Simulated database or directory store of existing users
EXISTING_DIRECTORY_USERS = {
    "jdoe": {"status": "ACTIVE", "department": "Engineering"},
    "asmith": {"status": "ACTIVE", "department": "HR"}
}

def process_lifecycle_batch(csv_path, dry_run=False):
    """
    Core lifecycle batch processing engine supporting ONBOARD, TRANSFER, and OFFBOARD.
    """
    print(f"\n[*] Loading lifecycle records from: {csv_path}")
    print(f"[*] Execution Mode: {'DRY-RUN (Simulation)' if dry_run else 'LIVE PROCESSING'}")
    
    start_time = time.time()
    
    # Extended simulated records representing mixed lifecycle requests
    simulated_records = [
        {"username": "jdoe", "action": "TRANSFER", "department": "Product Management", "email": "jdoe@company.local"},
        {"username": "bwayne", "action": "ONBOARD", "department": "Security", "email": "bwayne@company.local"},
        {"username": "asmith", "action": "OFFBOARD", "department": "HR", "email": "asmith@company.local"},
        {"username": "jdoe", "action": "ONBOARD", "department": "Engineering", "email": "jdoe@company.local"} # Test duplicate/idempotency
    ]
    
    total = len(simulated_records)
    success_count = 0
    skipped_count = 0
    failure_count = 0
    
    print("-" * 65)
    for index, record in enumerate(simulated_records, start=1):
        uname = record['username']
        action = record['action'].upper()
        target_dept = record['department']
        
        print(f"[{index}/{total}] User: {uname} | Action: {action} -> Dept: {target_dept}")
        
        # 1. Idempotency & Duplicate Prevention Checks
        user_exists = uname in EXISTING_DIRECTORY_USERS
        user_status = EXISTING_DIRECTORY_USERS.get(uname, {}).get("status")
        
        if action == "ONBOARD":
            if user_exists and user_status == "ACTIVE":
                print(f"    [SKIPPED] Idempotency Check: User '{uname}' already exists and is ACTIVE.")
                skipped_count += 1
                continue
        elif action in ["TRANSFER", "OFFBOARD"]:
            if not user_exists:
                print(f"    [X] Failure: Cannot {action.lower()} user '{uname}'—account not found in directory.")
                failure_count += 1
                continue
                
        # 2. Execution Simulation / Live Handling
        if dry_run:
            print(f"    [SIMULATION] Successfully simulated lifecycle action '{action}' for '{uname}'.")
        else:
            # Update internal mock state for live run
            if action == "ONBOARD":
                EXISTING_DIRECTORY_USERS[uname] = {"status": "ACTIVE", "department": target_dept}
            elif action == "TRANSFER":
                EXISTING_DIRECTORY_USERS[uname]["department"] = target_dept
            elif action == "OFFBOARD":
                EXISTING_DIRECTORY_USERS[uname]["status"] = "DISABLED"
            print(f"    [SUCCESS] Executed '{action}' for '{uname}'.")
            
        success_count += 1

    elapsed_time = time.time() - start_time
    
    # Enhanced Lifecycle Summary Report
    print("-" * 65)
    print("           LIFECYCLE BATCH EXECUTION SUMMARY REPORT           ")
    print("-" * 65)
    print(f" Total Records Processed : {total}")
    print(f" Successful Operations   : {success_count}")
    print(f" Skipped (Idempotent)    : {skipped_count}")
    print(f" Failures / Errors       : {failure_count}")
    print(f" Execution Time          : {elapsed_time:.2f} seconds")
    print("-" * 65)

def main():
    parser = argparse.ArgumentParser(
        description="Enterprise Active Directory Identity Lifecycle Manager"
    )
    parser.add_argument(
        "--csv", 
        default="lifecycle_requests.csv", 
        help="Path to the lifecycle input CSV file"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Simulate lifecycle actions without modifying system state"
    )
    
    args = parser.parse_args()
    
    try:
        process_lifecycle_batch(args.csv, dry_run=args.dry_run)
    except Exception as e:
        print(f"[ERROR] Critical lifecycle failure: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()