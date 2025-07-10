# TasteShift - Cultural Intelligence Platform

A full-stack web application that generates audience personas using the Qloo Taste API and analyzes campaign alignment with Google Gemini AI.

## Features

- **Cultural Persona Generation**: Generate detailed audience personas based on region and demographic using Qloo's cultural intelligence API
- **Campaign Analysis**: Analyze marketing campaigns against generated personas with AI-powered insights
- **Taste Shock Score**: Get a 0-100 score indicating how culturally aligned or disruptive your campaign is
- **Creative Suggestions**: Receive AI-generated creative suggestions including taglines, concepts, and visual directions
- **Persona History**: Store and retrieve generated personas and analyses using Supabase

## Tech Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: Database ORM
- **Flask-CORS**: Cross-origin resource sharing
- **Requests**: HTTP library for API calls

### Frontend
- **React**: JavaScript UI library (vanilla JS implementation)
- **Bootstrap 5**: CSS framework with dark theme
- **Font Awesome**: Icon library

### APIs & Services
- **Qloo Taste API**: Cultural intelligence and taste patterns
- **Google Gemini Pro**: AI content generation and analysis
- **Supabase**: PostgreSQL database for data persistence

## Setup Instructions

### Prerequisites
- Python 3.8+
- Access to Replit or local development environment

### Environment Variables
Set the following environment variables in your Replit secrets or `.env` file:

```env
# Qloo API Configuration
QLOO_API_URL=https://hackathon.api.qloo.com
QLOO_API_KEY=W-_OejnIgjKjlrZT1exz0fFtkIEf7UtwfwuW33rgedU

# Google Gemini API
GEMINI_API_KEY=AIzaSyBbYvRipCZLg2qn2ySFkiKnRjXcp164vG0

# Supabase Configuration
SUPABASE_URL=https://soxuvylsurltctqhendh.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNveHV2eWxzdXJsdGN0cWhlbmRoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIxMjg0MDksImV4cCI6MjA2NzcwNDQwOX0.p5jVtshmHS_TIKSQvb5I2drtcaU0MMkpLQZXYlEa0ro

# Database (from Supabase project settings)
DATABASE_URL=postgresql://[username]:[password]@[host]:[port]/[database]

# Session Security
SESSION_SECRET=your-secret-key-here
