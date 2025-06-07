import os
import json
import requests
import sys

# --- Configuration ---
DOMAIN_NAME = "is-a.shop" # Your primary domain

# Cloudflare API details from GitHub Secrets
CLOUDFLARE_API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
CLOUDFLARE_ZONE_ID = os.getenv('CLOUDFLARE_ZONE_ID')

# --- Cloudflare API Function ---
def create_cloudflare_dns_record(subdomain_name, target_value, record_type="CNAME"):
    """
    Creates a DNS record in Cloudflare.
    subdomain_name: e.g., "myproject" (will become myproject.is-a.shop)
    target_value: e.g., "user.github.io" or "192.0.2.1"
    record_type: "CNAME" or "A"
    """
    if not CLOUDFLARE_API_TOKEN or not CLOUDFLARE_ZONE_ID:
        print("Error: Cloudflare API Token or Zone ID not found in environment variables.")
        return False

    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records"

    # Cloudflare API expects the full subdomain name for 'name' field
    full_dns_name = f"{subdomain_name}.{DOMAIN_NAME}"

    data = {
        "type": record_type.upper(), # Ensure type is uppercase
        "name": full_dns_name,
        "content": target_value,
        "ttl": 300, # 5 minutes, can be adjusted (1 = automatic)
        "proxied": True # Recommended for Cloudflare: enables CDN, SSL, etc.
    }

    print(f"Attempting to create DNS record: {full_dns_name} -> {target_value} (Type: {record_type})")
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print(f"Successfully created DNS record for {full_dns_name}")
        return True
    else:
        print(f"Failed to create DNS record for {full_dns_name}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        # Check for specific Cloudflare error codes
        try:
            error_details = response.json()
            if 'errors' in error_details:
                for error in error_details['errors']:
                    if error.get('code') == 81057: # Record already exists
                        print(f"Warning: DNS record for {full_dns_name} already exists. Skipping creation.")
                        return True # Consider it a success if it already exists
                    elif error.get('code') == 1004: # DNS validation error (e.g., invalid target)
                        print(f"Error: DNS record validation failed. Check 'target' value. Cloudflare error: {error.get('message')}")
                        return False
        except json.JSONDecodeError:
            pass # Not a JSON response, just print raw error

        return False

# --- Main Script Logic ---
if __name__ == "__main__":
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
        print(f"Error: Invalid JSON format in file {json_file_path}")
        sys.exit(1)

    subdomain = data.get("subdomain")
    target = data.get("target")
    record_type = data.get("record_type", "CNAME") # Default to CNAME if not specified

    # Basic Validation
    if not subdomain or not target:
        print("Error: 'subdomain' and 'target' fields are required in the JSON file.")
        sys.exit(1)

    if not isinstance(subdomain, str) or not subdomain.strip():
        print("Error: 'subdomain' must be a non-empty string.")
        sys.exit(1)

    # Basic alphanumeric check for subdomain for safety
    if not subdomain.replace('-', '').isalnum(): # Allow hyphens, then check alphanumeric
        print(f"Error: Subdomain '{subdomain}' contains invalid characters. Only alphanumeric and hyphens are allowed.")
        sys.exit(1)

    if not isinstance(target, str) or not target.strip():
        print("Error: 'target' must be a non-empty string.")
        sys.exit(1)

    # Convert to lowercase for consistency (DNS is case-insensitive, but good practice)
    subdomain = subdomain.lower()
    target = target.lower()

    # Call the Cloudflare API function
    success = create_cloudflare_dns_record(subdomain, target, record_type)

    if not success:
        sys.exit(1) # Indicate failure to GitHub Actions , Report if gives error.