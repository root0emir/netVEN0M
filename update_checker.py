import requests
import json
import pkg_resources

def check_for_updates():
    current_version = pkg_resources.get_distribution("netVEN0M").version
    response = requests.get("https://api.github.com/repos/root0emir/netVEN0M/releases/latest")
    
    if response.status_code == 200:
        latest_version = response.json()["tag_name"]
        if current_version < latest_version:
            print(f"A new version is available: {latest_version}. Don't forget to update")
        else:
            print("You are on the latest version.")
    else:
        print("An error occurred while checking for updates.")

if __name__ == "__main__":
    check_for_updates()
