# Repo structure
```directory
kickball-scheduler/
├── .github/
│   └── workflows/
│       ├── deploy-generator.yml  # Deploy on changes to generator_lambda/
│       ├── deploy-history.yml    # Deploy on changes to history_lambda/
│       └── deploy-angular.yml    # Deploy on changes to angular-app/
├── angular-app/                  # The UI (S3/CloudFront)
│   ├── src/
│   └── angular.json
├── backend/
│   ├── generator_lambda/         # The "Scheduler" Function
│   │   ├── lambda_function.py    # Entry point for /generate
│   │   ├── algorithms/           # weighted_random.py, etc.
│   │   ├──shared/                # validation.py & balance_report.py
|   |   └── tests/                # python unit tests
│   ├── history_lambda/           # The "Archive" Function
│   │   ├── lambda_function.py    # Entry point for /history
|   |   └── tests/                # python unit tests
├── requirements.txt              # Backend dependencies (Pandas, Boto3, etc.)
└── README.md
```

# Phase 1: Modular Python Backend (The Engine)

Instead of one large script, you will break your code into modular files. This allows you to swap algorithms while keeping validation the same.

# Phase 2: AWS Serverless Infrastructure

You will move from local execution to the cloud using these specific services:

- AWS Lambda: Runs your Python code. You'll create a "Generator" function for scheduling and a "History" function for S3 access.

- Amazon API Gateway: Acts as the bridge. It provides a URL (e.g., https://api.yoursite.com/generate) that your Angular app can call.

- Amazon S3:

    - Bucket A: Hosts your Angular static files (HTML/JS/CSS).

    - Bucket B: Stores generated schedules as .json files for the "History" feature.

    ```json
    {
        "metadata": {
            "generated_at": "2026-01-24T12:00:00Z",
            "algorithm_used": "weighted_random_v1",
            "parity_score": 2.45,
            "quality_status": "EXCELLENT"
        },
        "teams": [...],
        "schedule": {
            "Week 1": [...],
            "Week 2": [...]
        }
    }
    ```

- Amazon CloudFront: A Content Delivery Network (CDN) that sits in front of S3 to provide HTTPS and faster loading.

# Phase 3: Angular Frontend (The Interactive UI)

Instead of a CSV, users interact with a dynamic form.

- Team Input: A dynamic list where users can add/remove rows for "Team Name" and "Rank."

- Algorithm Selector: A dropdown menu to choose between "Weighted Random" or other styles.

- API Service: An Angular service using HttpClient to POST the form data to API Gateway.

- History Dashboard: A component that calls the "History" Lambda to list previous schedules stored in S3.

# Phase 4: CI/CD Pipeline (GitHub Actions)

This automates your work so that every time you git push, your site updates.

- Frontend Workflow (.github/workflows/frontend.yml):

    - Triggers on changes to the angular-app/ folder.

    - Runs npm install and ng build --prod.

    - Uses aws s3 sync to upload the dist/ folder to your S3 bucket.

    - Invalidates CloudFront cache so users see the new version immediately.

- Backend Workflow (.github/workflows/backend.yml):

    - Triggers on changes to the python-api/ folder.

    - Runs pytest to ensure your algorithms still work.

    - Zips the Python files and uses aws lambda update-function-code to deploy.
    - https://www.youtube.com/watch?v=H4xbYKPjvbs
    - https://www.youtube.com/watch?v=H4xbYKPjvbs