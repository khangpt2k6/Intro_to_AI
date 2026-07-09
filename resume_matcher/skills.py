"""Skill taxonomy: canonical skill names mapped to their surface-form aliases.

This plays the role of the O*NET-style controlled vocabulary from the proposal:
differently worded mentions ("JS", "Javascript") normalize to one canonical
skill so resume vectors and job vectors are comparable. The list focuses on
the job families we demo (IT, data, finance) and is easy to extend.
"""

# canonical skill -> list of aliases (matched case-insensitively, word-bounded)
SKILL_ALIASES = {
    # programming languages
    "Python": ["python"],
    "Java": ["java"],
    "JavaScript": ["javascript", "js", "ecmascript"],
    "TypeScript": ["typescript"],
    "C++": ["c++", "cpp"],
    "C#": ["c#", "c sharp"],
    "R": ["r programming", "r language"],
    "SQL": ["sql", "mysql", "postgresql", "postgres", "sql server", "t-sql", "pl/sql"],
    "HTML/CSS": ["html", "css", "html5", "css3"],
    "PHP": ["php"],
    "Go": ["golang"],

    # frameworks and tools
    "React": ["react", "react.js", "reactjs"],
    "Node.js": ["node.js", "nodejs", "node js"],
    "Django": ["django"],
    "Flask": ["flask"],
    ".NET": [".net", "dotnet", "asp.net"],
    "Spring": ["spring boot", "spring framework"],

    # data / ML
    "Machine Learning": ["machine learning", "ml models", "scikit-learn", "sklearn"],
    "Deep Learning": ["deep learning", "neural network", "neural networks", "tensorflow", "pytorch", "keras"],
    "NLP": ["nlp", "natural language processing", "text mining"],
    "Data Analysis": ["data analysis", "data analytics", "data analyst"],
    "Statistics": ["statistics", "statistical analysis", "statistical modeling", "hypothesis testing"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Tableau": ["tableau"],
    "Power BI": ["power bi", "powerbi"],
    "Excel": ["excel", "microsoft excel", "ms excel", "pivot tables", "vlookup"],
    "Data Visualization": ["data visualization", "matplotlib", "seaborn", "d3.js"],
    "Big Data": ["hadoop", "spark", "big data", "hive"],
    "ETL": ["etl", "data pipeline", "data pipelines", "data warehousing"],

    # infrastructure
    "AWS": ["aws", "amazon web services", "ec2", "s3 bucket", "lambda"],
    "Azure": ["azure"],
    "GCP": ["gcp", "google cloud"],
    "Docker": ["docker", "containerization", "containers"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Git": ["git", "github", "gitlab", "version control"],
    "CI/CD": ["ci/cd", "continuous integration", "continuous deployment", "jenkins"],
    "Linux": ["linux", "unix", "bash", "shell scripting"],
    "REST APIs": ["rest api", "rest apis", "restful", "web services", "api development"],
    "Networking": ["tcp/ip", "networking", "dns", "vpn", "firewall", "cisco"],
    "Security": ["cybersecurity", "information security", "penetration testing", "vulnerability"],
    "Databases": ["database administration", "database design", "oracle", "mongodb", "nosql"],

    # process / soft
    "Agile": ["agile", "scrum", "kanban", "sprint planning"],
    "Project Management": ["project management", "pmp", "project manager", "jira"],
    "Communication": ["communication skills", "presentation skills", "public speaking"],
    "Leadership": ["leadership", "team lead", "mentoring", "supervising"],
    "Problem Solving": ["problem solving", "troubleshooting", "root cause analysis"],
    "Customer Service": ["customer service", "customer support", "client relations"],

    # finance / accounting (for the cross-domain demo)
    "Accounting": ["accounting", "general ledger", "accounts payable", "accounts receivable", "bookkeeping"],
    "Financial Reporting": ["financial reporting", "financial statements", "financial analysis"],
    "QuickBooks": ["quickbooks"],
    "SAP": ["sap"],
    "Auditing": ["auditing", "internal audit", "audit"],
    "Payroll": ["payroll"],
    "Budgeting": ["budgeting", "budget planning", "forecasting"],
    "Tax": ["tax preparation", "tax returns", "taxation"],
    "CPA": ["cpa", "certified public accountant"],
    "GAAP": ["gaap"],
}
