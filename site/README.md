# SOS Venezuela — landing page

Single self-contained `index.html` (no build step, no dependencies). Spanish-first
with a progressive-enhancement EN toggle. Bot-first; surfcall credited underneath.
Built for the Build4Venezuela 2026 submission.

## Preview locally

```bash
python3 -m http.server 8080 --directory site
# open http://localhost:8080
```

## Deploy

**Vercel** (from repo root):
```bash
npx vercel --cwd site --prod
# or: set the Vercel project "Root Directory" to `site` in the dashboard
```

**Netlify**:
```bash
npx netlify deploy --dir=site --prod
```

Either gives you a URL like `https://<name>.vercel.app` — paste that into the
hackathon form's **PROJECT LINK**. Add a custom domain later in the dashboard if
you want (e.g. `sos.geckovision.tech` via a CNAME).

## Notes
- The Telegram CTA points at `https://t.me/DEV_VEZbot` — **the bot must be running**
  for the link to work end-to-end (the landing page is static; the bot is separate).
- No analytics, no trackers, no secrets — safe to host publicly (control-plane only).
- Edit copy in `index.html`: Spanish ships in the markup; English lives in the `EN`
  dictionary in the inline `<script>`. Keep the two in sync.
