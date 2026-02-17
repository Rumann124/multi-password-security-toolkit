import requests

def check_leakcheck_public(email):
    
    url = f"https://leakcheck.io/api/public?check={email}"
    
    try:
        print(f"[*] Checking {email}...")
        response = requests.get(url)
        data = response.json()
        
        # Check if the API request was successful
        if data.get('success'):
            if data.get('found'):
                print(f"[!] DANGER: {email} is LEAKED.")
                
                # GET THE SOURCES SAFELY
                sources = data.get('sources', [])
                
                if not sources:
                    print("    (Source names hidden in free public tier)")
                else:
                    print("    Sources found:")
                    # Loop through them instead of joining
                    for s in sources:
                        # If it's a simple string, just print it
                        if isinstance(s, str):
                            print(f"    - {s}")
                        # If it's a dictionary (object), print it nicely
                        elif isinstance(s, dict):
                            # Try to find a 'name' or just print the whole thing
                            name = s.get('name') or s.get('source') or str(s)
                            print(f"    - {name}")
                        else:
                            print(f"    - {s}")
            else:
                print(f"[:] Safe. {email} was not found in the public database.")
        else:
            # Print the specific error from the API
            print(f"[-] API Error: {data.get('error')}")
            
    except Exception as e:
        print(f"[-] Script crashed: {e}")

# Run it
check_leakcheck_public("test@example.com")