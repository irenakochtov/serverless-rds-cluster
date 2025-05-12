import json
import os
import boto3
import requests
import base64

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_OWNER = "irenakochtov"
REPO_NAME = "serverless-rds-cluster"
BASE_BRANCH = "main"

s3 = boto3.client("s3")

def lambda_handler(event, context):
    for record in event['Records']:
        message = json.loads(record['body'])
        db_name = message.get("db_name", "default-db")

        print(f"📥 Received message from SQS: {message}")

        # Step 1: Get SHA of the latest commit from main
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        ref_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/ref/heads/{BASE_BRANCH}"
        ref_resp = requests.get(ref_url, headers=headers)
        ref_data = ref_resp.json()
        print("🔍 GitHub ref response:", ref_data)

        if "object" not in ref_data:
            raise Exception("❌ GitHub ref fetch failed. Response: " + json.dumps(ref_data))

        main_sha = ref_data["object"]["sha"]

        # Step 2: Create new branch
        new_branch = f"rds-{db_name}"
        branch_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/refs"
        branch_data = {
            "ref": f"refs/heads/{new_branch}",
            "sha": main_sha
        }
        branch_resp = requests.post(branch_url, headers=headers, json=branch_data)
        print("🌿 Created new branch:", branch_resp.status_code, branch_resp.text)

        # Step 3: Create file content
        file_content = f'resource "aws_db_instance" "{db_name}" {{\n  identifier = "{db_name}"\n  engine = "mysql"\n  instance_class = "db.t3.micro"\n  username = "admin"\n  password = "SuperSecure123!"\n  allocated_storage = 20\n  skip_final_snapshot = true\n}}'

        blob_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/blobs"
        blob_data = {
            "content": file_content,
            "encoding": "utf-8"
        }
        blob_resp = requests.post(blob_url, headers=headers, json=blob_data)
        blob_json = blob_resp.json()
        print("🧱 GitHub blob response:", blob_json)

        if "sha" not in blob_json:
            raise Exception("❌ GitHub blob creation failed. Response: " + json.dumps(blob_json))

        blob_sha = blob_json["sha"]

        # Step 4: Create tree
        tree_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/trees"
        tree_data = {
            "base_tree": main_sha,
            "tree": [
                {
                    "path": f"terraform/{db_name}.tf",
                    "mode": "100644",
                    "type": "blob",
                    "sha": blob_sha
                }
            ]
        }
        tree_resp = requests.post(tree_url, headers=headers, json=tree_data)
        tree_json = tree_resp.json()
        print("🌳 GitHub tree response:", tree_json)

        if "sha" not in tree_json:
            raise Exception("❌ GitHub tree creation failed. Response: " + json.dumps(tree_json))

        tree_sha = tree_json["sha"]

        # Step 5: Create commit
        commit_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/commits"
        commit_data = {
            "message": f"Add RDS instance {db_name}",
            "tree": tree_sha,
            "parents": [main_sha]
        }
        commit_resp = requests.post(commit_url, headers=headers, json=commit_data)
        commit_json = commit_resp.json()
        print("💬 GitHub commit response:", commit_json)

        if "sha" not in commit_json:
            raise Exception("❌ GitHub commit failed. Response: " + json.dumps(commit_json))

        commit_sha = commit_json["sha"]

        # Step 6: Update branch reference
        update_ref_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/refs/heads/{new_branch}"
        update_ref_data = {
            "sha": commit_sha,
            "force": True
        }
        update_ref_resp = requests.patch(update_ref_url, headers=headers, json=update_ref_data)
        print("🔁 Updated branch reference:", update_ref_resp.status_code, update_ref_resp.text)

        # Step 7: Open PR
        pr_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls"
        pr_data = {
            "title": f"Add RDS instance {db_name}",
            "head": new_branch,
            "base": BASE_BRANCH,
            "body": f"This PR adds a new RDS instance named {db_name}."
        }
        pr_resp = requests.post(pr_url, headers=headers, json=pr_data)
        print("📬 PR creation response:", pr_resp.status_code, pr_resp.text)

    return {
        "statusCode": 200,
        "body": json.dumps("RDS request processed and PR created.")
    }