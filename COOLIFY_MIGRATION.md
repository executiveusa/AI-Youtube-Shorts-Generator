# Migration Checklist: Railway to Coolify

This document provides a step-by-step checklist for migrating the AI Youtube Shorts Generator from Railway to Coolify when free-tier limits are exceeded or manual migration is desired.

## Migration Triggers

This migration should be initiated when:
- ✅ Railway free tier limits are approaching (>80% usage)
- ✅ Auto-shutdown has been triggered
- ✅ Maintenance mode is active
- ✅ Manual decision to migrate to self-hosted solution
- ✅ Need for more control over infrastructure

## Pre-Migration Checklist

### 1. Assessment Phase
- [ ] Review current Railway usage metrics
- [ ] Document current environment variables
- [ ] Export Railway logs for reference
- [ ] Take note of current deployment configuration
- [ ] Backup any persistent data (if applicable)
- [ ] Review cost projections for Coolify hosting

### 2. Coolify Setup
- [ ] Provision VPS or dedicated server for Coolify
  - Recommended: 2GB RAM, 2 vCPU, 20GB SSD minimum
  - Providers: DigitalOcean, Linode, Hetzner, Vultr
- [ ] Install Coolify on the server
  ```bash
  curl -fsSL https://get.coolify.io | bash
  ```
- [ ] Access Coolify dashboard (usually at http://your-server-ip:8000)
- [ ] Complete Coolify initial setup wizard
- [ ] Configure SSL/TLS certificates (Let's Encrypt)

### 3. Environment Preparation
- [ ] Retrieve all secrets from Railway dashboard
- [ ] Document all environment variables:
  ```
  OPENAI_API=...
  PYTHON_VERSION=...
  PORT=...
  (add others as needed)
  ```
- [ ] Update `master.secrets.json` with production values
- [ ] Verify `.agents` file is current with all required secrets

## Migration Steps

### Phase 1: Coolify Configuration (30 minutes)

#### Step 1: Create New Project
- [ ] Log into Coolify dashboard
- [ ] Click "New Resource"
- [ ] Select "Git Repository"
- [ ] Enter repository URL: `https://github.com/executiveusa/AI-Youtube-Shorts-Generator`
- [ ] Select branch: `main`
- [ ] Name: `ai-youtube-shorts-generator`

#### Step 2: Configure Build Settings
- [ ] Build Type: Select "Nixpacks"
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `python main.py`
- [ ] Port: `8080`
- [ ] Health Check: Disable (or configure custom)

#### Step 3: Set Environment Variables
- [ ] Navigate to Environment Variables section
- [ ] Add all variables from Railway:
  ```bash
  PYTHON_VERSION=3.10
  PYTHONUNBUFFERED=1
  PORT=8080
  OPENAI_API=<your_key_here>
  COOLIFY_DEPLOYMENT=true
  FREE_TIER_MODE=false
  ```
- [ ] Remove Railway-specific variables
- [ ] Verify all secrets are correctly entered

#### Step 4: Configure Resources
- [ ] Memory Limit: 512MB - 1GB
- [ ] CPU Limit: 0.5 - 1.0 vCPU
- [ ] Disk Space: 2GB minimum
- [ ] Enable auto-restart on failure

### Phase 2: Deployment Testing (20 minutes)

#### Step 5: Initial Deployment
- [ ] Click "Deploy" button in Coolify
- [ ] Monitor build logs for errors
- [ ] Wait for deployment to complete
- [ ] Verify deployment status shows "Running"

#### Step 6: Smoke Testing
- [ ] Access application URL provided by Coolify
- [ ] Test basic functionality:
  - [ ] Application starts without errors
  - [ ] Can process a test video URL
  - [ ] OpenAI integration works (if enabled)
  - [ ] Video processing completes
  - [ ] Output files are generated
- [ ] Review application logs for warnings/errors

#### Step 7: Performance Verification
- [ ] Monitor resource usage (CPU, Memory)
- [ ] Verify response times are acceptable
- [ ] Check for memory leaks or resource exhaustion
- [ ] Run load test (if applicable)

### Phase 3: DNS and Domain Setup (15 minutes)

#### Step 8: Domain Configuration
- [ ] In Coolify, navigate to Domain settings
- [ ] Add custom domain (optional): `shorts.yourdomain.com`
- [ ] Enable SSL/TLS (Let's Encrypt)
- [ ] Update DNS records:
  ```
  Type: A
  Name: shorts (or @)
  Value: <your-coolify-server-ip>
  TTL: 300
  ```
- [ ] Wait for DNS propagation (5-30 minutes)
- [ ] Verify HTTPS works correctly

### Phase 4: Railway Decommissioning (10 minutes)

#### Step 9: Gradual Migration
- [ ] Keep Railway deployment running for 24-48 hours
- [ ] Monitor Coolify deployment for stability
- [ ] Update any external links/integrations to new URL
- [ ] Notify users of new endpoint (if applicable)

#### Step 10: Railway Cleanup
- [ ] Verify Coolify deployment is stable
- [ ] Stop Railway service
- [ ] Download any logs from Railway for archive
- [ ] Remove Railway project (optional, can keep as backup)
- [ ] Cancel Railway subscription (if paid)

### Phase 5: Post-Migration (30 minutes)

#### Step 11: Monitoring Setup
- [ ] Configure Coolify monitoring/alerts
- [ ] Set up uptime monitoring (UptimeRobot, Pingdom, etc.)
- [ ] Configure log retention policies
- [ ] Set up backup strategy for persistent data

#### Step 12: Documentation Updates
- [ ] Update README.md with new deployment URL
- [ ] Update deployment documentation
- [ ] Document Coolify-specific configurations
- [ ] Update `master.secrets.json` with Coolify details

#### Step 13: Cost Analysis
- [ ] Document monthly VPS costs
- [ ] Track bandwidth usage
- [ ] Monitor compute resources
- [ ] Compare with Railway costs
- [ ] Optimize resource allocation if needed

## Hostinger VPN Setup (Optional)

### Step 14: VPN Configuration
- [ ] Subscribe to Hostinger VPN service
- [ ] Download OpenVPN or WireGuard configuration
- [ ] SSH into Coolify server
- [ ] Install VPN client:
  ```bash
  apt-get update
  apt-get install openvpn wireguard
  ```
- [ ] Copy VPN configuration:
  ```bash
  scp hostinger-vpn.ovpn user@coolify-server:/etc/openvpn/client/
  ```
- [ ] Start VPN service:
  ```bash
  systemctl start openvpn-client@hostinger
  systemctl enable openvpn-client@hostinger
  ```
- [ ] Verify VPN connection:
  ```bash
  curl ifconfig.me  # Should show VPN IP
  ```
- [ ] Update Coolify environment:
  ```bash
  HOSTINGER_VPN_ENABLED=true
  ```

## Rollback Plan

In case of migration issues:

### Emergency Rollback to Railway
- [ ] Re-enable Railway service immediately
- [ ] Update DNS back to Railway endpoint
- [ ] Investigate Coolify issues
- [ ] Document problems encountered
- [ ] Plan remediation before next migration attempt

### Coolify Troubleshooting
- [ ] Check Coolify logs: Dashboard → Deployment → Logs
- [ ] Verify environment variables are correct
- [ ] Check system resource availability
- [ ] Review nixpacks build logs
- [ ] Verify network connectivity
- [ ] Check VPN status (if applicable)

## Success Criteria

Migration is complete when:
- ✅ Coolify deployment is running stably for 48+ hours
- ✅ All functionality works as expected
- ✅ Performance metrics are acceptable
- ✅ Monitoring and alerts are configured
- ✅ Documentation is updated
- ✅ Railway is safely decommissioned
- ✅ Cost projections are confirmed

## Post-Migration Optimization

### Week 1
- [ ] Monitor resource usage patterns
- [ ] Adjust memory/CPU allocations as needed
- [ ] Fine-tune auto-restart policies
- [ ] Optimize build process

### Week 2-4
- [ ] Review cost vs. Railway
- [ ] Implement additional monitoring
- [ ] Set up automated backups
- [ ] Consider horizontal scaling if needed

## Support Resources

- **Coolify Docs**: https://coolify.io/docs
- **Coolify Discord**: https://discord.gg/coolify
- **Project Issues**: https://github.com/executiveusa/AI-Youtube-Shorts-Generator/issues
- **VPS Providers**: DigitalOcean, Linode, Hetzner, Vultr

## Migration Timeline Estimate

| Phase | Estimated Time | Complexity |
|-------|---------------|------------|
| Pre-Migration | 1-2 hours | Low |
| Coolify Setup | 30 minutes | Medium |
| Deployment Testing | 20 minutes | Low |
| DNS Setup | 15 minutes | Low |
| Railway Cleanup | 10 minutes | Low |
| Post-Migration | 30 minutes | Low |
| VPN Setup (Optional) | 30 minutes | Medium |
| **Total** | **3-4 hours** | **Medium** |

## Notes

- Keep `master.secrets.json` updated throughout migration
- Document any custom configurations or deviations
- Take screenshots of configurations for reference
- Keep Railway and Coolify running in parallel during testing
- Plan migration during low-traffic period

---

**Status**: ⬜ Not Started | ⏳ In Progress | ✅ Completed

**Migration Date**: _________________

**Migrated By**: _________________

**Rollback Required**: Yes ⬜ / No ⬜

**Notes**:
```
[Add any migration-specific notes, issues encountered, or lessons learned]
```

---

**Last Updated**: 2025-12-06
