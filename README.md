# Fashion Design System

A fashion design system built on top of Stable Diffusion.

## Project Structure

```
fashion-sd/
├── models/           # Database models
├── config/          # Configuration files
├── inference.py     # Image generation script
└── requirements.txt # Project dependencies
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up PostgreSQL database and update the configuration in `config/database.py`

3. Run the database initialization script:
```bash
python3 -m models.init_db
```

4. Run tests:
```bash
python3 -m pytest tests/
```

## Database Schema

The system uses a PostgreSQL database with the following schema:

```sql
CREATE TABLE fashion_designs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prompt TEXT NOT NULL,
    negative_prompt TEXT NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    file_path TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
``` 