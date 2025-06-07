import os
import json
import requests
import sys

# --- Configuration ---
DNS_PROVIDER = os.getenv('DNS_PROVIDER', 'cloudflare') # 'cloudflare', 'godaddy', etc.
DOMAIN_NAME = "is-a.shop" # Your primary domain
# For Cloudflare:
CLOUDFLARE_API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
CLOUDFLARE_ZONE_ID = os.getenv('CLOUDFLARE_ZONE_ID') # Get this from your Cloudflare dashboard for is-a.shop

# --- Helper Functions ---
def create_cloudflare_dns_record(subdomain, target, record_type="CNAME"):
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records"

    data = {
        "type": record_type,
        "name": f"{subdomain}.{DOMAIN_NAME}", # Cloudflare API expects full FQDN for 'name'
        "content": target,
        "ttl": 300, # 5 minutes, can be adjusted
        "proxied": True # Recommended for Cloudflare: enables CDN, SSL, etc.
    }

    print(f"Attempting to create DNS record: {subdomain}.{DOMAIN_NAME} -> {target} ({record_type})")
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print(f"Successfully created DNS record for {subdomain}.{DOMAIN_NAME}")
        return True
    else:
        print(f"Failed to create DNS record for {subdomain}.{DOMAIN_NAME}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

# You would add similar functions for other DNS providers here if needed.
# e.g., create_godaddy_dns_record(...)

# --- Main Logic ---
if __name__ == "__main__":
    # This script expects the path to the merged JSON file as an argument
    if len(sys.argv) < 2:
        print("Usage: python add_dns_record.py <path_to_merged_json>")
        sys.exit(1)

    json_file_path = sys.argv[1]

    if not os.path.exists(json_file_path):
        print(f"Error: JSON file not found at {json_file_path}")
        sys.exit(1)

    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file {json_file_path}")
        sys.exit(1)

    subdomain = data.get("subdomain")
    target = data.get("target")
    record_type = data.get("record_type", "CNAME") # Allow users to specify A or CNAME

    if not subdomain or not target:
        print("Error: 'subdomain' and 'target' fields are required in the JSON file.")
        sys.exit(1)

    # Basic validation (you can add more robust checks)
    if not isinstance(subdomain, str) or not subdomain.isalnum(): # Simple check for alphanumeric
        print("Error: Subdomain must be alphanumeric.")
        sys.exit(1)
    if not isinstance(target, str) or not target:
        print("Error: Target must be a valid string.")
        sys.exit(1)

    # Call the appropriate DNS creation function
    if DNS_PROVIDER == 'cloudflare':
        success = create_cloudflare_dns_record(subdomain, target, record_type)
    # Add elif for other providers here
    else:
        print(f"Error: Unsupported DNS provider '{DNS_PROVIDER}'.")
        sys.exit(1)

    if not success:
        sys.exit(1) # Indicate failure to GitHub Actions