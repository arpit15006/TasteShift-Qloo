# TasteShift Deployment Guide

This guide covers multiple deployment options for the TasteShift application.

## Prerequisites

Before deploying, ensure you have:
- Your code in a Git repository (GitHub, GitLab, etc.)
- API keys for Gemini and Qloo
- Supabase database configured

## Environment Variables

All deployment platforms will need these environment variables:

```env
GEMINI_API_KEY=AIzaSyCJmaRDeEs4SQOYLkpQv_JVVoC_-mXe1N8
QLOO_API_KEY=W-_OejnIgjKjlrZT1exz0fFtkIEf7UtwfwuW33rgedU
SUPABASE_URL=https://onscypevhzxnucswtspm.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9uc2N5cGV2aHp4bnVjc3d0c3BtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIyMjk1NDEsImV4cCI6MjA2NzgwNTU0MX0.44Ykn5tfwFi0JhAmFqJSBSVE4dh2gt6j3RIADCZoSm0
DATABASE_URL=postgresql://postgres.onscypevhzxnucswtspm:Arpit1234@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
SESSION_SECRET=your-random-secret-key-here
```

## Deployment Options

### 1. Railway (Recommended) 🚂

Railway is excellent for Flask apps with PostgreSQL support.

**Steps:**
1. Go to [railway.app](https://railway.app)
2. Sign up/login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect the Python app
6. Add environment variables in the Variables tab
7. Deploy!

**Features:**
- Automatic HTTPS
- Custom domains
- Built-in PostgreSQL (optional)
- Easy scaling

### 2. Render 🎨

Great free tier with automatic deployments.

**Steps:**
1. Go to [render.com](https://render.com)
2. Connect your GitHub repository
3. Choose "Web Service"
4. Use these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn main:app --bind 0.0.0.0:$PORT`
5. Add environment variables
6. Deploy!

### 3. Vercel ⚡

Serverless deployment, great for demos.

**Steps:**
1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in your project directory
3. Follow the prompts
4. Add environment variables in Vercel dashboard

### 4. Heroku 🟣

Classic PaaS platform.

**Steps:**
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Add environment variables: `heroku config:set GEMINI_API_KEY=your-key`
5. Deploy: `git push heroku main`

### 5. Docker 🐳

For containerized deployment on any platform.

**Local Testing:**
```bash
# Build the image
docker build -t tasteshift .

# Run with environment file
docker run -p 5000:5000 --env-file .env tasteshift
```

**Docker Compose:**
```bash
# Create .env file with your variables
cp .env.example .env

# Start the application
docker-compose up -d
```

### 6. Replit (Already Configured) 🔄

Your app is already configured for Replit deployment.

**Steps:**
1. Import your GitHub repo to Replit
2. Add secrets in the Secrets tab
3. Click Run!

## Post-Deployment Checklist

After deploying to any platform:

1. **Test the application** - Visit your deployed URL
2. **Check database connection** - Ensure Supabase is connected
3. **Test API endpoints** - Try generating a persona
4. **Monitor logs** - Check for any errors
5. **Set up custom domain** (optional)

## Troubleshooting

### Common Issues:

**Database Connection Errors:**
- Verify DATABASE_URL is correct
- Check Supabase IP allowlist
- Ensure psycopg2-binary is installed

**API Key Errors:**
- Verify all environment variables are set
- Check API key validity
- Ensure no extra spaces in keys

**Build Failures:**
- Check Python version compatibility
- Verify requirements.txt is complete
- Check for missing system dependencies

**Port Issues:**
- Most platforms auto-assign PORT
- Ensure your app uses `os.environ.get('PORT', 5000)`

## Performance Optimization

For production deployments:

1. **Enable caching** for static files
2. **Use CDN** for assets
3. **Monitor performance** with platform tools
4. **Set up health checks**
5. **Configure auto-scaling** if available

## Security Considerations

1. **Never commit API keys** to version control
2. **Use environment variables** for all secrets
3. **Enable HTTPS** (most platforms do this automatically)
4. **Set strong SESSION_SECRET**
5. **Monitor API usage** to prevent abuse

Choose the deployment option that best fits your needs. Railway and Render are recommended for their ease of use and free tiers.
