# News Aggregation System - Server

## Purpose
Backend API for aggregating, storing, and serving news articles with user authentication and admin management.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set environment variables :
   - `SECRET_KEY`
   - `SMTP_PASSWORD`
3. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
