#!/usr/bin/env python3
"""
FDE Website Builder.
Generates all pages from shared templates. Run after editing this file:
    python3 build.py
"""
import os, re

OUT = os.path.dirname(os.path.abspath(__file__))

# Hard rule: no em-dashes ever.
def ed_check(html):
    if "—" in html:
        bad = [i for i, c in enumerate(html) if c == "—"]
        raise AssertionError(f"Em-dash found at positions {bad[:5]}")
    return html

NAV_LINKS = [
    ("Home", "/"),
    ("About", "/about.html"),
    ("Services", "/services.html"),
    ("Portfolio", "/portfolio.html"),
    ("Reviews", "/reviews.html"),
    ("Blog", "/blog.html"),
    ("Contact", "/contact.html"),
]

def nav(active=""):
    links = ""
    for label, href in NAV_LINKS:
        cls = "active" if href == active or (active == "/" and href == "/") else ""
        links += f'<a href="{href}" class="{cls}">{label}</a>'
    return f'''<nav class="top" id="nav">
  <div class="container nav-inner">
    <a href="/" class="logo">
      <img src="/fde-logo.png" alt="Florida Demolition Experts" />
      <span class="logo-text">FDE</span>
    </a>
    <button class="nav-toggle" aria-label="Menu" onclick="document.querySelector('.nav-links').classList.toggle('open')">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
    <div class="nav-links">
      {links}
      <a href="/contact.html" class="nav-cta">Free On-Site Quote</a>
    </div>
  </div>
</nav>'''

FOOTER = '''<footer>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="/fde-logo.png" alt="Florida Demolition Experts" />
        <p>Woman-owned demolition contractor serving Boca Raton, Broward, and Palm Beach. Permit to push. Site swept clean. Every job.</p>
        <p class="license">Florida License #86-4496-D-X</p>
        <div class="social-links">
          <a href="https://www.instagram.com/floridademolitionexperts/" target="_blank" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg></a>
          <a href="https://www.tiktok.com/@florida.demolitio" target="_blank" rel="noopener" aria-label="TikTok"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5.8 20.1a6.34 6.34 0 0 0 10.86-4.43V9.01a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1.84-.44z"/></svg></a>
          <a href="https://www.youtube.com/@FloridaDemolitionExperts" target="_blank" rel="noopener" aria-label="YouTube"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z"/><polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"/></svg></a>
          <a href="https://www.facebook.com/profile.php?id=61574911868153" target="_blank" rel="noopener" aria-label="Facebook"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg></a>
        </div>
      </div>
      <div class="footer-col">
        <h5>Services</h5>
        <a href="/residential.html">Residential</a>
        <a href="/commercial.html">Commercial</a>
        <a href="/concrete-removal.html">Concrete Removal</a>
        <a href="/site-preparation.html">Site Preparation</a>
        <a href="/permits.html">Permits &amp; Planning</a>
        <a href="/emergency.html">Emergency Services</a>
      </div>
      <div class="footer-col">
        <h5>Company</h5>
        <a href="/about.html">About / Team</a>
        <a href="/portfolio.html">Portfolio</a>
        <a href="/reviews.html">Reviews</a>
        <a href="/blog.html">Blog</a>
        <a href="/contact.html">Contact</a>
      </div>
      <div class="footer-col">
        <h5>Contact</h5>
        <a href="tel:9544446643" style="color: var(--accent); font-weight: 600;">954-444-6643</a>
        <a href="mailto:nataliya@floridademolitionexperts.com">nataliya@floridademolitionexperts.com</a>
        <p style="color: var(--muted); font-size: 14px;">2505 NE 35 Dr<br>Fort Lauderdale, FL 33308</p>
        <p style="color: var(--muted); font-size: 14px;">Mon to Fri, 8 AM to 5 PM</p>
      </div>
    </div>
    <div class="footer-bottom">
      <div>&copy; 2026 Florida Demolition Experts. Woman-owned. South Florida.</div>
      <div>Site by Dotoli Digital</div>
    </div>
  </div>
</footer>
<a href="tel:9544446643" class="sticky-cta">Call 954-444-6643</a>
<script>
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  if (window.scrollY > 40) nav.classList.add('scrolled');
  else nav.classList.remove('scrolled');
});
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add('visible'); });
}, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
</script>
</body>
</html>'''

def head(title, desc, canonical=None):
    can = f'<link rel="canonical" href="{canonical}" />' if canonical else ''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:type" content="website" />
<link rel="icon" type="image/png" href="/fde-logo.png" />
{can}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
</head>
<body>'''

def page(filename, title, desc, body, active_nav, canonical=None):
    html = head(title, desc, canonical) + "\n" + nav(active_nav) + "\n" + body + "\n" + FOOTER
    html = ed_check(html)
    path = os.path.join(OUT, filename)
    with open(path, "w") as f:
        f.write(html)
    print(f"  wrote {filename:30s} {len(html):>6} chars")

# ============================================================
# CTA BLOCK (reused across many pages)
# ============================================================
CTA_BLOCK = '''<section id="contact" class="cta-section">
  <div class="container">
    <div class="cta-grid">
      <div class="reveal">
        <span class="section-eyebrow">Free Quote</span>
        <h2 class="section-title">Tell us about the job. <span class="italic-line">We will come walk it.</span></h2>
        <p class="section-sub">Every quote is on-site, not over the phone. We walk the property, mark the scope, and send you a real fixed price. No pressure. No surprises.</p>
        <div style="display:flex; align-items:center; gap:24px; padding-top: 24px; border-top: 1px solid var(--line);">
          <div>
            <div style="color: var(--muted); font-size: 12px; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 6px;">Or call directly</div>
            <a href="tel:9544446643" style="font-family: 'Space Grotesk'; font-size: 32px; font-weight: 600; color: var(--accent); text-decoration: none; letter-spacing: -0.02em;">954-444-6643</a>
          </div>
        </div>
      </div>
      <div class="cta-form-card reveal">
        <h3>Request your on-site quote</h3>
        <p class="sub">Same-day callback. Quote walk usually within 48 hours.</p>
        <form onsubmit="event.preventDefault(); alert('Thanks. We will call you within one business day at the number provided.'); this.reset();">
          <div class="form-field"><label for="name">Full name</label><input id="name" name="name" type="text" required placeholder="Your name" /></div>
          <div class="form-field"><label for="phone">Phone</label><input id="phone" name="phone" type="tel" required placeholder="Phone number" /></div>
          <div class="form-field"><label for="address">Property address</label><input id="address" name="address" type="text" required placeholder="Street, city, ZIP" /></div>
          <div class="form-field"><label for="type">Job type</label>
            <select id="type" name="type">
              <option>Residential demolition</option>
              <option>Commercial demolition</option>
              <option>Concrete removal</option>
              <option>Site preparation</option>
              <option>Pool removal</option>
              <option>Permits only</option>
              <option>Emergency / disaster response</option>
              <option>Not sure yet</option>
            </select>
          </div>
          <div class="form-field"><label for="notes">Notes (optional)</label><textarea id="notes" name="notes" placeholder="Anything we should know before the walk-through"></textarea></div>
          <button type="submit" class="form-submit">Request my free quote</button>
        </form>
      </div>
    </div>
  </div>
</section>'''

# ============================================================
# CHECK ICON helper (SVG)
# ============================================================
CHK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>'
ARROW = '<svg style="width:16px;height:16px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'

# ============================================================
# PAGES
# ============================================================

# HOMEPAGE
home_body = '''<section class="hero hero-tall">
  <div class="hero-grid"></div>
  <div class="container hero-content">
    <div class="hero-eyebrow"><span class="dot"></span>Booking July &amp; August now &middot; South Florida</div>
    <h1>Demolition done <span class="italic-line">right.</span><br>The <span class="accent">first time.</span></h1>
    <p class="hero-sub">Woman-owned. South Florida. We pull every permit, sweep every site, and answer every call. The team general contractors keep on speed dial.</p>
    <div class="hero-ctas">
      <a href="/contact.html" class="btn-primary">Free On-Site Quote ''' + ARROW + '''</a>
      <a href="tel:9544446643" class="btn-secondary"><svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>954-444-6643</a>
    </div>
  </div>
</section>

<div class="trust-bar">
  <div class="container trust-inner">
    <div class="trust-item">''' + CHK + '''Page 1 on Google</div>
    <span class="trust-divider"></span>
    <div class="trust-item">''' + CHK + '''Woman-Owned</div>
    <span class="trust-divider"></span>
    <div class="trust-item">''' + CHK + '''Licensed &amp; Insured</div>
    <span class="trust-divider"></span>
    <div class="trust-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>Boca &middot; Broward &middot; Palm Beach</div>
  </div>
</div>

<section id="why">
  <div class="container">
    <div class="reveal">
      <span class="section-eyebrow">Why FDE</span>
      <h2 class="section-title">Four things every demo crew should do.<br><span class="italic-line">Most do not.</span></h2>
    </div>
    <div class="why-grid" style="margin-top: 64px;">
      <div class="why-card reveal">
        <div class="why-icon"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="15" x2="15" y2="15"/></svg></div>
        <h3>Permit to Push</h3>
        <p>Demolition permit. Asbestos clearance. Utility disconnects. Final close-out. Most demo crews hand you a quote and disappear. We file every form and text you when each one closes.</p>
      </div>
      <div class="why-card reveal">
        <div class="why-icon"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg></div>
        <h3>The FDE Five</h3>
        <p>Walk, mark, disconnect, drop, sort. A five-step playbook on every job. The reason GCs keep calling us back: the next trade walks onto a site that is ready, not a mess.</p>
      </div>
      <div class="why-card reveal">
        <div class="why-icon"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></div>
        <h3>Page 1 on Google</h3>
        <p>When South Florida property owners search demolition contractor, they find us on the first page. That ranking is earned, not bought. It is also why the right kind of clients keep calling.</p>
      </div>
      <div class="why-card reveal">
        <div class="why-icon"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></div>
        <h3>Founder-Run</h3>
        <p>Nataliya runs every job. The owner is on every quote, on every site, and on the phone when something goes sideways. Not a call center. Not a subcontractor. Her.</p>
      </div>
    </div>
  </div>
</section>

<section id="process" class="process-section">
  <div class="container">
    <div class="reveal">
      <span class="section-eyebrow">The Process</span>
      <h2 class="section-title">The FDE Five.</h2>
      <p class="section-sub">Every demolition follows the same five steps. The drop is the part everyone wants to film. It is also ten percent of the job.</p>
    </div>
    <div class="process-grid">
      <div class="process-step reveal"><div class="step-number">01</div><h4>Walk</h4><p>Map every utility, every load-bearing wall, every salvage piece.</p></div>
      <div class="process-step reveal"><div class="step-number">02</div><h4>Mark</h4><p>Spray every line. Stake every boundary. Photograph for the file.</p></div>
      <div class="process-step reveal"><div class="step-number">03</div><h4>Disconnect</h4><p>Power, gas, water, sewer. Each one shut off by the right authority.</p></div>
      <div class="process-step reveal"><div class="step-number">04</div><h4>Drop</h4><p>The visible part. Controlled, dust-managed, neighbor-aware.</p></div>
      <div class="process-step reveal"><div class="step-number">05</div><h4>Sort</h4><p>Concrete, metal, wood, separated for recycling. Site swept clean.</p></div>
    </div>
    <div class="process-note reveal" style="margin-top: 36px;">
      <strong>Need it build-ready?</strong> Site grading and earthwork to your target elevation is our paid upsell. Ask for a combined quote.
    </div>
  </div>
</section>

<section id="services">
  <div class="container">
    <div class="reveal">
      <span class="section-eyebrow">Services</span>
      <h2 class="section-title">Every demolition need.<br><span class="italic-line">One in-house crew.</span></h2>
    </div>
    <div class="services-grid" style="margin-top: 64px;">
      <div class="service-card reveal">
        <h3>Residential</h3>
        <p>Full tear-down, interior gut, pool removal. Permit to push, every job.</p>
        <ul class="service-list">
          <li>''' + CHK + '''Full house tear-down</li>
          <li>''' + CHK + '''Interior demo (kitchen, bath, gut)</li>
          <li>''' + CHK + '''Pool removal &amp; back-fill</li>
          <li>''' + CHK + '''Garage &amp; outbuilding removal</li>
        </ul>
        <a href="/residential.html" class="service-cta">Residential details ''' + ARROW + '''</a>
      </div>
      <div class="service-card reveal">
        <h3>Commercial</h3>
        <p>Strip-outs, full structures, partial demo. Built for GC schedules.</p>
        <ul class="service-list">
          <li>''' + CHK + '''Commercial structure removal</li>
          <li>''' + CHK + '''Retail &amp; office strip-out</li>
          <li>''' + CHK + '''Partial &amp; selective demo</li>
          <li>''' + CHK + '''GC partnership &amp; schedule-fit</li>
        </ul>
        <a href="/commercial.html" class="service-cta">Commercial details ''' + ARROW + '''</a>
      </div>
      <div class="service-card featured reveal">
        <span class="service-tag">Premium</span>
        <h3>Earthwork</h3>
        <p>Grading and demucking after demo. Doubles the value of your lot before the next crew shows up.</p>
        <ul class="service-list">
          <li>''' + CHK + '''Site grading to target elevation</li>
          <li>''' + CHK + '''Demucking &amp; soil correction</li>
          <li>''' + CHK + '''Build-ready lot prep</li>
          <li>''' + CHK + '''Bundled with demolition pricing</li>
        </ul>
        <a href="/site-preparation.html" class="service-cta">Earthwork details ''' + ARROW + '''</a>
      </div>
    </div>
    <div style="text-align: center; margin-top: 48px;">
      <a href="/services.html" class="btn-secondary">View all services ''' + ARROW + '''</a>
    </div>
  </div>
</section>

<section id="founder" style="background: var(--surface); border-top: 1px solid var(--line); border-bottom: 1px solid var(--line);">
  <div class="container">
    <div class="founder-grid">
      <div class="founder-image reveal">
        <div class="placeholder-text">[ Founder photo placeholder &middot; replace with Nataliya headshot from Kalvin shoot ]</div>
        <div class="founder-image-overlay"></div>
        <div class="founder-image-text">
          <div class="name">Nataliya Shkurat</div>
          <div class="role">Founder, Florida Demolition Experts</div>
        </div>
      </div>
      <div class="reveal">
        <span class="section-eyebrow">The Founder</span>
        <p class="founder-quote">I am <span class="highlight">not the cheapest</span> demolition company in Florida.<br>I am the one you call when you want it done right the first time.</p>
        <p class="founder-bio">Two years ago I was running this company off a single truck and a flip phone. Today, FDE comes up on page one of Google for the demolition searches that matter in South Florida, and I am pricing in a second excavator and an earthwork crew I never thought I could afford this fast.</p>
        <p class="founder-bio">What changed is not the work. The work was always good. What changed is the systems behind it. Every permit pulled. Every site swept. Every call answered. That is why the same builders keep coming back.</p>
        <div class="founder-signature">
          <div><div class="sig-name">Nataliya Shkurat</div><div class="sig-title">Founder &amp; Owner</div></div>
        </div>
      </div>
    </div>
  </div>
</section>

<div class="stats-strip">
  <div class="container">
    <div class="stats-grid">
      <div class="stat reveal"><div class="stat-number">38</div><div class="stat-label">Signed jobs</div></div>
      <div class="stat reveal"><div class="stat-number">Page 1</div><div class="stat-label">Google rankings</div></div>
      <div class="stat reveal"><div class="stat-number">2 yrs</div><div class="stat-label">Building FDE</div></div>
      <div class="stat reveal"><div class="stat-number">3 counties</div><div class="stat-label">Boca, Broward, Palm Beach</div></div>
    </div>
  </div>
</div>

<section>
  <div class="container">
    <div class="testimonial reveal">
      <p class="testimonial-quote">Before I found Nataliya, I had been burned by demo crews who would leave a mess and disappear. Now every demolition job I quote, every interior tear-out I do not want to do myself, I just call her. That is it.</p>
      <div class="testimonial-attribution"><strong>General Contractor</strong>Repeat client &middot; South Florida</div>
    </div>
  </div>
</section>
''' + CTA_BLOCK

page("index.html",
     "Florida Demolition Experts | Woman-Owned Demolition Contractor in South Florida",
     "Woman-owned demolition contractor serving Boca Raton, Broward, and Palm Beach. We pull every permit, sweep every site. Free on-site quote: 954-444-6643.",
     home_body, "/")

# ============================================================
# ABOUT
# ============================================================
about_body = '''<section class="page-header">
  <div class="container">
    <div class="crumb"><a href="/">Home</a><span class="sep">/</span><span>About</span></div>
    <h1 style="font-family:'Space Grotesk'; font-size: clamp(40px,5.5vw,72px); font-weight: 600; line-height: 1.05; letter-spacing: -0.03em; max-width: 900px;">Two years.<br>One truck to <span style="color: var(--accent);">page one of Google.</span></h1>
    <p style="color: var(--muted); font-size: 18px; max-width: 600px; margin-top: 24px; line-height: 1.6;">A woman-owned demolition company built in South Florida, on the back of one rule: do it right the first time.</p>
  </div>
</section>

<section style="padding-top: 0;">
  <div class="container">
    <div class="two-col">
      <div class="two-col-text reveal">
        <span class="section-eyebrow">Our Story</span>
        <h2>Breaking barriers. Building futures.</h2>
        <p>Florida Demolition Experts was founded by Nataliya Shkurat with one excavator, one truck, and one belief: that demolition done right is not about how hard you can hit. It is about what you leave behind.</p>
        <p>Two years later, we are the demolition crew general contractors call first. Not because we are the cheapest. Because we pull every permit, run every disconnect, and sweep every site so the next trade walks in on schedule.</p>
        <p>We are licensed, insured, and woman-owned. Every quote is on-site, not over the phone. Every job follows the same five-step playbook. And every call gets answered by someone who knows the property by name.</p>
      </div>
      <div class="image-block reveal">[ Team photo placeholder &middot; on-site crew + Nataliya ]</div>
    </div>
  </div>
</section>

<section class="process-section">
  <div class="container">
    <div class="reveal">
      <span class="section-eyebrow">What We Stand For</span>
      <h2 class="section-title">Four non-negotiables.</h2>
    </div>
    <div class="why-grid" style="margin-top: 64px;">
      <div class="why-card reveal">
        <div class="why-icon"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 12l2 2 4-4"/><circle cx="12" cy="12" r="10"/></svg></div>
        <h3>Permit-first</h3>
        <p>No job starts without paperwork. We file, you stay legal, the timeline holds.</p>
      </div>
      <div class="why-card reveal">
        <div class="why-icon"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div>
        <h3>On schedule</h3>
        <p>We tell you the day. We start on the day. We finish on the day.</p>
      </div>
      <div class="why-card reveal">
        <div class="why-icon"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg></div>
        <h3>Site swept clean</h3>
        <p>Concrete, metal, wood, sorted for recycling. Lot ready for the next crew.</p>
      </div>
      <div class="why-card reveal">
        <div class="why-icon"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg></div>
        <h3>Real phone, real founder</h3>
        <p>When you call 954-444-6643, you reach a real person on the team. Most days, Nataliya.</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="founder-grid">
      <div class="founder-image reveal">
        <div class="placeholder-text">[ Nataliya headshot placeholder ]</div>
        <div class="founder-image-overlay"></div>
        <div class="founder-image-text">
          <div class="name">Nataliya Shkurat</div>
          <div class="role">Founder &amp; Owner</div>
        </div>
      </div>
      <div class="reveal">
        <span class="section-eyebrow">Meet the Founder</span>
        <p class="founder-quote">I built this company because I watched too many owners get burned by the <span class="highlight">cheapest bid.</span></p>
        <p class="founder-bio">Nataliya Shkurat founded Florida Demolition Experts in 2024. In two years she has grown FDE from a single-truck operation into one of the most-searched demolition contractors in South Florida.</p>
        <p class="founder-bio">She runs every quote walk, signs off on every permit, and answers the phone when a GC calls at 7 AM with a problem. The crew has grown. The standard has not.</p>
      </div>
    </div>
  </div>
</section>
''' + CTA_BLOCK

page("about.html",
     "About Florida Demolition Experts | Woman-Owned Demolition in South Florida",
     "Florida Demolition Experts is a woman-owned demolition contractor founded by Nataliya Shkurat. Two years from one truck to page one of Google in South Florida.",
     about_body, "/about.html")

# ============================================================
# SERVICES OVERVIEW
# ============================================================
services_body = '''<section class="page-header">
  <div class="container">
    <div class="crumb"><a href="/">Home</a><span class="sep">/</span><span>Services</span></div>
    <h1 style="font-family:'Space Grotesk'; font-size: clamp(40px,5.5vw,72px); font-weight: 600; line-height: 1.05; letter-spacing: -0.03em; max-width: 900px;">Every demolition need.<br><span style="color: var(--accent);">One in-house crew.</span></h1>
    <p style="color: var(--muted); font-size: 18px; max-width: 600px; margin-top: 24px; line-height: 1.6;">From a single interior tear-out to a full commercial structure, the same five-step playbook applies. Permit to push, every job.</p>
  </div>
</section>

<section style="padding-top: 0;">
  <div class="container">
    <div class="services-grid">
      <div class="service-card reveal">
        <h3>Residential Demolition</h3>
        <p>Full houses, interior gut-outs, garages, pools. Built for homeowners, GCs, and developers.</p>
        <ul class="service-list">
          <li>''' + CHK + '''Full single-family tear-down</li>
          <li>''' + CHK + '''Interior demo (kitchen, bath, full gut)</li>
          <li>''' + CHK + '''Pool removal &amp; back-fill</li>
          <li>''' + CHK + '''Garage &amp; outbuilding removal</li>
        </ul>
        <a href="/residential.html" class="service-cta">View residential ''' + ARROW + '''</a>
      </div>
      <div class="service-card reveal">
        <h3>Commercial Demolition</h3>
        <p>Office, retail, warehouse, industrial. Selective strip-outs and full structures, on the GC schedule.</p>
        <ul class="service-list">
          <li>''' + CHK + '''Full commercial tear-down</li>
          <li>''' + CHK + '''Retail strip-out</li>
          <li>''' + CHK + '''Office &amp; tenant fit-out demo</li>
          <li>''' + CHK + '''Warehouse &amp; industrial</li>
        </ul>
        <a href="/commercial.html" class="service-cta">View commercial ''' + ARROW + '''</a>
      </div>
      <div class="service-card reveal">
        <h3>Concrete Removal</h3>
        <p>Driveways, slabs, foundations, sidewalks, pool decks. Sawcut, break, haul, recycle.</p>
        <ul class="service-list">
          <li>''' + CHK + '''Driveways &amp; sidewalks</li>
          <li>''' + CHK + '''Slab &amp; foundation removal</li>
          <li>''' + CHK + '''Pool deck &amp; patio</li>
          <li>''' + CHK + '''Concrete recycling</li>
        </ul>
        <a href="/concrete-removal.html" class="service-cta">View concrete ''' + ARROW + '''</a>
      </div>
      <div class="service-card featured reveal">
        <span class="service-tag">Premium</span>
        <h3>Site Preparation</h3>
        <p>Land clearing, grading, demucking, excavation. Build-ready lot in one combined contract.</p>
        <ul class="service-list">
          <li>''' + CHK + '''Land clearing &amp; brush removal</li>
          <li>''' + CHK + '''Site grading &amp; cut/fill</li>
          <li>''' + CHK + '''Demucking &amp; soil correction</li>
          <li>''' + CHK + '''Bundled with demolition</li>
        </ul>
        <a href="/site-preparation.html" class="service-cta">View site prep ''' + ARROW + '''</a>
      </div>
      <div class="service-card reveal">
        <h3>Permits &amp; Planning</h3>
        <p>Six to eight weeks of paperwork that you never have to touch. Quoted as its own line item.</p>
        <ul class="service-list">
          <li>''' + CHK + '''Demolition permit filing</li>
          <li>''' + CHK + '''Asbestos clearance survey</li>
          <li>''' + CHK + '''Utility shut-off coordination</li>
          <li>''' + CHK + '''Final close-out inspection</li>
        </ul>
        <a href="/permits.html" class="service-cta">View permits ''' + ARROW + '''</a>
      </div>
      <div class="service-card reveal">
        <h3>Emergency Services</h3>
        <p>Storm damage. Fire response. Unsafe structures. Same-day site visit, fast remediation.</p>
        <ul class="service-list">
          <li>''' + CHK + '''Storm &amp; hurricane damage</li>
          <li>''' + CHK + '''Fire-damaged structure</li>
          <li>''' + CHK + '''Unsafe / collapsed structures</li>
          <li>''' + CHK + '''24-hour callback</li>
        </ul>
        <a href="/emergency.html" class="service-cta">View emergency ''' + ARROW + '''</a>
      </div>
    </div>

    <div style="margin-top: 80px; padding-top: 60px; border-top: 1px solid var(--line);">
      <div class="reveal">
        <span class="section-eyebrow">Also In-House</span>
        <h2 class="section-title" style="font-size: clamp(28px,3.5vw,42px);">Recycling, salvage, and subcontractor coordination.</h2>
        <p class="section-sub">Every job ends with concrete, metal, and wood sorted for recycling. And when your project needs another trade, we coordinate directly so you do not have to.</p>
      </div>
    </div>
  </div>
</section>
''' + CTA_BLOCK

page("services.html",
     "Demolition Services | Florida Demolition Experts",
     "Residential, commercial, concrete removal, site preparation, permits, and emergency demolition across Boca Raton, Broward, and Palm Beach.",
     services_body, "/services.html")

# ============================================================
# SERVICE PAGE BUILDER (reusable)
# ============================================================
def service_page(filename, page_title, hero_h1, hero_h1_accent, hero_sub,
                 lead_h2, lead_p, bullets, side_image_caption, faqs=None):
    bullets_html = "\n".join([f'<li>{b}</li>' for b in bullets])
    faqs_html = ""
    if faqs:
        items = "\n".join([f'<details class="faq-item"><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs])
        faqs_html = f'''<section class="process-section">
  <div class="container">
    <div class="reveal" style="text-align: center; max-width: 700px; margin: 0 auto 64px;">
      <span class="section-eyebrow">Common Questions</span>
      <h2 class="section-title" style="margin: 0 auto;">FAQ</h2>
    </div>
    <div class="faq-list">{items}</div>
  </div>
</section>'''

    body = f'''<section class="page-header">
  <div class="container">
    <div class="crumb"><a href="/">Home</a><span class="sep">/</span><a href="/services.html">Services</a><span class="sep">/</span><span>{page_title}</span></div>
    <h1 style="font-family:'Space Grotesk'; font-size: clamp(40px,5.5vw,72px); font-weight: 600; line-height: 1.05; letter-spacing: -0.03em; max-width: 900px;">{hero_h1}<br><span style="color: var(--accent);">{hero_h1_accent}</span></h1>
    <p style="color: var(--muted); font-size: 18px; max-width: 600px; margin-top: 24px; line-height: 1.6;">{hero_sub}</p>
    <div style="margin-top: 32px;"><a href="/contact.html" class="btn-primary">Free On-Site Quote {ARROW}</a></div>
  </div>
</section>

<section style="padding-top: 0;">
  <div class="container">
    <div class="two-col">
      <div class="two-col-text reveal">
        <span class="section-eyebrow">What We Do</span>
        <h2>{lead_h2}</h2>
        <p>{lead_p}</p>
        <ul>{bullets_html}</ul>
        <a href="/contact.html" class="btn-primary">Get a quote {ARROW}</a>
      </div>
      <div class="image-block reveal">[ {side_image_caption} ]</div>
    </div>
  </div>
</section>

{faqs_html}
''' + CTA_BLOCK
    page(filename, f"{page_title} | Florida Demolition Experts",
         f"{page_title} from Florida Demolition Experts in Boca Raton, Broward, and Palm Beach. Licensed, insured, woman-owned. Call 954-444-6643.",
         body, "/services.html")


# RESIDENTIAL
service_page(
    "residential.html",
    "Residential Demolition",
    "Residential demolition,",
    "done to the inch.",
    "Houses, interiors, pools, garages. Permit to push, site swept clean, every job.",
    "From single rooms to full tear-downs.",
    "Residential demolition is the bulk of what we do in South Florida. Single-family tear-downs for developers and homeowners. Kitchen and bathroom gut-outs for remodelers. Pool removals with back-fill so the lot is build-ready. Garage and outbuilding removal as add-ons or standalones. Every project follows the same five-step playbook, with permits pulled before we lift a hammer.",
    [
        "Single-family home tear-down (any era, any size)",
        "Interior gut-outs (kitchen, bath, full interior)",
        "Pool removal with structural back-fill",
        "Garage, shed, and outbuilding removal",
        "Asbestos and lead survey coordination",
        "Same five-step playbook from walk to site-swept",
    ],
    "Residential tear-down in progress",
    [
        ("How long does a residential demolition take?",
         "The demo itself is usually one to two days. The paperwork that legally lets us start (permits, asbestos clearance, utility disconnects) typically takes six to eight weeks. We file it all and text you when each step closes."),
        ("Do I need to be on site during the demolition?",
         "No. We document everything with photos before, during, and after. You will get a final walk-through video when the site is swept clean."),
        ("What about the pool? Can you fill it in?",
         "Yes. We break out the pool shell, structural back-fill with compacted clean fill, and grade the surface to your target elevation. Quoted as one combined service."),
        ("Will my insurance cover any damage?",
         "Most homeowners policies will not cover damage from unpermitted work. With FDE, every permit is pulled, every disconnect is authorized, and we carry full liability insurance throughout the job."),
    ]
)

# COMMERCIAL
service_page(
    "commercial.html",
    "Commercial Demolition",
    "Commercial demolition,",
    "on the GC's schedule.",
    "Office, retail, warehouse, industrial. Selective strip-outs and full structures with permits closed before the next trade arrives.",
    "Built to fit the general contractor's timeline.",
    "Commercial demolition rewards crews that show up on the day, finish on the day, and leave the site ready for the next trade. That is the bar we hit. Office tear-outs for tenant fit-outs. Retail strip-outs between leases. Full warehouse and industrial structures with selective demolition where load-bearing elements stay. Every job comes with a real foreman on site, daily progress reports, and an end-of-day swept condition.",
    [
        "Full commercial structure removal",
        "Retail and office strip-outs between tenants",
        "Selective and partial demolition",
        "Warehouse, industrial, and mixed-use",
        "GC-friendly scheduling and daily reports",
        "Coordination with electrical, plumbing, and structural trades",
    ],
    "Commercial strip-out underway",
    [
        ("Can you work nights or weekends to fit our schedule?",
         "Yes. For commercial jobs where business hours matter, we run after-hours and weekend crews at a scheduled premium. Quoted up front."),
        ("Do you handle asbestos and other hazmat?",
         "We coordinate the certified asbestos abatement subcontractor and pull the survey ourselves. You get one point of contact, one combined invoice."),
        ("How do you protect adjacent tenants and properties?",
         "Dust suppression, scaffolded barriers, and noise scheduling are built into the quote. We walk the boundary with you before day one."),
        ("Will you provide daily progress updates?",
         "Yes. The site foreman sends a daily photo + status to the GC and the owner. You always know where the job stands."),
    ]
)

# CONCRETE REMOVAL
service_page(
    "concrete-removal.html",
    "Concrete Removal",
    "Concrete removal,",
    "without the mess.",
    "Driveways, slabs, foundations, pool decks. Saw-cut clean, broken out, hauled, and recycled.",
    "Clean cuts, clean removal, clean lot.",
    "Concrete removal is more than swinging a hammer. We saw-cut clean edges so adjacent surfaces stay intact, break out the slab with controlled equipment, and haul every piece off-site to a recycling facility. Whether it is a single residential driveway or a full commercial parking lot, the approach is the same: protect what stays, remove what goes, leave the site sweep-clean.",
    [
        "Driveway and sidewalk removal",
        "Slab and foundation demolition",
        "Pool deck and patio removal",
        "Concrete saw-cutting for partial removals",
        "Commercial parking lot tear-out",
        "Concrete recycling at certified facility",
    ],
    "Saw-cut driveway removal in progress",
    [
        ("How much concrete can you remove in a day?",
         "A typical residential driveway (600 to 1,000 sq ft) comes out in one day including haul-off. Larger commercial jobs scale with crew size."),
        ("Will my landscaping or adjacent slabs be damaged?",
         "Saw-cut edges and controlled breaking prevent collateral damage. We protect adjacent landscaping with plywood and tarps before the equipment moves in."),
        ("Do you recycle the concrete?",
         "Yes. All concrete is hauled to a certified recycling facility where it is crushed for road base and aggregate. You get a recycling receipt with your final invoice."),
        ("Can you remove the concrete and then prep the area for new pour?",
         "Yes. Removal, sub-base prep, and grading can be quoted as one combined service. Bundle saves time and money."),
    ]
)

# SITE PREPARATION
service_page(
    "site-preparation.html",
    "Site Preparation &amp; Earthwork",
    "Build-ready lot,",
    "in one contract.",
    "Land clearing, grading, demucking, excavation. Bundled with demolition so the next crew starts on a level surface.",
    "Demolition is half the work. Site prep is the other half.",
    "Site preparation is what separates a cleared lot from a build-ready lot. We clear brush and vegetation, demuck soft soil, cut and fill to your target elevation, and grade the final surface. Quoted as our paid earthwork upsell, but priced as a bundle when combined with demolition. Doubles the value of the lot before the foundation crew shows up.",
    [
        "Land clearing and brush removal",
        "Site grading to target elevation",
        "Cut and fill earthwork",
        "Demucking and soft-soil correction",
        "Excavation for foundations and utilities",
        "Build-ready surface for the next crew",
    ],
    "Excavator grading a cleared lot",
    [
        ("Is site prep included in the demolition quote?",
         "No. Site preparation is a separate service that we offer as a paid upsell. It is priced as a bundle when combined with demolition. Ask for a combined quote."),
        ("How do you determine target elevation?",
         "We work from your site plan or surveyor stakes. If you do not have one yet, we can recommend a local surveyor and coordinate directly."),
        ("What is demucking?",
         "South Florida soil sometimes contains organic muck that cannot support structural loads. Demucking removes that layer and replaces it with engineered fill. We test, remove, and re-compact in one trip."),
        ("Can you handle the entire pre-construction package?",
         "Yes. Demolition, clearing, grading, and excavation in one contract, one crew, one schedule. That is the point of having it all in-house."),
    ]
)

# PERMITS
service_page(
    "permits.html",
    "Permits &amp; Planning",
    "Six to eight weeks of paperwork.",
    "Zero on you.",
    "Demolition permit, asbestos clearance, utility shut-off, final close-out. Four filings, three agencies, one person chasing all of it. That person is us.",
    "Most demolition crews hand you a quote and disappear.",
    "Permit coordination is the work nobody else wants to do, and it is the reason most demolition timelines blow up. We file the demolition permit. We schedule the asbestos clearance survey. We coordinate the utility shut-offs with the right authority. We submit the final close-out inspection. Quoted as its own line item on every estimate so you can opt out if you really want to handle it yourself. Most clients do not.",
    [
        "Demolition permit filing with the right county",
        "Asbestos clearance survey coordination",
        "Utility shut-off (power, gas, water, sewer)",
        "Final close-out inspection submission",
        "Text updates when each step closes",
        "Separate line item on every quote",
    ],
    "Stamped demolition permit on tailgate",
    [
        ("Why does this take six to eight weeks?",
         "Permit review at the county, asbestos lab turnaround, and utility scheduling are all sequential. We file the day you sign, but the agencies set the pace. The good news: you do not have to chase any of it."),
        ("What if I want to pull the permit myself to save money?",
         "You can. It is quoted as its own line item so you can opt out. Most owners try it once and call us back for the next job."),
        ("Do you handle asbestos abatement too?",
         "We coordinate the certified abatement subcontractor and pull the survey. You get one point of contact, one timeline, one combined quote."),
        ("What happens if my project does not need a permit?",
         "Some interior tear-outs and small structures qualify for permit-exempt status. We confirm with the local building department before we tell you either way."),
    ]
)

# EMERGENCY
service_page(
    "emergency.html",
    "Emergency Demolition",
    "Storm damage. Fire damage.",
    "Unsafe structures.",
    "Same-day site visit. Fast remediation. Insurance-friendly documentation from the first photo to the final invoice.",
    "When the structure cannot wait.",
    "Emergency demolition is for the situations you did not plan for. Hurricane damage that needs to be cleared before the insurance adjuster arrives. A fire-damaged structure that needs to come down before the city issues a citation. A partially collapsed building that puts neighbors at risk. We respond with same-day site visits, document everything for your insurance carrier, and execute fast safe removal.",
    [
        "Storm and hurricane damage response",
        "Fire-damaged structure removal",
        "Partial collapse / unsafe structure",
        "Insurance-friendly photo documentation",
        "Same-day site visit, 24-hour callback",
        "Coordination with adjusters and inspectors",
    ],
    "Storm-damaged structure being cleared",
    [
        ("How fast can you respond?",
         "Same-day site visit for true emergencies. Removal typically starts within 24 to 72 hours depending on permits and insurance coordination."),
        ("Will you work with my insurance carrier?",
         "Yes. We document everything from the initial walk-through and send the package directly to your adjuster if you authorize it. We have worked with most major Florida carriers."),
        ("What if the structure is partially collapsed?",
         "We bring a structural-aware crew with shoring equipment and controlled-collapse experience. Safety of adjacent properties and people is the first call we make."),
        ("Is emergency demo more expensive?",
         "There is an expedited-response premium for same-day mobilization. We tell you up front before any work starts. No surprise invoicing after the fact."),
    ]
)

# ============================================================
# PORTFOLIO
# ============================================================
portfolio_body = '''<section class="page-header">
  <div class="container">
    <div class="crumb"><a href="/">Home</a><span class="sep">/</span><span>Portfolio</span></div>
    <h1 style="font-family:'Space Grotesk'; font-size: clamp(40px,5.5vw,72px); font-weight: 600; line-height: 1.05; letter-spacing: -0.03em; max-width: 900px;">Selected work<br><span style="color: var(--accent);">across South Florida.</span></h1>
    <p style="color: var(--muted); font-size: 18px; max-width: 600px; margin-top: 24px; line-height: 1.6;">A small sample of recent demolition, concrete, and site-preparation jobs. Most clients prefer privacy, so addresses are abbreviated.</p>
  </div>
</section>

<section style="padding-top: 0;">
  <div class="container">
    <div class="portfolio-grid">
      <div class="portfolio-card reveal"><div class="portfolio-thumb">[ Before / After photo ]</div><div class="portfolio-card-body"><div class="meta">Residential &middot; 3,200 sq ft</div><h4>Full Home Tear-Down</h4><p>Boca Raton. Single-family demolition, pool removal, site graded for new build. 6 hours on site.</p></div></div>
      <div class="portfolio-card reveal"><div class="portfolio-thumb">[ Before / After photo ]</div><div class="portfolio-card-body"><div class="meta">Commercial &middot; Strip-out</div><h4>Retail Tenant Fit-Out</h4><p>Fort Lauderdale. After-hours strip-out for a new tenant. Walls, ceilings, fixtures gone in 4 nights.</p></div></div>
      <div class="portfolio-card reveal"><div class="portfolio-thumb">[ Before / After photo ]</div><div class="portfolio-card-body"><div class="meta">Residential &middot; Interior gut</div><h4>Whole-House Interior</h4><p>Hollywood. Full interior tear-out to studs for remodel. Salvaged fixtures preserved per owner request.</p></div></div>
      <div class="portfolio-card reveal"><div class="portfolio-thumb">[ Before / After photo ]</div><div class="portfolio-card-body"><div class="meta">Concrete &middot; 1,400 sq ft</div><h4>Driveway &amp; Pool Deck</h4><p>Pompano Beach. Saw-cut driveway and old pool deck, recycled at certified facility.</p></div></div>
      <div class="portfolio-card reveal"><div class="portfolio-thumb">[ Before / After photo ]</div><div class="portfolio-card-body"><div class="meta">Site Prep &middot; Build-ready</div><h4>Lot Clear + Grade</h4><p>Coral Springs. Land clearing, demucking, grading to target elevation for new construction.</p></div></div>
      <div class="portfolio-card reveal"><div class="portfolio-thumb">[ Before / After photo ]</div><div class="portfolio-card-body"><div class="meta">Emergency &middot; Storm</div><h4>Hurricane Damage Removal</h4><p>Delray Beach. Damaged structure cleared for insurance assessment within 48 hours of call.</p></div></div>
      <div class="portfolio-card reveal"><div class="portfolio-thumb">[ Before / After photo ]</div><div class="portfolio-card-body"><div class="meta">Residential &middot; Pool</div><h4>Pool Removal &amp; Fill</h4><p>Plantation. Old in-ground pool broken out, structural back-fill, lot ready for landscaping.</p></div></div>
      <div class="portfolio-card reveal"><div class="portfolio-thumb">[ Before / After photo ]</div><div class="portfolio-card-body"><div class="meta">Commercial &middot; Warehouse</div><h4>Industrial Strip-Out</h4><p>Davie. Selective demo inside an active warehouse. Production never stopped.</p></div></div>
      <div class="portfolio-card reveal"><div class="portfolio-thumb">[ Before / After photo ]</div><div class="portfolio-card-body"><div class="meta">Concrete &middot; Foundation</div><h4>Slab &amp; Foundation</h4><p>Sunrise. Full residential slab removal, broken out and hauled in one day.</p></div></div>
    </div>
    <div style="text-align: center; margin-top: 64px; color: var(--muted); font-size: 14px;">Portfolio thumbnails are placeholders. Replace with real before / after photos from project files.</div>
  </div>
</section>
''' + CTA_BLOCK

page("portfolio.html",
     "Portfolio | Florida Demolition Experts",
     "Selected demolition, concrete, and site-preparation projects across Boca Raton, Broward, Palm Beach, and South Florida.",
     portfolio_body, "/portfolio.html")

# ============================================================
# REVIEWS
# ============================================================
reviews_body = '''<section class="page-header">
  <div class="container">
    <div class="crumb"><a href="/">Home</a><span class="sep">/</span><span>Reviews</span></div>
    <h1 style="font-family:'Space Grotesk'; font-size: clamp(40px,5.5vw,72px); font-weight: 600; line-height: 1.05; letter-spacing: -0.03em; max-width: 900px;">What clients<br><span style="color: var(--accent);">actually say.</span></h1>
    <p style="color: var(--muted); font-size: 18px; max-width: 600px; margin-top: 24px; line-height: 1.6;">Most reviews here come from general contractors, developers, and homeowners we have worked with more than once.</p>
  </div>
</section>

<section style="padding-top: 0;">
  <div class="container">
    <div class="testimonial-grid">
      <div class="testimonial-card reveal">
        <div class="stars">&starf;&starf;&starf;&starf;&starf;</div>
        <p class="quote">Before I found Nataliya, I had been burned by demo crews who would leave a mess and disappear. Now every demolition job I quote, every interior tear-out, I just call her.</p>
        <div class="author"><strong>General Contractor</strong>Repeat client &middot; South Florida</div>
      </div>
      <div class="testimonial-card reveal">
        <div class="stars">&starf;&starf;&starf;&starf;&starf;</div>
        <p class="quote">They pulled every permit. Showed up on the day. Finished early. My foundation crew started on schedule for the first time in years.</p>
        <div class="author"><strong>Developer</strong>Boca Raton</div>
      </div>
      <div class="testimonial-card reveal">
        <div class="stars">&starf;&starf;&starf;&starf;&starf;</div>
        <p class="quote">We had hurricane damage and needed it cleared in 48 hours for the insurance walk. FDE was on site the next morning. Documented everything.</p>
        <div class="author"><strong>Homeowner</strong>Fort Lauderdale</div>
      </div>
      <div class="testimonial-card reveal">
        <div class="stars">&starf;&starf;&starf;&starf;&starf;</div>
        <p class="quote">Got three quotes. Nataliya was not the cheapest. She was the only one who came out and walked the property before pricing it. We hired her on the spot.</p>
        <div class="author"><strong>Homeowner</strong>Hollywood</div>
      </div>
      <div class="testimonial-card reveal">
        <div class="stars">&starf;&starf;&starf;&starf;&starf;</div>
        <p class="quote">Full commercial strip-out, after hours, for a tenant turnover. The next trade walked in to a swept site. Will use again.</p>
        <div class="author"><strong>Property Manager</strong>Fort Lauderdale</div>
      </div>
      <div class="testimonial-card reveal">
        <div class="stars">&starf;&starf;&starf;&starf;&starf;</div>
        <p class="quote">The permit coordination alone was worth the price. I had no idea how much paperwork was involved until FDE took it off my plate.</p>
        <div class="author"><strong>Homeowner</strong>Palm Beach</div>
      </div>
    </div>

    <div style="text-align: center; margin-top: 80px; padding: 48px; background: var(--surface); border: 1px solid var(--line); border-radius: 24px;">
      <h3 style="font-family: 'Space Grotesk'; font-size: 28px; font-weight: 600; margin-bottom: 12px; letter-spacing: -0.02em;">Worked with us recently?</h3>
      <p style="color: var(--muted); margin-bottom: 24px;">Leave a Google review. It helps the next homeowner find a real demolition crew.</p>
      <a href="https://g.page/r/" target="_blank" rel="noopener" class="btn-primary">Leave a Google review ''' + ARROW + '''</a>
    </div>
  </div>
</section>
''' + CTA_BLOCK

page("reviews.html",
     "Reviews | Florida Demolition Experts",
     "What clients say about working with Florida Demolition Experts. Real reviews from general contractors, developers, and homeowners across South Florida.",
     reviews_body, "/reviews.html")

# ============================================================
# BLOG
# ============================================================
blog_body = '''<section class="page-header">
  <div class="container">
    <div class="crumb"><a href="/">Home</a><span class="sep">/</span><span>Blog</span></div>
    <h1 style="font-family:'Space Grotesk'; font-size: clamp(40px,5.5vw,72px); font-weight: 600; line-height: 1.05; letter-spacing: -0.03em; max-width: 900px;">Field notes from<br><span style="color: var(--accent);">South Florida demolition.</span></h1>
    <p style="color: var(--muted); font-size: 18px; max-width: 600px; margin-top: 24px; line-height: 1.6;">What we learn on site. What every homeowner and GC should know before they sign a demo contract.</p>
  </div>
</section>

<section style="padding-top: 0;">
  <div class="container">
    <div class="portfolio-grid">
      <div class="portfolio-card reveal"><div class="portfolio-thumb">[ Article cover ]</div><div class="portfolio-card-body"><div class="meta">Permits &middot; 6 min read</div><h4>4 filings, 3 agencies, 1 person chasing it</h4><p>What actually happens between signing a demolition contract and the first hammer hitting the wall.</p></div></div>
      <div class="portfolio-card reveal"><div class="portfolio-thumb">[ Article cover ]</div><div class="portfolio-card-body"><div class="meta">Safety &middot; 5 min read</div><h4>Three things your cheap demo guy is hiding</h4><p>Fines, asbestos, insurance gaps. The risks the lowest bid does not include.</p></div></div>
      <div class="portfolio-card reveal"><div class="portfolio-thumb">[ Article cover ]</div><div class="portfolio-card-body"><div class="meta">Process &middot; 4 min read</div><h4>The FDE Five: how every job runs</h4><p>Walk, mark, disconnect, drop, sort. The same five steps on every project, every time.</p></div></div>
      <div class="portfolio-card reveal"><div class="portfolio-thumb">[ Article cover ]</div><div class="portfolio-card-body"><div class="meta">Cost &middot; 7 min read</div><h4>What demolition actually costs in South Florida</h4><p>A breakdown of the real cost drivers: size, permits, asbestos, haul-off, site prep.</p></div></div>
      <div class="portfolio-card reveal"><div class="portfolio-thumb">[ Article cover ]</div><div class="portfolio-card-body"><div class="meta">GC &middot; 6 min read</div><h4>Why general contractors keep calling us back</h4><p>The next trade walking onto a clean site is the only metric that matters.</p></div></div>
      <div class="portfolio-card reveal"><div class="portfolio-thumb">[ Article cover ]</div><div class="portfolio-card-body"><div class="meta">Pool &middot; 5 min read</div><h4>Should you remove the pool or convert it?</h4><p>When a pool removal makes the lot more valuable, and when it does not.</p></div></div>
    </div>
    <div style="text-align: center; margin-top: 64px; color: var(--muted); font-size: 14px;">Blog articles coming soon. Subscribe via the contact form to be notified.</div>
  </div>
</section>
''' + CTA_BLOCK

page("blog.html",
     "Blog | Florida Demolition Experts",
     "Field notes from the FDE crew. What every homeowner and general contractor should know before signing a demolition contract.",
     blog_body, "/blog.html")

# ============================================================
# CONTACT
# ============================================================
contact_body = '''<section class="page-header">
  <div class="container">
    <div class="crumb"><a href="/">Home</a><span class="sep">/</span><span>Contact</span></div>
    <h1 style="font-family:'Space Grotesk'; font-size: clamp(40px,5.5vw,72px); font-weight: 600; line-height: 1.05; letter-spacing: -0.03em; max-width: 900px;">Tell us about the job.<br><span style="color: var(--accent);">We will come walk it.</span></h1>
    <p style="color: var(--muted); font-size: 18px; max-width: 600px; margin-top: 24px; line-height: 1.6;">Every quote is on-site, not over the phone. Same-day callback. Quote walk usually within 48 hours.</p>
  </div>
</section>

<section style="padding-top: 0;">
  <div class="container">
    <div class="cta-grid">
      <div class="reveal">
        <span class="section-eyebrow">Get In Touch</span>
        <h2 style="font-family: 'Space Grotesk'; font-size: clamp(32px,4vw,48px); font-weight: 600; line-height: 1.1; letter-spacing: -0.02em; margin-bottom: 32px;">Three ways to reach Nataliya.</h2>

        <div style="margin-bottom: 28px;">
          <div style="color: var(--muted); font-size: 12px; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 8px;">Phone (fastest)</div>
          <a href="tel:9544446643" style="font-family: 'Space Grotesk'; font-size: 32px; font-weight: 600; color: var(--accent); letter-spacing: -0.02em;">954-444-6643</a>
        </div>

        <div style="margin-bottom: 28px;">
          <div style="color: var(--muted); font-size: 12px; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 8px;">Email</div>
          <a href="mailto:nataliya@floridademolitionexperts.com" style="font-family: 'Space Grotesk'; font-size: 18px; font-weight: 500; color: var(--text);">nataliya@floridademolitionexperts.com</a>
        </div>

        <div style="margin-bottom: 28px;">
          <div style="color: var(--muted); font-size: 12px; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 8px;">Office</div>
          <div style="font-family: 'Space Grotesk'; font-size: 18px; font-weight: 500;">2505 NE 35 Dr<br>Fort Lauderdale, FL 33308</div>
        </div>

        <div style="padding-top: 24px; border-top: 1px solid var(--line);">
          <div style="color: var(--muted); font-size: 12px; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 8px;">Hours</div>
          <div style="color: var(--text); font-size: 16px;">Monday to Friday, 8 AM to 5 PM</div>
          <div style="color: var(--muted); font-size: 14px; margin-top: 4px;">Emergency response available 24/7. Call the main number.</div>
        </div>
      </div>

      <div class="cta-form-card reveal">
        <h3>Request your on-site quote</h3>
        <p class="sub">Same-day callback. Quote walk usually within 48 hours.</p>
        <form onsubmit="event.preventDefault(); alert('Thanks. We will call you within one business day at the number provided.'); this.reset();">
          <div class="form-field"><label for="name">Full name</label><input id="name" name="name" type="text" required placeholder="Your name" /></div>
          <div class="form-field"><label for="phone">Phone</label><input id="phone" name="phone" type="tel" required placeholder="Phone number" /></div>
          <div class="form-field"><label for="email">Email (optional)</label><input id="email" name="email" type="email" placeholder="you@email.com" /></div>
          <div class="form-field"><label for="address">Property address</label><input id="address" name="address" type="text" required placeholder="Street, city, ZIP" /></div>
          <div class="form-field"><label for="type">Job type</label>
            <select id="type" name="type">
              <option>Residential demolition</option>
              <option>Commercial demolition</option>
              <option>Concrete removal</option>
              <option>Site preparation / earthwork</option>
              <option>Pool removal</option>
              <option>Permits only</option>
              <option>Emergency / disaster response</option>
              <option>Not sure yet</option>
            </select>
          </div>
          <div class="form-field"><label for="notes">Notes (optional)</label><textarea id="notes" name="notes" placeholder="Anything we should know before the walk-through"></textarea></div>
          <button type="submit" class="form-submit">Request my free quote</button>
        </form>
      </div>
    </div>
  </div>
</section>

<section class="process-section" style="padding: 80px 0;">
  <div class="container" style="text-align: center;">
    <span class="section-eyebrow">Service Area</span>
    <h2 class="section-title" style="margin: 0 auto 24px;">South Florida.</h2>
    <p style="color: var(--muted); font-size: 17px; max-width: 600px; margin: 0 auto;">Boca Raton, Broward County, and Palm Beach. If your project is in South Florida, we can quote it.</p>
  </div>
</section>'''

page("contact.html",
     "Contact | Florida Demolition Experts",
     "Call 954-444-6643 or email nataliya@floridademolitionexperts.com for a free on-site demolition quote in Boca Raton, Broward, and Palm Beach.",
     contact_body, "/contact.html")


print("\nDone. All pages built and em-dash free.")
