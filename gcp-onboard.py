# This script logs into GCP and iterates through subscriptions to onboard them into Dome9
# Feedback to chrisbe@checkpoint.com or open an issue on https://github.com/chrisbeckett/gcpd9-autoonboarding/issues

# To run the script, you will need to set environment variable for GOOGLE_APPLICATION_CREDENTIALS to the file path of the Service Account JSON file

# You will also need to set environment variables for D9_API_KEY and D9_API_SECRET

# Import required libraries
from google.cloud import resource_manager
import os
import requests
from requests.auth import HTTPBasicAuth
import json
import sys
from colorama import Fore,init
init()


gcp_client = resource_manager.Client()

# Verify the environment variables have been set

def verify_env_variables():
    try:
        if 'D9_API_KEY' in os.environ:
            pass
        else:
            print(Fore.RED + "ERROR : The Dome9 API key has not been defined in environment variables")
            sys.exit(0)
        if 'D9_API_SECRET' in os.environ:
            pass
        else:
            print(Fore.RED + "ERROR : The Dome9 API key secret not been defined in environment variables")
            sys.exit(0)
        if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
            pass
        else:
            print(Fore.RED + "ERROR : The Google Cloud Application Credentials file location has not been defined in environment variables")
            sys.exit(0)
    except:
        print(Fore.RED + "An unknown error occured")
        sys.exit(0)


verify_env_variables()

# Read in required environment variables
d9_api_key = os.environ['D9_API_KEY']
d9_api_secret = os.environ['D9_API_SECRET']
d9_api = os.environ.get('D9_API', 'https://api.dome9.com')
gcp_creds = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

# Open and read the credential JSON file
f = open(gcp_creds)
creds_json_file = json.load(f)

# Set header parameters for Dome9 HTTP POST
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def add_projects():
    try:
        added_accounts = 0
        print(Fore.WHITE + "===================================================================================================================")
        print(Fore.YELLOW + "                                             Dome9 GCP Onboarding Tool")
        print(Fore.WHITE + "===================================================================================================================","\n")
        for project in gcp_client.list_projects():
            #print("Creds JSON info :","\n",creds_json_file,"\n")
            creds_json_file.update({'project_id': project.project_id})
            newval = creds_json_file.get("project_id")
            print(Fore.WHITE + "===================================================================================================================")
            print(Fore.WHITE + "Project ID updated to: ",newval)
            print(Fore.YELLOW + "Project found:", Fore.WHITE + project.name, Fore.YELLOW + "Project ID: ",Fore.GREEN + project.project_id)
            payload = {'name': project.name,'serviceAccountCredentials': creds_json_file}
            r = requests.post(d9_api + '/v2/GoogleCloudAccount',json=payload, headers=headers, auth=(d9_api_key, d9_api_secret))
            if r.status_code == 201:
                print(Fore.GREEN + 'Project successfully added to Dome9:', project.name)
                print(Fore.WHITE + "===================================================================================================================","\n")
                added_accounts = added_accounts + 1
            elif r.status_code == 400:
                print(Fore.RED + 'There was an error with the project, please check credentials and that it does not already exist in Dome9')
                print("Error message:")
                print(r.text,"\n")
            elif r.status_code == 401:
                print(Fore.RED + 'Bad credentials onboarding project to Dome9:',project.name,"\n")
            elif r.status_code == 409:
                print(Fore.GREEN + 'Project already exists in Dome9:', project.name)
                print(Fore.WHITE + "===================================================================================================================","\n")
            elif r.status_code == 500:
                print(Fore.RED + 'Error onboarding project to Dome9, check dependent APIs are enabled in GCP:',project.name,"\n")
            else:
                print(Fore.RED + 'Unknown error onboarding subscription to Dome9:',project.name,'Status Code:', r.status_code)
                print(r.content,"\n")
    except:
        print(Fore.RED + "Unknown error, soz!")
    print("\n")
    print(Fore.WHITE + "===================================================================================================================")
    print(Fore.WHITE + "                                           RUN COMPLETE - SUMMARY RESULTS")
    print(Fore.WHITE + "===================================================================================================================","\n")
    print(Fore.CYAN + "Number of GCP projects successfully added to Dome9: ", added_accounts)
    print(Fore.WHITE + "===================================================================================================================","\n")

add_projects()
