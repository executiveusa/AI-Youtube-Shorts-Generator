# Railway Zero-Secrets Deployment Guide

This guide provides comprehensive instructions for deploying the AI Youtube Shorts Generator on Railway with zero-secrets bootstrapping and cost protection.

## Overview

This repository is configured for **zero-secrets deployment** on Railway, meaning it can be deployed immediately without requiring API keys or secrets. The application will run in a limited mode with manual highlight selection until secrets are provisioned.

## Quick Start (Zero-Secrets Mode)

Deploy to Railway in 3 steps:

### 1. Fork/Clone Repository
```bash
git clone https://github.com/executiveusa/AI-Youtube-Shorts-Generator.git
cd AI-Youtube-Shorts-Generator
```

### 2. Deploy to Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

### 3. Access Your Deployment
```bash
# Get deployment URL
railway domain
```

**Note**: In zero-secrets mode, the application will prompt for manual highlight timestamps instead of using AI.

## Configuration Files

This repository includes the following deployment configurations:

| File | Purpose |
|------|---------|
| `railway.toml` | Railway deployment configuration with cost guardrails |
| `nixpacks.toml` | Build configuration and system dependencies |
| `.agents` | Structured secret requirements for provisioning |
| `master.secrets.json.template` | Template for local secrets management |
| `maintenance.html` | Auto-deployed when free-tier limits exceeded |
| `COOLIFY_SUPPORT.md` | Alternative deployment on Coolify |
| `COOLIFY_MIGRATION.md` | Migration checklist from Railway to Coolify |

## Features

### ✅ Zero-Secrets Deployment
- Deploy immediately without API keys
- Application runs in manual mode
- No external dependencies required for basic operation

### ✅ Cost Protection
- Hard memory limit: 512MB
- CPU limit: 0.5 vCPU
- Monitoring for free-tier usage
- Auto-shutdown on limit breach
- Maintenance page deployment

### ✅ Fallback Modes
- **OpenAI Disabled**: Manual timestamp selection
- **GPU Unavailable**: CPU-based processing
- **Network Issues**: Graceful degradation

### ✅ Multi-Host Support
- Primary: Railway (free tier)
- Backup: Coolify (self-hosted)
- Optional: Hostinger VPN tunneling

## Deployment Modes

### Mode 1: Zero-Secrets (Default)

**Perfect for**: Testing, development, CI/CD

```bash
# No configuration needed
railway up

# Environment:
OPENAI_API=DISABLED
STUB_OPENAI=true
MANUAL_HIGHLIGHT_MODE=true
```

**Behavior**:
- Downloads YouTube videos ✅
- Transcribes audio ✅
- **Manual highlight selection** (user input)
- Crops and processes video ✅

### Mode 2: Full AI Mode

**Perfect for**: Production, automated workflows

```bash
# Set OpenAI API key in Railway dashboard
railway variables set OPENAI_API=sk-proj-your-key-here

# Or via CLI
railway variables set OPENAI_API="sk-proj-..." STUB_OPENAI=false
```

**Behavior**:
- Downloads YouTube videos ✅
- Transcribes audio ✅
- **AI-powered highlight extraction** (GPT-4)
- Crops and processes video ✅

## Environment Variables

### Core Variables

```bash
# Python configuration
PYTHON_VERSION=3.10
PYTHONUNBUFFERED=1

# Railway configuration
PORT=8080
RAILWAY_ENVIRONMENT=production

# Cost protection
FREE_TIER_MODE=true
ENABLE_COST_MONITORING=true
MAX_PROCESSING_TIME=300
```

### Optional Variables

```bash
# OpenAI API (optional, for AI mode)
OPENAI_API=sk-proj-your-key-here
STUB_OPENAI=false

# Performance tuning
CUDA_VISIBLE_DEVICES=-1  # Disable GPU
OMP_NUM_THREADS=2        # Limit CPU threads
```

### Setting Variables in Railway

**Via Dashboard**:
1. Go to Railway dashboard
2. Select your project
3. Click "Variables" tab
4. Add/edit variables
5. Deploy changes

**Via CLI**:
```bash
railway variables set OPENAI_API="sk-proj-..."
railway variables set STUB_OPENAI=false
```

## Secrets Management

### Local Development

1. **Copy template**:
   ```bash
   cp master.secrets.json.template master.secrets.json
   ```

2. **Edit secrets**:
   ```json
   {
     "projects": {
       "AI-Youtube-Shorts-Generator": {
         "secrets": {
           "OPENAI_API": {
             "value": "sk-proj-your-real-key-here"
           }
         }
       }
     }
   }
   ```

3. **Create .env**:
   ```bash
   echo "OPENAI_API=sk-proj-your-real-key-here" > .env
   ```

4. **Never commit**:
   ```bash
   # Already in .gitignore
   git check-ignore .env master.secrets.json
   ```

### Production (Railway)

**Best Practice**: Use Railway dashboard to set secrets

1. Navigate to project → Variables
2. Add `OPENAI_API` as secret variable
3. Set visibility to "Encrypted"
4. Deploy

## Cost Monitoring

### Free Tier Limits

Railway free tier includes:
- **500 hours/month** of runtime
- **100 GB/month** of egress
- **100 minutes/month** of build time

### Guardrails Implemented

1. **Resource Limits**:
   - Memory: 512MB maximum
   - CPU: 0.5 vCPU maximum
   - No GPU acceleration

2. **Auto-Shutdown**:
   - Triggers at 80% of free tier usage
   - Deploys maintenance page
   - Logs shutdown reason

3. **Monitoring Markers**:
   - Environment: `ENABLE_COST_MONITORING=true`
   - Logs: Check for "FREE_TIER_WARNING"
   - Status: Review Railway dashboard metrics

### Manual Monitoring

```bash
# Check current usage
railway status

# View logs for warnings
railway logs

# Check environment
railway variables
```

## Build Process

### Nixpacks Build

Railway uses Nixpacks for automatic builds:

```bash
# Phase 1: Setup
- Install system packages: ffmpeg, opencv, etc.

# Phase 2: Install
- Upgrade pip
- Install Python dependencies from requirements.txt

# Phase 3: Start
- Run: python main.py
```

### Build Time Optimization

```toml
# nixpacks.toml
[phases.install]
cmds = [
    "pip install --no-cache-dir -r requirements.txt"
]
```

**Tips**:
- Use `--no-cache-dir` to reduce build size
- Minimize dependencies
- Pre-compile large packages

## Troubleshooting

### Build Failures

**Problem**: Nixpacks build fails

```bash
# Check logs
railway logs --build

# Common issues:
# 1. Missing system dependencies → Update nixpacks.toml
# 2. Python version mismatch → Set PYTHON_VERSION=3.10
# 3. Dependency conflicts → Review requirements.txt
```

### Runtime Errors

**Problem**: Application crashes after deployment

```bash
# Check runtime logs
railway logs

# Common issues:
# 1. Missing OPENAI_API → Expected in zero-secrets mode
# 2. Memory limit → Reduce model size or increase limit
# 3. Port binding → Ensure PORT=8080
```

### OpenAI API Errors

**Problem**: "API key not found" or "Invalid API key"

```bash
# In zero-secrets mode:
# ✓ This is expected - application will prompt for manual input

# In full AI mode:
# 1. Check variable is set: railway variables
# 2. Verify key format: sk-proj-...
# 3. Test key locally first
# 4. Check OpenAI account status
```

### Free Tier Exceeded

**Problem**: Maintenance mode activated

```bash
# Check usage
railway status

# Options:
# 1. Wait for monthly reset
# 2. Upgrade Railway plan
# 3. Migrate to Coolify (see COOLIFY_MIGRATION.md)
```

## Usage Example

### Zero-Secrets Mode

```bash
# Deploy
railway up

# Application prompts:
Enter YouTube video URL: https://youtube.com/watch?v=...
# ... processing ...

MANUAL HIGHLIGHT SELECTION MODE
Enter the highlight timestamps for your short:
Start time (in seconds): 30
End time (in seconds): 90

✓ Selected highlight: 30s to 90s (duration: 60s)
Confirm this selection? (y/n): y

# ... video processing continues ...
```

### Full AI Mode

```bash
# Set API key
railway variables set OPENAI_API="sk-proj-..."

# Deploy
railway up

# Application auto-selects highlights:
Enter YouTube video URL: https://youtube.com/watch?v=...
# ... processing ...
AI analyzing transcript for highlights...
Start: 45, End: 105
# ... video processing continues ...
```

## Advanced Topics

### Custom Domains

```bash
# Add custom domain in Railway dashboard
# Or via CLI:
railway domain add your-domain.com
```

### Scaling

**Horizontal Scaling**: Not recommended (stateful video processing)

**Vertical Scaling**:
```toml
# railway.toml
[deploy.resources]
memoryLimit = "1Gi"  # Upgrade from 512Mi
cpuLimit = "1"       # Upgrade from 0.5
```

### Webhooks

Integration webhook for automated deployments:

```bash
# GitHub → Railway webhook (auto-configured)
# Or manual: railway webhook create
```

## Migration to Coolify

When Railway free tier is insufficient, migrate to Coolify:

1. Review [COOLIFY_MIGRATION.md](./COOLIFY_MIGRATION.md)
2. Follow step-by-step checklist
3. Estimated time: 3-4 hours
4. Cost: ~$5-20/month for VPS

## Support and Resources

- **Railway Docs**: https://docs.railway.app
- **Project Repository**: https://github.com/executiveusa/AI-Youtube-Shorts-Generator
- **Issues**: https://github.com/executiveusa/AI-Youtube-Shorts-Generator/issues
- **Railway Discord**: https://discord.gg/railway

## Security Best Practices

1. ✅ Never commit secrets to git
2. ✅ Use Railway encrypted variables
3. ✅ Rotate API keys every 90 days
4. ✅ Monitor API usage and costs
5. ✅ Use `.gitignore` for sensitive files
6. ✅ Keep `master.secrets.json` locally only

## Changelog

### v1.0.0 (2025-12-06)
- ✅ Zero-secrets deployment support
- ✅ Railway configuration with cost guardrails
- ✅ Manual fallback mode for OpenAI
- ✅ Maintenance page for auto-shutdown
- ✅ Coolify migration scaffolding
- ✅ Comprehensive documentation

---

**Status**: 🟢 Ready for Deployment

**Deployment URL**: `railway up` to generate

**Estimated Cost**: $0/month (free tier) → $5-20/month (Coolify)

**Last Updated**: 2025-12-06
