# 🗺️ Roadmap - NexusLab

## Faza 1: MVP (2-3 tygodnie) ⏳ IN PROGRESS

### Week 1: Django Foundation
- [x] VPS setup (Hostinger)
- [x] PostgreSQL database
- [x] n8n workflow Gratka scraper
- [ ] Django project structure
  - [ ] Create apps (website, accounts, gratka, chatbot, dashboard)
  - [ ] Configure settings (base, production)
  - [ ] Setup .env variables
- [ ] Database models
  - [ ] UserConfig
  - [ ] UserOffer
- [ ] Django AllAuth integration
- [ ] Admin panel customization

### Week 2: Core Features
- [ ] Landing page (nexuslab.pl)
  - [ ] Hero section
  - [ ] Services overview
  - [ ] Pricing table
  - [ ] Contact form
- [ ] Authentication
  - [ ] Login/Register
  - [ ] Email verification
  - [ ] Password reset
- [ ] Gratka Panel (gratka.nexuslab.pl)
  - [ ] Config form (HTMX)
  - [ ] Webhook to save config
  - [ ] User dashboard (oferty)
  - [ ] Multi-tenant RLS
- [ ] n8n multi-user integration
  - [ ] Read all user configs
  - [ ] Dynamic URL per user
  - [ ] Email per user

### Week 3: Polish & Launch
- [ ] Email templates (Gmail SMTP)
- [ ] Frontend styling (Tailwind)
- [ ] Responsive design (mobile)
- [ ] Testing
  - [ ] Unit tests (Django)
  - [ ] E2E tests (Playwright - opcjonalnie)
  - [ ] Load testing
- [ ] Nginx SSL (Let's Encrypt)
- [ ] Deployment automation
- [ ] **Launch to first client!** 🚀

---

## Faza 2: Enhanced Features (1 miesiąc)

### Chatbot Integration
- [ ] Claude API setup
- [ ] Knowledge base (RAG)
  - [ ] Company info
  - [ ] Services descriptions
  - [ ] FAQ
- [ ] WebSocket for real-time chat
- [ ] Chat widget on website
- [ ] Conversation history (PostgreSQL)

### Dashboard Improvements
- [ ] Statistics (total offers, new today, etc.)
- [ ] Offer favorites (bookmark)
- [ ] Search & filters
- [ ] Export to CSV
- [ ] Email preferences (frequency, format)

### Multiple Sources
- [ ] OLX scraper (n8n workflow)
- [ ] Otodom scraper (n8n workflow)
- [ ] Facebook Groups monitor (Gmail trigger)
- [ ] Unified offers view

---

## Faza 3: Monetization (1-2 miesiące)

### Subscription Plans
- [ ] Database models (Plan, UserSubscription)
- [ ] Stripe integration
  - [ ] Payment form
  - [ ] Webhook handling
  - [ ] Invoice generation
- [ ] Plan limitations
  - [ ] Max locations per plan
  - [ ] Max sources per plan
  - [ ] Feature gates
- [ ] Upgrade/downgrade flow
- [ ] Billing dashboard

### Plans:
- **Basic** (49 PLN/mies): 1 location, 1 source, email alerts
- **Pro** (99 PLN/mies): 3 locations, 3 sources, email + SMS (przyszłość)
- **Business** (199 PLN/mies): 10 locations, all sources, API access

---

## Faza 4: Advanced Features (2-3 miesiące)

### AI-Powered Insights
- [ ] Offer scoring (Claude API)
  - [ ] Match score (0-100)
  - [ ] Price per m² analysis
  - [ ] Location scoring
- [ ] Smart recommendations
- [ ] Market trends analysis
- [ ] Price predictions (ML - przyszłość)

### Automation Marketplace
- [ ] Template workflows (pre-built)
  - [ ] Email marketing automation
  - [ ] Social media posting
  - [ ] Lead enrichment
  - [ ] Invoice processing
- [ ] One-click install
- [ ] Custom workflow builder (drag-and-drop)

### API for Developers
- [ ] REST API (DRF)
  - [ ] Authentication (JWT)
  - [ ] Endpoints: /offers, /config, /stats
  - [ ] Rate limiting
  - [ ] API keys management
- [ ] Webhooks (user-defined)
- [ ] SDK (Python, JavaScript)
- [ ] API documentation (Swagger)

---

## Faza 5: Scale & Optimize (3+ miesiące)

### Performance
- [ ] Redis caching
- [ ] Database query optimization
- [ ] CDN for static files (Cloudflare)
- [ ] Load balancer (if needed)
- [ ] PostgreSQL read replicas

### Monitoring & Analytics
- [ ] Sentry (error tracking)
- [ ] Prometheus + Grafana (metrics)
- [ ] User analytics (PostHog)
- [ ] Uptime monitoring
- [ ] Performance monitoring (APM)

### Team Features
- [ ] Multi-user accounts (Team plan)
- [ ] Role-based permissions
- [ ] Shared dashboards
- [ ] Team invitations
- [ ] Activity logs

### White-label (dla agencji)
- [ ] Custom branding
- [ ] Own domain
- [ ] Reseller program
- [ ] API dla agencji

---

## Faza 6: Expansion (6+ miesięcy)

### New Markets
- [ ] International markets (Germany, UK)
- [ ] Multi-language support (i18n)
- [ ] Multi-currency pricing
- [ ] Local payment methods

### Mobile Apps
- [ ] React Native app (iOS + Android)
- [ ] Push notifications
- [ ] Offline mode
- [ ] Mobile-first UI

### Integrations
- [ ] Zapier integration
- [ ] Make.com integration
- [ ] Slack bot
- [ ] Discord bot
- [ ] Telegram bot

### AI Agents Beyond Real Estate
- [ ] Job listings monitor
- [ ] E-commerce price tracking
- [ ] News aggregator
- [ ] Social media monitor
- [ ] Generic scraping tool

---

## Backlog Ideas (Someday/Maybe)

### Community
- [ ] User forum (comments on offers)
- [ ] Rating system
- [ ] Public profiles
- [ ] Marketplace for workflows

### Advanced AI
- [ ] Voice assistant (speech-to-text)
- [ ] Image analysis (photos from offers)
- [ ] Virtual tours integration
- [ ] 3D floor plans

### Business Intelligence
- [ ] Market reports (PDF generation)
- [ ] Investment calculator
- [ ] ROI predictions
- [ ] Heatmaps (best locations)

---

## Success Metrics

### MVP Success:
- [ ] 10 paying users
- [ ] 500+ offers monitored daily
- [ ] 95% uptime
- [ ] <3s page load time

### 6-Month Success:
- [ ] 50 paying users
- [ ] 10 000 PLN MRR (Monthly Recurring Revenue)
- [ ] 3 additional services launched
- [ ] 5-star reviews (average)

### 1-Year Success:
- [ ] 200+ paying users
- [ ] 50 000 PLN MRR
- [ ] Team of 2-3 people
- [ ] Break-even + profitable

---

## Current Sprint (Next 7 days)

**Priority: Django MVP**

### This Week Tasks:
1. [ ] Django project structure (Day 1)
2. [ ] Models: UserConfig, UserOffer (Day 1)
3. [ ] Django AllAuth setup (Day 2)
4. [ ] Landing page template (Day 2-3)
5. [ ] Gratka panel form + HTMX (Day 3-4)
6. [ ] Multi-user n8n workflow (Day 4-5)
7. [ ] Email integration (Gmail SMTP) (Day 5)
8. [ ] Testing + bug fixes (Day 6-7)
9. [ ] Deployment + SSL (Day 7)

**Goal: Wdrożenie pierwszego klienta do końca tygodnia!**

---

## Long-term Vision (2-3 lata)

**NexusLab = platforma no-code/low-code dla automatyzacji AI w Polsce**

- 1000+ paying users
- 500k PLN MRR
- 10-person team
- Recognized brand in automation space
- Exit opportunity or sustainable lifestyle business
