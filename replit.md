# TasteShift - Cultural Intelligence Platform

## Overview

TasteShift is a full-stack web application that generates audience personas using cultural intelligence from the Qloo Taste API and analyzes marketing campaign alignment with Google Gemini AI. The platform provides marketers with data-driven insights into cultural taste patterns and generates creative campaign suggestions based on target demographics and regions.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python) with SQLAlchemy ORM
- **Database**: SQLite for local development, designed to support PostgreSQL/Supabase for production
- **API Structure**: RESTful endpoints for persona generation and campaign analysis
- **CORS**: Enabled for cross-origin requests from frontend

### Frontend Architecture
- **Framework**: Vanilla JavaScript with React-like component structure
- **UI Library**: Bootstrap 5 with dark theme
- **Icons**: Font Awesome for visual elements
- **State Management**: Global JavaScript state for current persona and loading states

### Database Design
- **Persona Model**: Stores region, demographic, taste data (JSON), and AI-generated descriptions
- **CampaignAnalysis Model**: Links to personas with campaign briefs, taste shock scores, and creative suggestions
- **Relationships**: One-to-many relationship between Persona and CampaignAnalysis

## Key Components

### Backend Services
1. **Qloo Service** (`services/qloo_service.py`)
   - Fetches cultural taste patterns from Qloo API
   - Handles region and demographic-based queries
   - Returns cross-domain taste data (music, food, film, fashion, books, brands)

2. **Gemini Service** (`services/gemini_service.py`)
   - Generates detailed persona descriptions from taste data
   - Analyzes campaign alignment and cultural fit
   - Provides taste shock scores and creative suggestions

3. **Supabase Service** (`services/supabase_service.py`)
   - Database connection management
   - Query execution wrapper
   - Designed for PostgreSQL integration

### Frontend Components
1. **Navigation**: Single-page application with section switching
2. **Persona Generation Form**: Region and demographic selection
3. **Campaign Analysis Form**: Campaign brief input and analysis
4. **Results Display**: Persona descriptions, scores, and suggestions
5. **History View**: Saved personas and analyses

## Data Flow

1. **Persona Generation**:
   - User selects region and demographic
   - Backend calls Qloo API for taste patterns
   - Gemini AI generates persona description
   - Data saved to database via SQLAlchemy

2. **Campaign Analysis**:
   - User inputs campaign brief
   - System analyzes against current persona
   - Gemini AI provides taste shock score (0-100)
   - Creative suggestions generated and displayed

3. **Data Persistence**:
   - All personas and analyses stored in database
   - JSON serialization for complex data structures
   - RESTful API endpoints for data retrieval

## External Dependencies

### APIs
- **Qloo Taste API**: Cultural intelligence and taste pattern data
- **Google Gemini Pro**: AI content generation and analysis
- **Supabase**: PostgreSQL database hosting (configured but using SQLite locally)

### Frontend Libraries
- **Bootstrap 5**: CSS framework with dark theme
- **Font Awesome**: Icon library
- **Vanilla JavaScript**: No framework dependencies

### Python Packages
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **Flask-CORS**: Cross-origin resource sharing
- **Requests**: HTTP client for API calls
- **Google GenAI**: Gemini API client

## Deployment Strategy

### Current Setup
- **Environment**: Designed for Replit deployment
- **Database**: SQLite for development, PostgreSQL-ready for production
- **Static Files**: Served via Flask
- **Port Configuration**: Flask server on port 5000
- **CORS**: Configured for frontend-backend communication

### Environment Variables
- `QLOO_API_KEY`: Authentication for Qloo API
- `GEMINI_API_KEY`: Google AI API authentication
- `SUPABASE_URL`: Database connection URL
- `SUPABASE_ANON_KEY`: Database access key
- `DATABASE_URL`: Optional PostgreSQL connection string

### Deployment Considerations
- All API keys stored in environment variables
- ProxyFix middleware for proper header handling
- Database auto-creation on startup
- Debug mode enabled for development
- Static file serving from Flask

The application is architected as a monolithic deployment suitable for Replit's hosting environment, with clear separation of concerns between data access, business logic, and presentation layers.