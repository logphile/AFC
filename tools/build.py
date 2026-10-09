"""Builds the static pages for the AFC preview into the repo folder.
Shared header/footer live here so every page stays consistent."""
import pathlib, sys, hashlib

OUT = pathlib.Path(sys.argv[1])
# cache-buster: changes whenever the stylesheet or script changes
VER = hashlib.md5((OUT / "styles.css").read_bytes() + (OUT / "main.js").read_bytes()).hexdigest()[:8]
IMG = "https://e8usa8896fd.exactdn.com/wp-content/uploads"
LOGO = "images/logo-mark.svg"

ICON = {
 "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
 "cal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18M8 15h2M14 15h2"/></svg>',
 "file": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/></svg>',
 "spine": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="2" width="6" height="3.2" rx="1.2"/><rect x="8.5" y="6.6" width="7" height="3.2" rx="1.2"/><rect x="8" y="11.2" width="8" height="3.2" rx="1.2"/><rect x="8.5" y="15.8" width="7" height="3.2" rx="1.2"/><path d="M12 19v3"/></svg>',
 "needle": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20 15 9"/><path d="M14 4l6 6"/><path d="m13 7 4 4"/><circle cx="18.5" cy="5.5" r="2"/></svg>',
 "hand": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 11V6a2 2 0 0 0-4 0v1M14 10V4a2 2 0 0 0-4 0v2M10 10.5V6a2 2 0 0 0-4 0v8"/><path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.9-6-2.4l-3.6-3.6a2 2 0 0 1 2.8-2.8L7 15"/></svg>',
 "leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10z"/><path d="M2 21c0-3 1.9-5.4 5.1-6"/></svg>',
 "flag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><path d="M4 22v-7"/></svg>',
 "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
 "dl": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>',
}

OFFICES = {
 "hampton": dict(name="Hampton Office", phone="(757) 838-8820", tel="+17578388820",
   addr="1919 Commerce Dr., Suite 280<br>Hampton, VA 23666",
   q="1919+Commerce+Dr+Suite+280+Hampton+VA+23666",
   hours=[(0,"Sunday",None),(1,"Monday",None),(2,"Tuesday","9:30 am – 1 pm<br>3 pm – 7 pm"),(3,"Wednesday",None),
          (4,"Thursday","9:30 am – 1 pm<br>3 pm – 7 pm"),(5,"Friday","9:30 am – 1 pm<br>3 pm – 5 pm"),(6,"Saturday",None)]),
 "gloucester": dict(name="Gloucester Office", phone="(804) 832-6705", tel="+18048326705",
   addr="4856 George Washington Memorial Hwy.<br>Hayes, VA 23072",
   q="4856+George+Washington+Memorial+Hwy+Hayes+VA+23072",
   hours=[(0,"Sunday",None),(1,"Monday","9 am – 1 pm<br>3 pm – 5:30 pm"),(2,"Tuesday",None),(3,"Wednesday","10 am – 1 pm<br>3 pm – 5:30 pm"),
          (4,"Thursday",None),(5,"Friday",None),(6,"Saturday",None)]),
}

NAV = [("index.html","Home"),("services.html","Services"),("new-patients.html","New Patients"),
       ("about.html","About Us"),("locations.html","Locations &amp; Hours")]

def hours_table(key):
    rows = []
    for d, name, t in OFFICES[key]["hours"]:
        cell = t if t else '<span class="closed">Closed</span>'
        rows.append(f'<tr data-day="{d}"><th scope="row">{name}</th><td>{cell}</td></tr>')
    return f'<table class="hours"><caption class="skip">{OFFICES[key]["name"]} hours</caption>{"".join(rows)}</table>'

def office_card(key, big=False):
    o = OFFICES[key]
    return f'''
<article class="card office" id="{key}">
  <div class="office-map"><iframe title="Map of the {o["name"]}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
    src="https://maps.google.com/maps?q={o["q"]}&amp;z=15&amp;output=embed"></iframe></div>
  <div class="office-body">
    <div>
      <h3>{o["name"]}</h3>
      <p class="today-item" data-status="{key}" style="margin:0 0 10px"><span class="dot"></span><span class="status-text">Checking hours…</span></p>
      <a class="office-phone" href="tel:{o["tel"]}">{o["phone"]}</a>
      <address>{o["addr"]}</address>
    </div>
    {hours_table(key) if big else ""}
    <div class="office-actions">
      <a class="btn btn-primary" href="tel:{o["tel"]}">{ICON["phone"]} Call</a>
      <a class="btn btn-outline" href="https://www.google.com/maps/dir/?api=1&amp;destination={o["q"]}" target="_blank" rel="noopener">{ICON["pin"]} Directions</a>
    </div>
  </div>
</article>'''

def page(fname, title, desc, body):
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h==fname else ""}>{t}</a>' for h,t in NAV)
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- Preview site: keep out of search engines so it never competes with the live site. -->
<meta name="robots" content="noindex, nofollow">
<title>{title} · Abbott Family Chiropractic</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/svg+xml" href="{LOGO}">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&amp;family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css?v={VER}">
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<div class="preview-bar">Design preview — not the live website</div>
<header class="site-header">
  <div class="wrap header-row">
    <a class="brand" href="index.html">
      <img src="{LOGO}" alt="" width="52" height="56">
      <span><span class="brand-name">Abbott Family Chiropractic</span><span class="brand-sub">Hampton &amp; Gloucester, Virginia</span></span>
    </a>
    <button class="menu-btn" aria-expanded="false" aria-controls="site-nav">{ICON["menu"]}<span class="menu-label">Menu</span></button>
    <nav class="nav" id="site-nav" aria-label="Main">
      {links}
      <a class="btn btn-primary" href="appointments.html"{" aria-current=\"page\"" if fname=="appointments.html" else ""}>Book a Visit</a>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <h3>Abbott Family Chiropractic</h3>
        <p>Gentle, hands-on chiropractic, acupuncture, and massage for the whole family. Proudly serving Hampton, Newport News, Poquoson, Yorktown, Gloucester, and Hayes.</p>
      </div>
      <div>
        <h3>Hampton</h3>
        <address>1919 Commerce Dr., Suite 280<br>Hampton, VA 23666<br><a href="tel:+17578388820">(757) 838-8820</a></address>
      </div>
      <div>
        <h3>Gloucester</h3>
        <address>4856 George Washington Memorial Hwy.<br>Hayes, VA 23072<br><a href="tel:+18048326705">(804) 832-6705</a></address>
      </div>
      <div>
        <h3>Quick links</h3>
        <ul>
          <li><a href="appointments.html">Request an appointment</a></li>
          <li><a href="new-patients.html">New patient forms</a></li>
          <li><a href="https://www.facebook.com/abbottfamilychiropractic/" rel="noopener">Facebook</a></li>
          <li><a href="https://www.instagram.com/abbottfamilychiro/" rel="noopener">Instagram</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> Abbott Family Chiropractic</span>
      <span>Design preview</span>
    </div>
  </div>
</footer>
<nav class="callbar" aria-label="Call an office">
  <a href="tel:+17578388820">Call Hampton<small>(757) 838-8820</small></a>
  <a href="tel:+18048326705">Call Gloucester<small>(804) 832-6705</small></a>
</nav>
<script src="main.js?v={VER}"></script>
</body>
</html>
'''
    (OUT / fname).write_text(html, encoding="utf-8")

# ------------------------------------------------------------------ Home
page("index.html", "Welcome", "Family chiropractic, acupuncture, and massage in Hampton and Gloucester, Virginia.", f'''
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow">Hampton &amp; Gloucester, Virginia</span>
      <h1>Gentle, hands-on care for the whole family.</h1>
      <p class="lead">Chiropractic, acupuncture, and massage from a team that has cared for Hampton Roads families since 2006.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="appointments.html">{ICON["cal"]} Book a Visit</a>
        <a class="btn btn-outline" href="new-patients.html">{ICON["file"]} New Patient Forms</a>
      </div>
    </div>
    <div>
      <div class="hero-photo"><img src="{IMG}/2026/09/2026-staff-featured-c-1.jpg?strip=all" alt="The Abbott Family Chiropractic team"></div>
      <div class="hero-badge">{ICON["flag"].replace('<svg','<svg width="22" height="22"')}<span><strong>VA Community Care</strong> patients welcome</span></div>
    </div>
  </div>
</section>

<div class="today" aria-live="polite">
  <div class="wrap">
    <span class="today-label">Today · <span data-today-name></span></span>
    <span class="today-item" data-status="hampton"><span class="dot"></span><strong>Hampton:</strong>&nbsp;<span class="status-text">…</span></span>
    <span class="today-item" data-status="gloucester"><span class="dot"></span><strong>Gloucester:</strong>&nbsp;<span class="status-text">…</span></span>
  </div>
</div>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>Two offices, one family practice</h2>
      <p>Tap a phone number to call, or get turn-by-turn directions.</p>
    </div>
    <div class="grid-2">{office_card("hampton")}{office_card("gloucester")}</div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <h2>Your first visit, made easy</h2>
      <p>A little preparation means less time in the waiting room and more time with the doctor.</p>
    </div>
    <div class="steps">
      <div class="card step"><h3>Call or request a time</h3><p>Call either office, or <a href="appointments.html">send a request online</a> and we'll call you back to confirm.</p></div>
      <div class="card step"><h3>Fill out your forms at home</h3><p>Type into our <a href="new-patients.html">new patient forms</a> on your computer, then print them and bring them along. No printer? Come 15 minutes early.</p></div>
      <div class="card step"><h3>Come in and feel better</h3><p>Bring your forms, your ID, and your insurance or VA referral information.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>How we can help</h2>
      <p>Care that works together, under one roof.</p>
    </div>
    <div class="grid-3">
      <a class="card" href="services.html#chiropractic" style="text-decoration:none;color:inherit"><div class="icon">{ICON["spine"]}</div><h3>Chiropractic</h3><p>Gentle adjustments, including the low-force Activator method — no "bone cracking" required.</p></a>
      <a class="card" href="services.html#acupuncture" style="text-decoration:none;color:inherit"><div class="icon">{ICON["needle"]}</div><h3>Acupuncture</h3><p>A time-tested approach to easing pain and stress that pairs well with chiropractic care.</p></a>
      <a class="card" href="services.html#massage" style="text-decoration:none;color:inherit"><div class="icon">{ICON["hand"]}</div><h3>Massage Therapy</h3><p>Licensed therapists offering therapeutic, deep tissue, prenatal, and hot stone massage.</p></a>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head"><h2>What our patients say</h2></div>
    <div class="grid-3">
      <figure class="card quote" style="margin:0"><blockquote>Since seeing Dr. Conklyn my headaches have gone down to almost none. She keeps me in check so I can keep up with my crazy life.</blockquote><cite>Dawn H., Gloucester</cite></figure>
      <figure class="card quote" style="margin:0"><blockquote>My chiropractic care has given me the ability to move with less pain and stiffness. I've been able to exercise and stay active.</blockquote><cite>Karen M., Hampton</cite></figure>
      <figure class="card quote" style="margin:0"><blockquote>It is so nice to go to a doctor's office where you are treated respectfully and your time is as valuable as theirs.</blockquote><cite>Patient review</cite></figure>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="callout">
      <div>
        <h2>New to our office?</h2>
        <p>Welcome! Download your forms before your first visit and you'll be seen sooner.</p>
      </div>
      <div class="callout-actions">
        <a class="btn btn-light" href="new-patients.html">{ICON["file"]} Get New Patient Forms</a>
        <a class="btn btn-light" href="https://www.instagram.com/abbottfamilychiro/" rel="noopener">Follow us on Instagram</a>
      </div>
    </div>
  </div>
</section>
''')

# ------------------------------------------------------------------ New patients
def forms(prefix, items):
    lis = "".join(f'''<li><a href="forms/{url}" target="_blank" rel="noopener">
      <span class="fi">{ICON["dl"]}</span>
      <span><span class="ft">{t}{" <span class=\"tag\">Everyone</span>" if req else ""}</span><span class="fs">{s} · Fillable PDF</span></span></a></li>''' for t,s,url,req in items)
    return f'<ul class="form-list">{lis}</ul>'

H = [("Patient Information Sheet","Contact and insurance details","1_AFC_Hampton_PatientInformationSheet_fillable.pdf",True),
     ("Patient Case History","Your health history and what brings you in","2_AFC_Hampton_CaseHistory_fillable.pdf",True),
     ("Acupuncture Intake","Only if you're scheduled for acupuncture","AFC_Hampton_AcupunctureIntake_fillable.pdf",False),
     ("Massage Intake","Only if you're scheduled for massage","AFC_MassageIntake_fillable.pdf",False)]
G = [("Patient Information Sheet","Contact and insurance details","1_AFC_Gloucester_PatientInformationSheet_fillable.pdf",True),
     ("Patient Case History","Your health history and what brings you in","2_AFC_Gloucester_CaseHistory_fillable.pdf",True),
     ("Acupuncture Intake","Only if you're scheduled for acupuncture","AFC_Gloucester_AcupunctureIntake_fillable.pdf",False),
     ("Massage Intake","Only if you're scheduled for massage","AFC_MassageIntake_fillable.pdf",False)]

page("new-patients.html", "New Patients", "New patient forms for our Hampton and Gloucester offices.", f'''
<section class="page-head"><div class="wrap">
  <h1>Welcome, new patients</h1>
  <p>Filling out your forms before you arrive is the single best way to keep your first visit on time.</p>
</div></section>

<section class="section">
  <div class="wrap">
    <div class="steps" style="margin-bottom:48px">
      <div class="card step"><h3>Pick your office</h3><p>Each office has its own forms. Choose the one where you'll be seen.</p></div>
      <div class="card step"><h3>Type or print</h3><p>Everyone needs the first two forms. You can type right into them on a computer, then print. Or print them and fill them out by hand.</p></div>
      <div class="card step"><h3>Bring them with you</h3><p>Along with a photo ID and your insurance card or VA referral.</p></div>
    </div>
    <div class="grid-2">
      <div class="card"><h2 style="font-size:1.7rem">Hampton forms</h2>{forms("H", H)}</div>
      <div class="card"><h2 style="font-size:1.7rem">Gloucester forms</h2>{forms("G", G)}</div>
    </div>
    <p class="notice" style="margin-top:32px"><strong>No printer?</strong> No problem. Arrive 15 minutes early and we'll have copies ready for you at the front desk. Need help reading or filling out a form? Just ask — we're happy to help.</p>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap" style="max-width:820px">
    <h2>Coming through VA Community Care?</h2>
    <p>We're glad to care for our veterans. Please make sure the VA has approved your referral before your first visit, and have your referral or authorization information with you when you call us. It helps us get you scheduled faster.</p>
    <h2 style="margin-top:40px">Your right to a Good Faith Estimate</h2>
    <p>If you don't have insurance, or aren't using it for this visit, you have the right to receive a written estimate of the expected cost of your care before your appointment. You can ask for one when you schedule. If your bill is $400 or more above the estimate, you may dispute it — please keep a copy of your estimate. Learn more at <a href="https://www.cms.gov/nosurprises" rel="noopener">cms.gov/nosurprises</a>.</p>
  </div>
</section>
''')

# ------------------------------------------------------------------ Appointments
def choice(name, value, label, typ="radio", req=False):
    return f'<label class="choice"><input type="{typ}" name="{name}" value="{value}"{" required" if req else ""}> {label}</label>'

page("appointments.html", "Book a Visit", "Call or request an appointment at our Hampton or Gloucester office.", f'''
<section class="page-head"><div class="wrap">
  <h1>Book a visit</h1>
  <p>The fastest way is to call. If we're with patients or the office is closed, send us a request and we'll call you back.</p>
</div></section>

<section class="section">
  <div class="wrap">
    <div class="grid-2" style="margin-bottom:56px">
      <div class="card"><h3>Hampton Office</h3><p class="today-item" data-status="hampton"><span class="dot"></span><span class="status-text">…</span></p>
        <a class="btn btn-primary" style="width:100%" href="tel:+17578388820">{ICON["phone"]} Call (757) 838-8820</a></div>
      <div class="card"><h3>Gloucester Office</h3><p class="today-item" data-status="gloucester"><span class="dot"></span><span class="status-text">…</span></p>
        <a class="btn btn-primary" style="width:100%" href="tel:+18048326705">{ICON["phone"]} Call (804) 832-6705</a></div>
    </div>

    <div class="card" style="max-width:820px;margin-inline:auto;padding:36px">
      <h2>Request an appointment</h2>
      <p class="notice"><strong>Please don't include medical details here.</strong> We'll talk about what's going on when we call you, or at your visit.</p>
      <form class="form" id="appt-form" novalidate style="margin-top:24px">
        <div class="two-col">
          <div class="field"><label for="name">Your name</label><input id="name" name="name" type="text" autocomplete="name" required></div>
          <div class="field"><label for="phone">Phone number<span class="hint">We'll call you to confirm.</span></label><input id="phone" name="phone" type="tel" autocomplete="tel" required></div>
        </div>
        <fieldset class="field"><legend>Which office?</legend>
          <div class="choices">{choice("office","Hampton","Hampton",req=True)}{choice("office","Gloucester","Gloucester")}{choice("office","Either","Whichever is sooner")}</div></fieldset>
        <fieldset class="field"><legend>Have you been to our office before?</legend>
          <div class="choices">{choice("returning","new","No, I'm new",req=True)}{choice("returning","returning","Yes, I'm a returning patient")}</div></fieldset>
        <fieldset class="field"><legend>What kind of visit?</legend>
          <div class="choices">{choice("type","chiro","Chiropractic","checkbox")}{choice("type","acu","Acupuncture","checkbox")}{choice("type","massage","Massage","checkbox")}</div></fieldset>
        <fieldset class="field"><legend>Is this visit through VA Community Care?</legend>
          <div class="choices">{choice("va","yes","Yes")}{choice("va","no","No")}{choice("va","unsure","Not sure")}</div></fieldset>
        <fieldset class="field"><legend>Best time of day<span class="hint">Check all that work for you.</span></legend>
          <div class="choices">{choice("time","morning","Morning","checkbox")}{choice("time","midday","Around midday","checkbox")}{choice("time","afternoon","Afternoon / evening","checkbox")}</div></fieldset>
        <div class="field"><label for="days">Days that work best<span class="hint">For example: "Tuesdays or Thursdays after 3."</span></label><input id="days" name="days" type="text"></div>
        <button class="btn btn-primary" type="submit" style="justify-self:start">{ICON["cal"]} Send my request</button>
      </form>
      <div class="form-success notice" id="appt-success" tabindex="-1">
        <strong>Thank you — we got your request.</strong><br>Someone from our front desk will call you to confirm a time. (This is a design preview, so nothing was actually sent.)
      </div>
    </div>
  </div>
</section>
''')

# ------------------------------------------------------------------ Services
page("services.html", "Services", "Chiropractic, acupuncture, and massage therapy in Hampton and Gloucester.", f'''
<section class="page-head"><div class="wrap">
  <h1>Our services</h1>
  <p>Chiropractic, acupuncture, and massage — often most helpful when they work together.</p>
</div></section>

<section class="section" style="padding-top:24px">
  <div class="wrap">
    <div class="service" id="chiropractic">
      <div class="service-art">{ICON["spine"]}</div>
      <div><h2>Chiropractic</h2>
        <p>Chiropractic care focuses on the spine and nervous system to help your body move better and feel better. We tailor every adjustment to you — your age, your history, and your comfort.</p>
        <ul><li>Gentle, low-force <strong>Activator</strong> adjustments — no "cracking" required</li><li>Care for headaches, back and neck pain, and stiffness</li><li>Care for every age, from children to seniors</li></ul>
        <a class="btn btn-primary" href="appointments.html">{ICON["cal"]} Book chiropractic</a></div>
    </div>
    <div class="service" id="acupuncture">
      <div class="service-art">{ICON["needle"]}</div>
      <div><h2>Acupuncture</h2>
        <p>Acupuncture uses very fine needles at specific points to help relieve pain, ease tension, and support your body's natural healing. Many patients find it pairs well with their chiropractic care.</p>
        <p>New to acupuncture? Please fill out the <a href="new-patients.html">acupuncture intake form</a> before your visit.</p>
        <a class="btn btn-primary" href="appointments.html">{ICON["cal"]} Book acupuncture</a></div>
    </div>
    <div class="service" id="massage">
      <div class="service-art">{ICON["hand"]}</div>
      <div><h2>Massage therapy</h2>
        <p>Our licensed massage therapists help loosen tight muscles, improve range of motion, and support recovery between adjustments.</p>
        <ul><li>Therapeutic and deep tissue massage</li><li>Prenatal massage</li><li>Hot stone massage</li><li>Stretching and range-of-motion work</li></ul>
        <a class="btn btn-primary" href="appointments.html">{ICON["cal"]} Book a massage</a></div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head"><h2>Products we carry</h2><p>Ask us at your next visit which, if any, might be right for you.</p></div>
    <div class="grid-3">
      <div class="card"><div class="icon">{ICON["leaf"]}</div><h3>Standard Process</h3><p>Whole-food nutritional supplements, including MediHerb herbal formulas.</p></div>
      <div class="card"><div class="icon">{ICON["spine"]}</div><h3>Foot Levelers</h3><p>Custom-made orthotics that support your feet, knees, hips, and spine.</p></div>
      <div class="card"><div class="icon">{ICON["leaf"]}</div><h3>Young Living</h3><p>Essential oils available at both offices.</p></div>
    </div>
  </div>
</section>
''')

# ------------------------------------------------------------------ About
def person(initials, name, role, bio, photo=None):
    pic = (f'<img src="{IMG}/2018/12/{photo}?strip=all" alt="{name}" loading="lazy" onerror="this.remove()">' if photo else "")
    return f'''<div class="card person"><div class="avatar">{pic}<span aria-hidden="true">{initials}</span></div>
      <div><h3 style="margin-bottom:2px">{name}</h3><span class="role">{role}</span><p>{bio}</p></div></div>'''

page("about.html", "About Us", "Meet the team at Abbott Family Chiropractic.", f'''
<section class="page-head"><div class="wrap">
  <h1>About our practice</h1>
  <p>A family practice serving Hampton since 2006 and Gloucester since 2014.</p>
</div></section>

<section class="section">
  <div class="wrap" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:40px;align-items:center">
    <div class="hero-photo story-mark"><img src="{LOGO}" alt="Abbott Family Chiropractic emblem"></div>
    <div>
      <h2>Our story</h2>
      <p>Our practice opened its Hampton office in January 2006 and added a second office in Gloucester in 2014, so families on both sides of the York River could get care close to home.</p>
      <p>Dr. Conklyn first saw a chiropractor at age eight, and credits that care with keeping her healthy through years of competitive swimming. That experience is the heart of how we practice: chiropractic isn't only about pain — it's about helping your whole body work the way it should.</p>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head"><h2>Meet the team</h2></div>
    <div class="grid-2">
      {person("SC","Dr. Siobhan Conklyn","Chiropractor","Dr. Conklyn provides chiropractic and acupuncture care, with a gentle, respectful approach her patients often mention first.","siobhan-conklyn-2018.jpg")}
      {person("VR","Valeria Reynolds, LMT","Massage Therapist","With over ten years of experience, Valeria is trained in deep tissue, prenatal, and hot stone massage.","valeria-reynolds-2018.jpg")}
      {person("JT","John Tango, LMT","Massage Therapist","An Army National Guard veteran, John has been a board-certified massage therapist since 2012, focusing on therapeutic massage, stretching, and range of motion.","john-tango-2018.jpg")}
      {person("MG","Malinda Boyce-Good","Office Manager","Malinda brings a lifelong passion for natural wellness, informed by decades of independent study and mentorship in applied kinesiology.")}
    </div>
  </div>
</section>
''')

# ------------------------------------------------------------------ Locations
page("locations.html", "Locations & Hours", "Hours, maps, and directions for our Hampton and Gloucester offices.", f'''
<section class="page-head"><div class="wrap">
  <h1>Locations &amp; hours</h1>
  <p>Two offices serving Hampton, Newport News, Poquoson, Yorktown, Gloucester, and Hayes. Today is <strong data-today-name></strong> — today's hours are highlighted.</p>
</div></section>
<section class="section">
  <div class="wrap grid-2" style="align-items:start">{office_card("hampton", True)}{office_card("gloucester", True)}</div>
</section>
''')

print("built", sorted(p.name for p in OUT.glob("*.html")))
