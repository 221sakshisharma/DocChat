GET_MATCHING_TAGS_SYSTEM_PROMPT = "\n\n".join([
    "You are an expert text analyzer.",
    "Your task is to select the 2 or 3 most relevant tags that best represent the main topics of the given text.",
    "Choose ONLY from the provided tag list.",
    "Do NOT invent new tags.",
    "Return BETWEEN 2 AND 3 tags only.",
    "Output must be STRICTLY valid JSON and nothing else:",
    "{\"tags\": [\"tag1\", \"tag2\"]}"
])

RESPOND_TO_MESSAGE_SYSTEM_PROMPT = "\n\n".join([
    "You are a chatbot who has some specific set of knowledge and you will be asked questions on that given the knowledge.",
    "Don't make up information and don't answer until and unless you have knowledge to back it.",
    "Knowledge you have:",
    "{{knowledge}}"
])

PREDEFINED_TAGS = [
    # Core tech & AI
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "data science",
    "technology",
    "software engineering",
    "system design",

    # Web & software
    "web development",
    "frontend",
    "backend",
    "full stack",
    "mobile development",
    "open source",

    # Infra & security
    "cloud computing",
    "devops",
    "cybersecurity",
    "networking",
    "distributed systems",

    # Business & management
    "business",
    "finance",
    "marketing",
    "product management",
    "entrepreneurship",
    "startups",
    "strategy",

    "research",

    # Education & learning
    "education",
    "career",
    "interview preparation",
    "skill development",

    # Health & social
    "healthcare",
    "mental health",
    "psychology",
    "social impact",

    # Media & content
    "documentation",
    "design",

    # Emerging & misc
    "blockchain",
    "iot",
    "automation",
    "robotics",
    "sustainability",
    "innovation",
]
