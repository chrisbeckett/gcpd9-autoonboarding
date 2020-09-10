What does this script do?
-------------------------

It logs into an GCP organisation, obtains a list of all projects attached to it and then adds them one by one to Dome9 if they don't already exist. It can be used as an Google Function to run daily to sweep up any new projects not already onboarded so cloud estate visibility is maintained.

Standalone Windows executable
-----------------------------

If you need to run the tool as a one off and don't want the faff of all the steps below, you can download the ZIP archive. This is a portable version of the tool for Windows only, all batteries included. Download and extract the ZIP and run **gcp-onboard.exe**. For a Linux or Mac version of this, please open an issue and I will address this. **Remember to set environment variables prior to running the tool (see below)**.

Pre-requisites
--------------
To run this script, you will need the following:-

1) **Python 3.6** (or newer)

2) A **GCP Service Account**
    - Create a dedicated security project to manage the Service Account (optional but recommended)
    - Go to **IAM**, **Service Accounts** and **Create Service Account**
    - Create the Service Account with a meaningful name *(D9-onboard or similar)*
    - Note the **e-mail address** of the Service Account, **you will need this later**
    - Click **Create**
    - Click **Continue** (no need to assign a role yet)
    - Click **Create Key** and save as **JSON** format, the key file will automatically download. Click **Done**
    - Click the **Organisation** object from the top drop down box in the GCP Console
    - Click **IAM** and click **Add**
    - In the **New Members** box, copy the e-mail address of the Service Account you created earlier *(e.g. myserviceaccount@security-project-9999.iam.gserviceaccount.com)*, pick the user when they are looked up
    - Add the Service Account to the **Project Viewer** role and click **Save**
    
3) Dome9 API key with admin permissions to add subscriptions (*https://supportcenter.checkpoint.com/supportcenter/portal?eventSubmit_doGoviewsolutiondetails=&solutionid=sk144514&partition=General&product=CloudGuard*)
    - Dome9 **API key**
    - Dome9 **API secret**
    
4) Run **git clone https://github.com/chrisbeckett/gcpd9-autoonboarding.git**

5) Run **python -m venv gcpd9-autoonboarding**

6) Run **scripts\activate.bat** to enable the Python virtual environment

7) Run **pip install -r requirements.txt** to install required Python modules
    
Setup
-----
To run the script locally, you need to set several environment variables which are then read in by the script. This prevents any secret keys being hard coded into the script. Set the following:-

- SET D9_API_KEY=xxxxxxxxxxx
- SET D9_API_SECRET=xxxxxxxxxxxx
- SET GOOGLE_APPLICATION_CREDENTIALS=C:\Users\AUser\Downloads\mykey.json *(for example)*

Running the script
------------------
Simply run the script **gcp-onboard.py** from the command line 
