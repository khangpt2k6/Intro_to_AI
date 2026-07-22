"""Skill taxonomy: canonical skill names mapped to their surface-form aliases.

This plays the role of the O*NET-style controlled vocabulary from the proposal:
differently worded mentions ("JS", "Javascript") normalize to one canonical
skill so resume vectors and job vectors are comparable.

The taxonomy covers all 24 job categories in the Kaggle resume dataset
(ACCOUNTANT, ADVOCATE, AGRICULTURE, APPAREL, ARTS, AUTOMOBILE, AVIATION,
BANKING, BPO, BUSINESS-DEVELOPMENT, CHEF, CONSTRUCTION, CONSULTANT, DESIGNER,
DIGITAL-MEDIA, ENGINEERING, FINANCE, FITNESS, HEALTHCARE, HR,
INFORMATION-TECHNOLOGY, PUBLIC-RELATIONS, SALES, TEACHER), grouped by domain.

Rules of the road (enforced by tests/test_skills.py):
  - aliases are lowercase and matched case-insensitively, word-bounded
  - no alias may map to two different canonical skills
Prefer multi-word aliases over bare generic words ("graphic design", not
"design"; "fine arts", not "art") so extraction does not over-match.
"""

# canonical skill -> list of aliases (matched case-insensitively, word-bounded)
SKILL_ALIASES = {
    # ------------------------------------------------------------------ #
    # programming languages
    # ------------------------------------------------------------------ #
    "Python": ["python"],
    "Java": ["java"],
    "JavaScript": ["javascript", "js", "ecmascript"],
    "TypeScript": ["typescript"],
    "C++": ["c++", "cpp"],
    "C#": ["c#", "c sharp"],
    "R": ["r programming", "r language"],
    "Ruby": ["ruby"],
    "Swift": ["swift"],
    "Kotlin": ["kotlin"],
    "Scala": ["scala"],
    "Perl": ["perl"],
    "MATLAB": ["matlab"],
    "SAS": ["sas programming", "sas analytics"],
    "SPSS": ["spss"],
    "VBA": ["vba", "visual basic"],
    "SQL": ["sql", "mysql", "postgresql", "postgres", "sql server", "t-sql", "pl/sql"],
    "HTML/CSS": ["html", "css", "html5", "css3"],
    "PHP": ["php"],
    "Go": ["golang"],

    # ------------------------------------------------------------------ #
    # web / app frameworks and tools
    # ------------------------------------------------------------------ #
    "React": ["react", "react.js", "reactjs"],
    "Angular": ["angular", "angularjs"],
    "Vue.js": ["vue", "vue.js", "vuejs"],
    "Node.js": ["node.js", "nodejs", "node js"],
    "Django": ["django"],
    "Flask": ["flask"],
    ".NET": [".net", "dotnet", "asp.net"],
    "Spring": ["spring boot", "spring framework"],
    "Ruby on Rails": ["ruby on rails", "rails framework"],
    "jQuery": ["jquery"],
    "Bootstrap": ["bootstrap"],
    "WordPress": ["wordpress"],

    # ------------------------------------------------------------------ #
    # data / analytics / ML
    # ------------------------------------------------------------------ #
    "Machine Learning": ["machine learning", "ml models", "scikit-learn", "sklearn"],
    "Deep Learning": ["deep learning", "neural network", "neural networks", "tensorflow", "pytorch", "keras"],
    "NLP": ["nlp", "natural language processing", "text mining"],
    "Computer Vision": ["computer vision", "image processing", "opencv"],
    "Data Analysis": ["data analysis", "data analytics", "data analyst"],
    "Data Science": ["data science", "data scientist"],
    "Statistics": ["statistics", "statistical analysis", "statistical modeling", "hypothesis testing"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Tableau": ["tableau"],
    "Power BI": ["power bi", "powerbi"],
    "Excel": ["excel", "microsoft excel", "ms excel", "pivot tables", "vlookup"],
    "Data Visualization": ["data visualization", "matplotlib", "seaborn", "d3.js"],
    "Big Data": ["hadoop", "spark", "big data", "hive"],
    "ETL": ["etl", "data pipeline", "data pipelines", "data warehousing"],
    "Data Modeling": ["data modeling", "dimensional modeling", "star schema"],

    # ------------------------------------------------------------------ #
    # cloud / infrastructure / devops
    # ------------------------------------------------------------------ #
    "AWS": ["aws", "amazon web services", "ec2", "s3 bucket", "lambda"],
    "Azure": ["azure"],
    "GCP": ["gcp", "google cloud"],
    "Docker": ["docker", "containerization", "containers"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Terraform": ["terraform", "infrastructure as code"],
    "Ansible": ["ansible"],
    "Git": ["git", "github", "gitlab", "version control"],
    "CI/CD": ["ci/cd", "continuous integration", "continuous deployment", "jenkins"],
    "Linux": ["linux", "unix", "bash", "shell scripting"],
    "REST APIs": ["rest api", "rest apis", "restful", "web services", "api development"],
    "Microservices": ["microservices", "service oriented architecture"],
    "Networking": ["tcp/ip", "networking", "dns", "vpn", "firewall", "cisco"],
    "Security": ["cybersecurity", "information security", "penetration testing", "vulnerability"],
    "Databases": ["database administration", "database design", "oracle", "mongodb", "nosql"],

    # ------------------------------------------------------------------ #
    # IT support
    # ------------------------------------------------------------------ #
    "Technical Support": ["technical support", "help desk", "helpdesk", "desktop support"],
    "System Administration": ["system administration", "system administrator", "windows server", "active directory"],
    "Virtualization": ["vmware", "virtualization", "hyper-v"],

    # ------------------------------------------------------------------ #
    # process / project / soft skills
    # ------------------------------------------------------------------ #
    "Agile": ["agile", "scrum", "kanban", "sprint planning"],
    "Project Management": ["project management", "pmp", "project manager", "jira"],
    "Communication": ["communication skills", "presentation skills", "public speaking"],
    "Leadership": ["leadership", "team lead", "mentoring", "supervising"],
    "Problem Solving": ["problem solving", "troubleshooting", "root cause analysis"],
    "Time Management": ["time management", "prioritization", "multitasking"],
    "Teamwork": ["teamwork", "collaboration", "team player", "cross-functional"],
    "Negotiation": ["negotiation", "negotiating", "conflict resolution"],
    "Strategic Planning": ["strategic planning", "strategic planner"],
    "Process Improvement": ["process improvement", "continuous improvement", "operational excellence"],
    "Six Sigma": ["six sigma", "lean six sigma", "dmaic"],
    "Lean": ["lean manufacturing", "lean methodology", "kaizen"],
    "Change Management": ["change management"],
    "Business Analysis": ["business analysis", "business analyst", "requirements gathering"],

    # ------------------------------------------------------------------ #
    # finance / accounting / banking
    # ------------------------------------------------------------------ #
    "Accounting": ["accounting", "general ledger", "accounts payable", "accounts receivable", "bookkeeping"],
    "Financial Reporting": ["financial reporting", "financial statements", "financial analysis"],
    "Financial Modeling": ["financial modeling", "financial modelling", "valuation", "dcf"],
    "QuickBooks": ["quickbooks"],
    "SAP": ["sap"],
    "Auditing": ["auditing", "internal audit", "audit"],
    "Payroll": ["payroll"],
    "Budgeting": ["budgeting", "budget planning", "forecasting"],
    "Tax": ["tax preparation", "tax returns", "taxation"],
    "CPA": ["cpa", "certified public accountant"],
    "GAAP": ["gaap"],
    "Cost Accounting": ["cost accounting", "cost analysis"],
    "Accounts Reconciliation": ["reconciliation", "account reconciliation", "bank reconciliation"],
    "Risk Management": ["risk management", "risk assessment", "risk analysis"],
    "Banking": ["retail banking", "commercial banking", "teller", "banking operations"],
    "Credit Analysis": ["credit analysis", "credit risk", "underwriting"],
    "Loan Processing": ["loan processing", "loan origination", "mortgage", "loan officer"],
    "Investment": ["investment management", "portfolio management", "wealth management", "asset management"],
    "Compliance": ["compliance", "regulatory compliance", "kyc", "anti-money laundering", "aml"],

    # ------------------------------------------------------------------ #
    # human resources
    # ------------------------------------------------------------------ #
    "Recruiting": ["recruiting", "recruitment", "talent acquisition", "sourcing candidates"],
    "Employee Relations": ["employee relations", "labor relations", "employee engagement"],
    "Performance Management": ["performance management", "performance reviews", "performance appraisal"],
    "Onboarding": ["onboarding", "new hire orientation"],
    "HRIS": ["hris", "workday", "peoplesoft", "hr information system"],
    "Benefits Administration": ["benefits administration", "compensation and benefits", "employee benefits"],
    "Training and Development": ["training and development", "learning and development", "employee training"],

    # ------------------------------------------------------------------ #
    # healthcare
    # ------------------------------------------------------------------ #
    "Patient Care": ["patient care", "patient assessment", "direct patient care"],
    "Nursing": ["nursing", "registered nurse", "rn", "lpn"],
    "Medical Coding": ["medical coding", "icd-10", "cpt coding", "medical billing"],
    "Electronic Health Records": ["electronic health records", "electronic medical records", "emr", "ehr", "epic systems"],
    "HIPAA": ["hipaa"],
    "Clinical Research": ["clinical research", "clinical trials", "clinical documentation"],
    "Medical Terminology": ["medical terminology"],
    "CPR": ["cpr", "bls", "basic life support", "acls", "first aid"],
    "Phlebotomy": ["phlebotomy", "venipuncture"],
    "Pharmacology": ["pharmacology", "medication administration"],

    # ------------------------------------------------------------------ #
    # education / teaching
    # ------------------------------------------------------------------ #
    "Teaching": ["teaching", "classroom instruction", "teacher"],
    "Curriculum Development": ["curriculum development", "curriculum design", "curriculum"],
    "Lesson Planning": ["lesson planning", "lesson plans"],
    "Classroom Management": ["classroom management"],
    "Student Assessment": ["student assessment", "grading", "student evaluation"],
    "Special Education": ["special education", "iep", "special needs"],
    "Tutoring": ["tutoring", "tutor"],
    "E-Learning": ["e-learning", "online learning", "distance learning", "instructional design"],
    "Early Childhood Education": ["early childhood education", "early childhood"],

    # ------------------------------------------------------------------ #
    # culinary / chef
    # ------------------------------------------------------------------ #
    "Culinary Arts": ["culinary arts", "culinary", "cooking", "food preparation"],
    "Menu Development": ["menu development", "menu planning", "recipe development"],
    "Food Safety": ["food safety", "sanitation", "servsafe", "haccp"],
    "Catering": ["catering", "banquet", "event catering"],
    "Baking": ["baking", "pastry", "pastry arts"],
    "Kitchen Management": ["kitchen management", "kitchen operations", "back of house"],
    "Inventory Management": ["inventory management", "inventory control", "stock management"],

    # ------------------------------------------------------------------ #
    # design / creative tools
    # ------------------------------------------------------------------ #
    "Graphic Design": ["graphic design", "graphic designer", "visual design"],
    "Interior Design": ["interior design", "interior designer", "space planning"],
    "Web Design": ["web design", "responsive design"],
    "UI/UX Design": ["ui/ux", "user experience", "ux design", "ui design", "wireframing", "prototyping"],
    "Adobe Photoshop": ["photoshop"],
    "Adobe Illustrator": ["illustrator", "adobe illustrator"],
    "Adobe InDesign": ["indesign"],
    "Adobe Creative Suite": ["adobe creative suite", "creative cloud", "adobe creative cloud"],
    "Figma": ["figma"],
    "Sketch": ["sketch app"],
    "CAD": ["cad", "autocad", "computer-aided design", "computer aided design"],
    "SolidWorks": ["solidworks"],
    "Typography": ["typography"],
    "Branding": ["branding", "brand identity", "logo design"],
    "3D Modeling": ["3d modeling", "3d rendering", "3d animation"],

    # ------------------------------------------------------------------ #
    # arts
    # ------------------------------------------------------------------ #
    "Fine Arts": ["fine arts", "fine art", "visual arts", "studio art"],
    "Photography": ["photography", "photographer"],
    "Painting": ["painting", "acrylic painting", "oil painting"],
    "Drawing": ["drawing", "illustration", "sketching"],
    "Performing Arts": ["performing arts", "theater", "theatre"],
    "Music": ["music production", "musician", "music composition"],
    "Creative Writing": ["creative writing", "storytelling"],
    "Art History": ["art history"],

    # ------------------------------------------------------------------ #
    # digital media / video
    # ------------------------------------------------------------------ #
    "Video Editing": ["video editing", "video production", "adobe premiere", "premiere pro"],
    "Motion Graphics": ["motion graphics", "after effects", "motion design"],
    "Animation": ["animation", "2d animation", "character animation"],
    "Content Production": ["content production", "content creation", "digital content"],

    # ------------------------------------------------------------------ #
    # fitness / wellness
    # ------------------------------------------------------------------ #
    "Personal Training": ["personal training", "personal trainer", "fitness training"],
    "Group Fitness": ["group fitness", "group exercise", "fitness instructor", "aerobics"],
    "Nutrition": ["nutrition", "dietary planning", "meal planning", "dietitian"],
    "Strength Training": ["strength training", "strength and conditioning", "weight training"],
    "Yoga": ["yoga", "pilates"],
    "Wellness": ["wellness", "wellness coaching", "health coaching"],

    # ------------------------------------------------------------------ #
    # sales / retail / marketing
    # ------------------------------------------------------------------ #
    "Sales": ["sales", "b2b sales", "b2c sales", "inside sales", "outside sales"],
    "Retail": ["retail", "retail sales", "store operations", "cashiering", "point of sale"],
    "Merchandising": ["merchandising", "visual merchandising", "merchandiser"],
    "Marketing": ["marketing", "marketing strategy", "marketing campaigns"],
    "Digital Marketing": ["digital marketing", "online marketing"],
    "SEO": ["seo", "search engine optimization", "sem"],
    "Social Media": ["social media", "social media marketing", "social media management"],
    "Content Marketing": ["content marketing", "email marketing", "content strategy"],
    "CRM": ["crm", "salesforce", "customer relationship management"],
    "Lead Generation": ["lead generation", "prospecting", "cold calling"],
    "Account Management": ["account management", "account manager", "key account"],
    "Business Development": ["business development", "partnerships", "b2b development"],
    "Market Research": ["market research", "market analysis", "competitive analysis"],
    "Google Analytics": ["google analytics", "web analytics"],
    "Advertising": ["advertising", "paid media", "google ads", "ppc"],
    "E-commerce": ["e-commerce", "ecommerce", "online store"],
    "Customer Service": ["customer service", "customer support", "client relations"],

    # ------------------------------------------------------------------ #
    # public relations / communications
    # ------------------------------------------------------------------ #
    "Public Relations": ["public relations", "pr strategy", "media relations"],
    "Press Releases": ["press release", "press releases"],
    "Corporate Communications": ["corporate communications", "internal communications"],
    "Copywriting": ["copywriting", "copywriter"],
    "Journalism": ["journalism", "journalist", "news writing", "news reporting", "editorial", "reporter"],
    "Event Planning": ["event planning", "event management", "event coordination"],
    "Crisis Communication": ["crisis communication", "crisis management", "reputation management"],

    # ------------------------------------------------------------------ #
    # apparel / fashion
    # ------------------------------------------------------------------ #
    "Fashion Design": ["fashion design", "apparel design", "fashion designer"],
    "Textiles": ["textiles", "fabric selection", "textile design"],
    "Pattern Making": ["pattern making", "garment construction", "sewing"],
    "Trend Analysis": ["trend analysis", "trend forecasting", "fashion trends"],
    "Product Development": ["product development", "product design", "sourcing"],
    "Quality Control": ["quality control", "quality assurance", "qa/qc"],

    # ------------------------------------------------------------------ #
    # legal / advocate
    # ------------------------------------------------------------------ #
    "Legal Research": ["legal research", "case law research"],
    "Litigation": ["litigation", "trial preparation", "civil litigation"],
    "Contract Law": ["contract law", "contract drafting", "contract negotiation"],
    "Legal Writing": ["legal writing", "legal documentation", "briefs"],
    "Case Management": ["case management", "caseload management"],
    "Paralegal": ["paralegal", "legal assistant"],
    "Intellectual Property": ["intellectual property", "patent law", "trademark"],

    # ------------------------------------------------------------------ #
    # agriculture
    # ------------------------------------------------------------------ #
    "Agriculture": ["agriculture", "farming", "agricultural"],
    "Crop Management": ["crop management", "crop production", "harvesting"],
    "Livestock": ["livestock", "animal husbandry", "cattle"],
    "Irrigation": ["irrigation", "water management"],
    "Agronomy": ["agronomy", "soil science", "soil analysis"],
    "Horticulture": ["horticulture", "landscaping", "greenhouse"],
    "Pest Control": ["pest control", "pest management", "integrated pest management"],

    # ------------------------------------------------------------------ #
    # automobile / automotive
    # ------------------------------------------------------------------ #
    "Automotive Repair": ["automotive repair", "auto repair", "vehicle maintenance", "auto mechanic"],
    "Engine Repair": ["engine repair", "engine diagnostics", "engine rebuild"],
    "Vehicle Diagnostics": ["vehicle diagnostics", "diagnostic testing", "obd"],
    "Welding": ["welding", "welder", "mig welding", "tig welding"],
    "Brake Systems": ["brake systems", "brake repair", "brakes"],

    # ------------------------------------------------------------------ #
    # aviation
    # ------------------------------------------------------------------ #
    "Aviation": ["aviation", "aeronautics"],
    "Aircraft Maintenance": ["aircraft maintenance", "aircraft mechanic", "a&p certification"],
    "Flight Operations": ["flight operations", "flight planning"],
    "Air Traffic Control": ["air traffic control", "atc"],
    "Aviation Safety": ["aviation safety", "faa regulations", "faa"],
    "Avionics": ["avionics"],

    # ------------------------------------------------------------------ #
    # construction / trades
    # ------------------------------------------------------------------ #
    "Construction Management": ["construction management", "site management", "construction supervision"],
    "Blueprint Reading": ["blueprint reading", "blueprints", "reading blueprints"],
    "Carpentry": ["carpentry", "carpenter", "framing"],
    "Masonry": ["masonry", "concrete", "bricklaying"],
    "Plumbing": ["plumbing", "plumber", "pipefitting"],
    "Electrical Systems": ["electrical wiring", "electrical systems", "electrician"],
    "Heavy Equipment": ["heavy equipment", "forklift", "crane operation"],
    "OSHA": ["osha", "osha compliance", "workplace safety"],
    "Estimating": ["cost estimating", "project estimation", "takeoffs"],
    "Surveying": ["land surveying", "surveying"],

    # ------------------------------------------------------------------ #
    # engineering (non-software)
    # ------------------------------------------------------------------ #
    "Mechanical Engineering": ["mechanical engineering", "mechanical design", "mechanical engineer"],
    "Electrical Engineering": ["electrical engineering", "electrical engineer", "circuit design"],
    "Civil Engineering": ["civil engineering", "civil engineer", "structural engineering"],
    "Chemical Engineering": ["chemical engineering", "chemical engineer", "process engineering"],
    "Manufacturing": ["manufacturing", "production planning", "assembly line"],
    "PLC Programming": ["plc", "plc programming", "scada"],
    "Robotics": ["robotics", "automation engineering"],
    "Thermodynamics": ["thermodynamics", "fluid mechanics"],

    # ------------------------------------------------------------------ #
    # BPO / call center
    # ------------------------------------------------------------------ #
    "Call Center Operations": ["call center", "contact center", "bpo operations"],
    "Telemarketing": ["telemarketing", "outbound calling", "inbound calls"],

    # ------------------------------------------------------------------ #
    # consulting / business
    # ------------------------------------------------------------------ #
    "Management Consulting": ["management consulting", "management consultant", "advisory services"],
    "Operations Management": ["operations management", "operations manager", "business operations"],
    "Supply Chain": ["supply chain", "logistics", "procurement", "warehouse management"],
    "Vendor Management": ["vendor management", "supplier management", "contract management"],
}
