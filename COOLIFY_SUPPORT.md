# Coolify Deployment Support

This document provides configuration markers and deployment guidance for deploying the AI Youtube Shorts Generator on Coolify as an alternative or backup to Railway.

## Overview

Coolify is a self-hosted, open-source alternative to Heroku/Railway/Vercel. This project includes pre-configured markers and scaffolding for Coolify deployment.

**Status**: ⚠️ Not Active by Default - Configuration scaffolding ready

## Prerequisites

- Coolify instance running (self-hosted or managed)
- Docker support enabled
- Access to Coolify dashboard
- Hostinger VPN (optional, for secure tunneling)

## Coolify Configuration

### Build Configuration

```yaml
# Coolify will auto-detect Python and use nixpacks
buildpack: nixpacks
dockerfile: ./Dockerfile.coolify  # Optional custom Dockerfile
```

### Environment Variables

Set these in Coolify dashboard:

```bash
# Core Configuration
PYTHON_VERSION=3.10
PYTHONUNBUFFERED=1
PORT=8080

# Optional: OpenAI Integration
OPENAI_API=your_openai_api_key_here

# Cost Protection
FREE_TIER_MODE=false
ENABLE_COST_MONITORING=false

# Coolify-specific
COOLIFY_DEPLOYMENT=true
```

### Resource Limits

Configure in Coolify UI:
- **Memory**: 512MB - 1GB recommended
- **CPU**: 0.5 - 1.0 vCPU
- **Disk**: 2GB minimum
- **Network**: Unlimited (self-hosted)

## System Dependencies

Coolify deployment requires these system packages:

```bash
# Installed via nixpacks.toml
- ffmpeg
- libsm6
- libxext6
- libxrender-dev
- libgomp1
- libopencv-dev
```

## Deployment Steps

### Option 1: Direct Git Deployment

1. **Connect Repository**
   ```
   Coolify Dashboard → New Resource → Git Repository
   Repository: https://github.com/executiveusa/AI-Youtube-Shorts-Generator
   Branch: main
   ```

2. **Configure Build**
   - Build Type: Nixpacks
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`

3. **Set Environment Variables**
   - Navigate to Environment Variables tab
   - Add required variables (see above)

4. **Deploy**
   - Click "Deploy" button
   - Monitor logs for successful startup

### Option 2: Docker Deployment

```dockerfile
# Dockerfile.coolify (create if needed)
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8080

# Start application
CMD ["python", "main.py"]
```

Deploy:
```bash
# In Coolify
Build Type: Dockerfile
Dockerfile Path: ./Dockerfile.coolify
```

## Hostinger VPN Integration

### Purpose
Use Hostinger VPN to create a secure tunnel from your Coolify instance to the internet, providing additional security and network isolation.

### Configuration

1. **Install VPN Client on Coolify Host**
   ```bash
   # SSH into your Coolify server
   ssh user@your-coolify-server
   
   # Install OpenVPN or WireGuard
   apt-get update
   apt-get install openvpn wireguard
   ```

2. **Configure Hostinger VPN**
   ```bash
   # Download VPN config from Hostinger
   # Place in /etc/openvpn/client/
   
   # Start VPN
   systemctl start openvpn-client@hostinger
   systemctl enable openvpn-client@hostinger
   ```

3. **Route Coolify Traffic Through VPN**
   ```bash
   # Configure routing rules
   # Add to /etc/network/interfaces or iptables
   
   # Verify VPN connection
   curl ifconfig.me  # Should show VPN IP
   ```

4. **Update Coolify Environment**
   ```bash
   HOSTINGER_VPN_ENABLED=true
   HOSTINGER_VPN_ENDPOINT=vpn.hostinger.com
   NETWORK_TUNNEL=active
   ```

### VPN Benefits
- ✅ Secure external API access
- ✅ IP masking for rate-limit protection
- ✅ Additional layer of security
- ✅ Geographic flexibility

### VPN Limitations
- ⚠️ Additional latency (~50-200ms)
- ⚠️ VPN connection must remain stable
- ⚠️ Requires manual VPN management

## Health Checks

Configure health checks in Coolify:

```yaml
healthcheck:
  enabled: false  # No web server by default
  path: /
  port: 8080
  interval: 30s
  timeout: 10s
  retries: 3
```

## Monitoring and Logs

### Access Logs
```bash
# In Coolify dashboard
Navigate to: Deployment → Logs → Runtime Logs
```

### Resource Monitoring
```bash
# Monitor resource usage
Coolify Dashboard → Resource → Metrics
```

## Migration from Railway

See [COOLIFY_MIGRATION.md](./COOLIFY_MIGRATION.md) for step-by-step migration guide.

## Cost Comparison

| Feature | Railway (Free) | Coolify (Self-Hosted) |
|---------|---------------|----------------------|
| Monthly Cost | $0 (500 hrs) | VPS cost (~$5-20/mo) |
| Build Minutes | 100 min/mo | Unlimited |
| Egress | 100 GB/mo | Unlimited (VPS-dependent) |
| Memory | Shared | Dedicated (VPS-dependent) |
| CPU | Shared | Dedicated (VPS-dependent) |
| Control | Limited | Full control |

## Troubleshooting

### Build Failures
```bash
# Check nixpacks.toml configuration
# Ensure all system dependencies are listed
# Verify Python version compatibility
```

### Runtime Errors
```bash
# Check environment variables are set
# Verify file permissions
# Check logs for specific errors
```

### VPN Connection Issues
```bash
# Test VPN connectivity
ping 8.8.8.8

# Check VPN service status
systemctl status openvpn-client@hostinger

# Restart VPN
systemctl restart openvpn-client@hostinger
```

## Support and Resources

- **Coolify Documentation**: https://coolify.io/docs
- **Project Repository**: https://github.com/executiveusa/AI-Youtube-Shorts-Generator
- **Hostinger VPN**: https://www.hostinger.com/vpn

## Status Markers

```yaml
coolify_support:
  status: scaffolded
  ready_for_activation: true
  tested: false
  documentation_complete: true
  
hostinger_vpn:
  status: documented
  active: false
  configuration_required: true
  manual_setup_needed: true
```

## Next Steps

1. ✅ Review this configuration
2. ⬜ Set up Coolify instance
3. ⬜ Configure Hostinger VPN (optional)
4. ⬜ Deploy and test
5. ⬜ Update status markers in this file

---

**Note**: This is a scaffolding document. Coolify deployment is not active by default. To activate, follow the deployment steps above and update the status markers.
