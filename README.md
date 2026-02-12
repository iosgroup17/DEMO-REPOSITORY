for windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install --prefer-binary -r requirements.txt

for mac
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt

graph TD
    subgraph CLOUD [Cloud: Automated Supplier]
        A[Trend Ingestion] --> B[(Trend Table: DB)]
        B --> C[Edge Function: Filter]
        D[Remote AI] -->|Strategic Seed| C
    end

    subgraph DEVICE [Device: On-Device Consumer]
        E[Private User Data] --> F[Local AI Model]
        C -->|Filtered Seed| F
        F --> G[Draft Synthesis]
        G --> H{Minor Edit?}
        H -->|Yes| F
        H -->|No| I[Remote AI Refinement]
        I --> J[Post Approved]
        J --> K[Schedule & Publish]
    end
