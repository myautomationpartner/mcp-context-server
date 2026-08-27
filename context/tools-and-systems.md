# Tools & Systems

Canonical live map: https://github.com/myautomationpartner/map-operating-system/blob/main/docs/LIVE.md

## Infrastructure
- Hetzner VPS, Coolify, Docker

## Core stack
- n8n (self-hosted at n8n.myautomationpartner.com)
- Supabase (zgkxrlednyovuytaejok)
- Cloudflare Pages, Workers, R2
- GitHub
- Chatwoot (inbox)
- Zernio (social)

## Data flow
Zernio → n8n → Supabase + R2
GitHub → Cloudflare Pages / Workers

## Dropped / not current
- Metricool (replaced by n8n + Zernio)
- Tidio (Chatwoot is the live inbox target)
- Dropbox as the target upload path (R2 is)
- Zite roles

## Not MAP
Delphi / Pacesetter tooling is a different company.

## Day job (not MAP)
Active Directory, Google Admin, firewalls, helpdesk
