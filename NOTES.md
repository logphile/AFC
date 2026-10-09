# Redesign notes

Reference notes for the Abbott Family Chiropractic redesign preview (October 2026).

## About this preview
- Plain HTML/CSS/JS, no build step, no WordPress. Hosted on GitHub Pages.
- Every page has `<meta name="robots" content="noindex, nofollow">` so it never competes with the live site in Google. Remove those tags only if this ever becomes the real site.
- Photos and PDFs are linked from the live site's image CDN (exactdn). If the live site goes away, copy them into an `images/` folder here.
- The logo slot uses the live site's favicon. Drop in a proper logo file (ideally SVG) from the 3D sign artwork.
- The appointment form is a demo: it shows a thank-you message but sends nothing.
- Office hours live in one place: the `HOURS` table at the top of `main.js`. The "Open now / Closed today" badges and the highlighted row in the hours tables all read from it.

## Design choices
- Colors: navy, slate, soft blue, white, to match the office sign.
- Fonts: Source Serif 4 for headings; Atkinson Hyperlegible for body text (designed by the Braille Institute for low-vision readers).
- 19px base text, 56px+ tap targets, no hover-only dropdown menus, visible focus outlines.
- On phones, a "Call Hampton / Call Gloucester" bar stays pinned to the bottom of the screen.
- Phone numbers are `tel:` links: on a phone they open the dialer with the number filled in.

## Things to confirm with her
- Team: only Dr. Conklyn, Valeria Reynolds, and John Tango are shown. The live staff page also lists Dr. Jason Abbott. Confirm the current roster and get current photos.
- Testimonials are from 2018. Embedding recent Google reviews would be more current.
- Facebook and Instagram links kept; the live site's LinkedIn link pointed to linkedin.com itself and was dropped.

## Pain points and options (researched Oct 2026)
**HIPAA is the constraint behind most of this.** Anything where patients type health information (intake forms, reason for visit, AI call transcripts) needs a vendor that signs a Business Associate Agreement (BAA). Free tiers essentially never include one; a plain Google Form cannot be made compliant.

- **Phone / AI receptionist:** Not free. HIPAA-ready options start around $29–49/month (e.g. Trillet $49/mo for 150 minutes; CloudTalk includes 50 free AI minutes then a paid add-on). Confirm a signed BAA directly. Best fit for her patients: after-hours and overflow only, staff answer during the day.
- **Appointments:** ChiroTouch's own online booking and digital intake (CT InForms / CTIntake) feed straight into ChiroTouch, which is the only option that removes work rather than moving it. Add-on cost. Generic free schedulers create double entry. VA Community Care visits need an approved referral regardless.
- **New patient forms:** Free now: convert the PDFs into fillable PDFs (type, then print or bring). Full fix: online intake into ChiroTouch. Cheapest standalone compliant form tool found: FormHippo, about $9/mo with a BAA on every plan (doesn't feed ChiroTouch).
- **News:** n8n can draft a post, wait for approval, then commit a Markdown file here; GitHub Pages republishes automatically. Keep the human approval step for health content. Zero-effort alternative: point to the Instagram she already posts to.
