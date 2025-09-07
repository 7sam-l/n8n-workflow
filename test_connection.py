# test_connection.py
import requests

def check_connectivity():
    """
    A simple script to check for basic internet connectivity from Python.
    """
    print("--- Starting Connection Test ---")
    
    test_urls = {
        "Google": "https://www.google.com",
        "YouTube": "https://www.youtube.com",
        "n8n Forum": "https://community.n8n.io"
    }
    
    all_successful = True
    
    for name, url in test_urls.items():
        try:
            # We add a timeout to prevent it from hanging indefinitely
            print(f"Attempting to connect to {name} at {url}...")
            response = requests.get(url, timeout=10)
            
            # A status code of 200 means "OK"
            if response.status_code == 200:
                print(f"SUCCESS: Successfully connected to {name}.")
            else:
                print(f"FAILURE: Connected to {name}, but got a bad status code: {response.status_code}")
                all_successful = False
        except requests.exceptions.RequestException as e:
            print(f"FAILURE: Could not connect to {name}.")
            print(f"   Error: {e}")
            all_successful = False
        print("-" * 20)
        
    if all_successful:
        print("\nTest Result: All connections were successful. Network seems OK.")
    else:
        print("\nTest Result: One or more connections failed. There is likely a network, firewall, or proxy issue.")

if __name__ == "__main__":
    check_connectivity()
