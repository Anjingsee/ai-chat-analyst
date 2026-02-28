# ai-chat-analyst
一个测试项目

项目结构：
ai-chat-analyst/
├── main.py                 # Application entry point
├── config.py              # Configuration management
├── database.py            # Database setup
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic schemas
├── requirements.txt       # Dependencies
├── .env.example           # Environment variables example
├── .gitignore             # Git ignore file
├── README.md              # This file
├── api/                   # API routes
│   ├── __init__.py
│   ├── health.py         # Health check endpoints
│   ├── chat.py           # Chat endpoints
│   ├── files.py          # File endpoints
│   └── analysis.py       # Analysis endpoints
├── services/             # Business logic
│   ├── __init__.py
│   ├── llm_service.py    # LLM integration
│   ├── file_service.py   # File handling
│   └── analysis_service.py # Analysis logic
├── utils/                # Utilities
│   ├── __init__.py
│   ├── chart_generator.py # Chart generation
│   └── statistical_analyzer.py # Statistics
└── uploads/              # File storage
