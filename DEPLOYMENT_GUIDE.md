# 🚀 Sports Betting Bot - Deployment Guide

This guide will help you deploy your Sports Betting Bot to various hosting platforms.

## 📋 Quick Deployment Options

### 🔥 **RECOMMENDED: Railway (Easiest)**
**✅ Free tier available, great for Python apps**

1. **Sign up** at [railway.app](https://railway.app)
2. **Connect your GitHub** repository
3. **Deploy with one click** - Railway will automatically detect your Python app
4. **Set environment variables** in Railway dashboard:
   - `ODDS_API_KEY` = your API key from the-odds-api.com
   - `FLASK_ENV` = production
5. **Your app will be live** at: `https://your-app-name.railway.app`

### 🎨 **Render (Great free option)**
**✅ Free tier with 750 hours/month**

1. **Sign up** at [render.com](https://render.com)
2. **Create new Web Service** from GitHub repo
3. **Configure:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT web_app:app`
4. **Set environment variables:**
   - `ODDS_API_KEY` = your API key
   - `PYTHON_VERSION` = 3.11.0
   - `FLASK_ENV` = production
5. **Deploy!** Your app will be at: `https://your-app-name.onrender.com`

### ⚡ **Vercel (Serverless)**
**✅ Great for static + serverless functions**

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```
2. **Deploy:**
   ```bash
   vercel --prod
   ```
3. **Set environment variables** in Vercel dashboard
4. **Your app will be live** at: `https://your-app-name.vercel.app`

### 🌊 **DigitalOcean App Platform**
**💰 $5/month minimum**

1. **Sign up** at [digitalocean.com](https://digitalocean.com)
2. **Create App** from GitHub
3. **Configure** Python app with gunicorn
4. **Set environment variables**
5. **Deploy** - will be at: `https://your-app-name-random.app.ondigitalocean.app`

---

## 🔧 Pre-Deployment Checklist

### ✅ **Files Ready for Deployment**
All these files are already created for you:

- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Process configuration
- ✅ `railway.json` - Railway configuration  
- ✅ `render.yaml` - Render configuration
- ✅ `vercel.json` - Vercel configuration
- ✅ `wsgi.py` - Production WSGI entry point

### 🔑 **Environment Variables Needed**

**Required:**
- `ODDS_API_KEY` - Your API key from the-odds-api.com

**Optional:**
- `FLASK_ENV` - Set to "production" for live deployment
- `PORT` - Will be set automatically by hosting provider

### 📚 **Get Your API Key**

1. Visit [the-odds-api.com](https://the-odds-api.com)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Set it as an environment variable in your hosting platform

---

## 🏆 **Recommended Deployment Steps**

### 🚀 **Option 1: Railway (Recommended)**

1. **Push to GitHub** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/sports-betting-bot.git
   git push -u origin main
   ```

2. **Deploy to Railway:**
   - Go to [railway.app](https://railway.app)
   - Click "Deploy from GitHub repo"
   - Select your repository  
   - Railway automatically detects Python and uses the Procfile
   - Add environment variable: `ODDS_API_KEY`
   - Your app will be live in ~2 minutes!

3. **Custom Domain (Optional):**
   - In Railway dashboard, go to Settings → Domains
   - Add your custom domain
   - Update DNS records as instructed

### 🎨 **Option 2: Render**

1. **Deploy to Render:**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Use these settings:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT web_app:app`
   - Add environment variables
   - Deploy!

---

## 🌍 **Custom Domain Setup**

### **For Railway:**
1. **Buy domain** (Namecheap, GoDaddy, etc.)
2. **In Railway:** Settings → Domains → Add domain
3. **In DNS settings:** Add CNAME record pointing to Railway URL

### **For Render:**
1. **In Render:** Settings → Custom Domains
2. **Add your domain** and follow DNS instructions
3. **SSL certificate** is automatically provided

---

## 🔒 **Security & Production Notes**

### **✅ Production Best Practices:**
- ✅ Environment variables are used for secrets
- ✅ Debug mode is disabled in production
- ✅ Gunicorn is used instead of Flask dev server
- ✅ CORS is configured properly
- ✅ Error handling is implemented

### **🔐 API Key Security:**
- ✅ Never commit API keys to Git
- ✅ Use environment variables only
- ✅ Each platform has secure environment variable storage

### **📊 Monitoring:**
- Most platforms provide built-in monitoring
- Check logs for any deployment issues
- Monitor API usage to avoid rate limits

---

## 🆘 **Troubleshooting**

### **Common Issues:**

**❌ "Application failed to start"**
- Check that `requirements.txt` includes all dependencies
- Verify `Procfile` is correct
- Check logs for Python errors

**❌ "Module not found"**
- Make sure all Python files are in the root directory
- Check that imports are correct
- Verify Python version compatibility

**❌ "API key not found"**
- Set `ODDS_API_KEY` environment variable
- Check spelling of environment variable name
- Restart the app after setting variables

**❌ "Port already in use"**
- Use `PORT` environment variable instead of hardcoded port
- Most platforms set this automatically

### **📞 Support:**
- **Railway:** Great documentation + Discord community
- **Render:** Good docs + email support  
- **Vercel:** Excellent docs + community
- **DigitalOcean:** Professional support available

---

## 🎯 **Next Steps After Deployment**

1. **✅ Test all features** on the live site
2. **📱 Share the URL** with others
3. **📊 Monitor API usage** to stay within limits
4. **🔄 Set up automatic deployments** from GitHub
5. **📈 Consider upgrading** to paid plans for more features

**🎉 Congratulations! Your Sports Betting Bot is now live!**

---

## 📚 **Additional Resources**

- [The Odds API Documentation](https://the-odds-api.com/liveapi/guides/v4/)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Gunicorn Documentation](https://gunicorn.org/)
- [Railway Documentation](https://docs.railway.app/)
- [Render Documentation](https://render.com/docs)
