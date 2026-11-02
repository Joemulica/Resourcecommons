# Resource Commons static site generator.
# Edit EVENTS below, then run: python3 build.py  -> writes ./site (upload to GitHub) and ./preview
import os, html, shutil

SITE = "Resource Commons"
EVENTS = [
 dict(slug="summer-opportunity-fair", key="summer", name="Summer Opportunity Fair", month="Feb", mnum=2,
   when="Planned for late February 2027", where="Northern Westchester", hue="summer",
   tagline="Day camps, sleepaway camps, classes and teen summer programs, all in one room.",
   audience="Families with kids from preschool through high school who are planning the summer.",
   zones=[("Little Kids","Day camps and half-day programs"),("Big Kids","Sleepaway, specialty and sports camps"),("Teen Zone","Counselor-in-training spots, summer jobs, pre-college and volunteering")],
   exhibitors=["Day camps","Sleepaway camps","Sports camps","Arts and music programs","STEM camps","Teen jobs and CIT programs","Pre-college programs","Swim schools"],
   talks=["How to choose a sleepaway camp","Your teen's first summer job","Ten-minute camp demos on the stage"],
   prices=[("Standard table","$750","$650 early bird"),("Premium table (corner or near the stage)","$1,000",""),("Stage demo slot, 10 minutes","$250","Add-on")]),
 dict(slug="special-needs-resource-day", key="specialneeds", name="Special Needs Resource Day", month="Apr", mnum=4,
   when="Planned for April 2027", where="Westchester, fully accessible venue", hue="sn",
   tagline="Schools, therapists, evaluators and advocates for families of kids with IEPs, 504 plans and different learning needs.",
   audience="Parents and caregivers of children with disabilities or learning differences, plus the educators who support them.",
   zones=[("Schools and programs","Special education schools, inclusive camps and after-school programs"),("Therapies","Speech, OT, PT, ABA and mental health providers"),("Planning and advocacy","Advocates, evaluators, special needs planners and attorneys")],
   exhibitors=["Special education schools","Speech and occupational therapists","Evaluators","Educational advocates","Inclusive camps","Special needs attorneys","Financial planners","Nonprofits and support groups"],
   talks=["Understanding your child's IEP","Getting an evaluation: where to start","Planning for the transition to adulthood"],
   prices=[("Standard table","$950",""),("Nonprofit table","Free or discounted","Limited, apply early")]),
 dict(slug="fall-activities-fair", key="fall", name="Fall Activities Fair", month="Sep", mnum=9,
   when="Planned for September 2027", where="Northern Westchester", hue="fall",
   tagline="After-school classes, sports leagues, music lessons and tutoring for the school year.",
   audience="Families of school-age kids looking for what to do after the bell.",
   zones=[("Move","Sports leagues, martial arts, dance and gymnastics"),("Make","Art, music, theater and STEM classes"),("Learn","Tutoring, test prep and language programs")],
   exhibitors=["Sports leagues","Martial arts","Dance studios","Music lessons","Art classes","Theater programs","Tutoring centers","Language schools"],
   talks=["Finding the right after-school balance","Try-it demos from local instructors"],
   prices=[("Standard table","$600","")]),
 dict(slug="first-steps-preschool-fair", key="preschool", name="First Steps Preschool Fair", month="Oct", mnum=10,
   when="Planned for October 2027, ahead of fall tours and pre-K deadlines", where="Northern Westchester", hue="pre",
   tagline="Preschools, daycares, pre-K options and early childhood resources for families with kids ages 0 to 6.",
   audience="Parents of babies, toddlers and preschoolers deciding on care, preschool and kindergarten.",
   zones=[("Schools","Preschools, nursery schools, daycares, Montessori and pre-K providers"),("Enrichment","Swim, gymnastics, music and art for little kids"),("Family services","Pediatric dentists, nanny agencies, financial and estate planning")],
   exhibitors=["Preschools","Daycares","Montessori schools","Pre-K providers","Swim schools","Toddler music and art","Speech and OT providers","Family planning services"],
   talks=["Play-based or academic preschool?","How pre-K works in your district","Is my child ready for kindergarten?","Early intervention: what to watch for"],
   prices=[("School table","$400",""),("Enrichment table","$500",""),("Family services table","$750","")]),
 dict(slug="caring-for-aging-parents", key="aging", name="Caring for Aging Parents Resource Day", month="Nov", mnum=11,
   when="Planned for November 2027", where="Westchester", hue="aging",
   tagline="Home care, senior living, elder law and planning help for adult children caring for a parent.",
   audience="Adult children, usually 45 to 65, who are starting to make care decisions for a parent.",
   zones=[("Care at home","Home care agencies, adult day programs and care managers"),("Senior living","Independent living, assisted living and memory care"),("Legal and money","Elder law attorneys, Medicaid planning and financial planners")],
   exhibitors=["Home care agencies","Assisted living communities","Memory care","Geriatric care managers","Elder law attorneys","Financial planners","Adult day programs","Caregiver support groups"],
   talks=["Having the conversation with your parent","Paying for care: Medicare, Medicaid and long-term care","When home isn't safe anymore"],
   prices=[("Standard table","$1,300","")]),
]
CODES = {"summer":"SOF27","specialneeds":"SNR27","fall":"FAF27","preschool":"FSP27","aging":"CAP27"}
GUIDES = {
 "summer": ("Westchester Summer Camp Guide", "Day and sleepaway camps side by side: ages, hours, cost ranges, transportation and sign-up deadlines."),
 "specialneeds": ("Special Needs Resource Guide", "Schools, therapists, evaluators and advocates in and near Westchester, plus a plain-English IEP and 504 primer."),
 "fall": ("Fall Activities Guide", "After-school classes, leagues, lessons and tutoring by town, age and day of the week."),
 "preschool": ("Preschool & Pre-K Guide", "Preschools and daycares compared on hours, philosophy and tuition range, with district pre-K timelines."),
 "aging": ("Caring for Aging Parents Guide", "Home care, senior living, elder law and Medicaid basics, with a checklist for the first family conversation."),
}
GUIDE_PRICE = "$15"
BUNDLE_PRICE = "$49"
TERMS = [
 "Your table is confirmed once payment clears. You'll get a receipt and confirmation by email.",
 "Paying by bank transfer (ACH) at checkout is preferred. It keeps table prices low.",
 "Full refund until 30 days before the fair. After that, tables can move to another fair but aren't refunded.",
 "If the fair is canceled for weather, your table moves to the snow date or you get a full refund.",
]
for _x in EVENTS: _x["code"] = CODES[_x["key"]]
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
e = html.escape

def head(title, desc, full=True):
    meta = f'''<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Geist:wght@400;500;600&display=swap">
<link rel="stylesheet" href="style.css">'''
    if full:
        return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{meta}
</head>
<body>'''
    return meta

def tail(full=True):
    s = '<script src="config.js"></script>\n<script src="site.js"></script>'
    return s + ("\n</body>\n</html>\n" if full else "\n")

def nav(active=""):
    links = "".join(f'<a href="{x}.html"{" aria-current=\"page\"" if active==x else ""}>{t}</a>' for x,t in [("index","Fairs"),("families","Families"),("guides","Guides"),("exhibit","Exhibit")])
    return f'''<header class="top"><div class="wrap top-in">
<a class="brand" href="index.html"><span class="mark" aria-hidden="true"></span>Resource Commons</a>
<nav class="nav">{links}<a class="btn small" href="families.html#signup">Get updates</a></nav>
</div></header>'''

def footer():
    return f'''<footer class="foot"><div class="wrap foot-in">
<div><a class="brand" href="index.html"><span class="mark" aria-hidden="true"></span>Resource Commons</a>
<p>Family resource fairs in Westchester, New York. Free for families.</p></div>
<div class="foot-links">{"".join(f'<a href="{x["slug"]}.html">{e(x["name"])}</a>' for x in EVENTS)}<a href="exhibit.html">Exhibit or sponsor</a><a href="guides.html">Resource guides</a></div>
</div></footer>'''

def yearstrip(current=None):
    by = {x["mnum"]: x for x in EVENTS}
    cells = []
    for i,m in enumerate(MONTHS, start=1):
        x = by.get(i)
        if x:
            cur = ' aria-current="true"' if current == x["key"] else ''
            cells.append(f'<a class="mo has {x["hue"]}" href="{x["slug"]}.html" title="{e(x["name"])}"{cur}><span class="pt"></span><span class="mo-l">{m}</span></a>')
        else:
            cells.append(f'<span class="mo"><span class="pt"></span><span class="mo-l">{m}</span></span>')
    return f'<div class="year" aria-label="Fair calendar">{"".join(cells)}</div>'

def home(full=True):
    tiles = "".join(f'''<a class="tile {x["hue"]}{" feat" if i==0 else ""}" href="{x["slug"]}.html">
<span class="tile-top"><span class="tile-m">{x["month"]}</span><span class="pill">{"Next up" if i==0 else "Planned"}</span></span>
<span class="tile-n">{e(x["name"])}</span>
<span class="tile-t">{e(x["tagline"])}</span>
<span class="tile-f"><span>{e(x["when"].split(",")[0].replace("Planned for ",""))}</span><span class="arrow" aria-hidden="true">→</span></span></a>''' for i,x in enumerate(EVENTS))
    body = f'''{nav("index")}
<main>
<section class="hero"><div class="wrap">
<p class="eyebrow"><span class="live" aria-hidden="true"></span>Westchester, NY · Free for families</p>
<h1>Every option your family is weighing. <span class="hl">One room.</span></h1>
<p class="lede">Camps, schools, therapists, care providers and local services set up a table. You walk in, ask your questions and leave with real answers.</p>
<div class="cta"><a class="btn" href="#fairs">See the fairs</a><a class="btn ghost" href="exhibit.html">Exhibit at a fair</a></div>
{yearstrip()}
</div></section>
<section class="band" id="fairs"><div class="wrap">
<div class="sec-h"><h2>Five fairs, one for each big decision.</h2><p>Each one lands in the season when families are actually choosing.</p></div>
<div class="bento">{tiles}<a class="tile ink" href="exhibit.html">
<span class="tile-top"><span class="tile-m">+</span><span class="pill">For businesses</span></span>
<span class="tile-n">Put your table in front of local families</span>
<span class="tile-t">Camps, schools, practices and services can exhibit at one fair or all five.</span>
<span class="tile-f"><span>Exhibitor info</span><span class="arrow" aria-hidden="true">→</span></span></a></div>
</div></section>
<section class="band"><div class="wrap">
<div class="sec-h"><h2>How a fair works</h2></div>
<div class="three cards">
<div><span class="ic" aria-hidden="true">$0</span><h3>Free for families</h3><p>RSVP to get the exhibitor list and talk schedule ahead of time. Bring the kids. There's a play area so you can actually talk.</p></div>
<div><span class="ic" aria-hidden="true">1×</span><h3>No ten-of-the-same tables</h3><p>We cap each category, so you meet a real range of local options.</p></div>
<div><span class="ic" aria-hidden="true">15′</span><h3>Short, useful talks</h3><p>Fifteen-minute sessions from people who do this every day, on the questions parents ask most.</p></div>
</div></div></section>
<section class="band"><div class="wrap">
<div class="promo"><div><h2>Run a camp, school, practice or local business?</h2><p>A table puts you face to face with Westchester families at the moment they're choosing. Bundles and season sponsorships available.</p></div>
<div class="cta"><a class="btn light" href="exhibit.html">Exhibitor info</a></div></div>
</div></section>
<section class="band"><div class="wrap"><div class="split">
<div><h2>Hear about each fair first.</h2><p>One email before each fair with the date, venue, exhibitor list and talk schedule.</p></div>
<div class="cta"><a class="btn" href="families.html#signup">Join the email list</a></div>
</div></div></section>
</main>
{footer()}'''
    return head(SITE, "Family resource fairs in Westchester, NY: camps, special needs resources, fall activities, preschools and caring for aging parents. Free for families.", full) + "\n" + body + "\n" + tail(full)

def event_page(x):
    zones = "".join(f'<div><h3>{e(a)}</h3><p>{e(b)}</p></div>' for a,b in x["zones"])
    chips = "".join(f'<li>{e(c)}</li>' for c in x["exhibitors"])
    talks = "".join(f'<li>{e(t)}</li>' for t in x["talks"])
    prices = "".join(f'<tr><td>{e(a)}</td><td class="num">{e(b)}</td><td class="note">{e(c)}</td></tr>' for a,b,c in x["prices"])
    body = f'''{nav()}
<main class="event {x["hue"]}">
<section class="ev-hero"><div class="wrap"><div class="panel">
<a class="back" href="index.html#fairs">← All fairs</a>
<p class="eyebrow">{x["month"]} · Resource Commons</p>
<h1>{e(x["name"])}</h1>
<p class="lede">{e(x["tagline"])}</p>
<dl class="facts"><div><dt>When</dt><dd>{e(x["when"])}</dd></div><div><dt>Where</dt><dd>{e(x["where"])}. Venue announced soon.</dd></div><div><dt>Families</dt><dd>Free, RSVP requested</dd></div></dl>
<div class="cta"><a class="btn" href="families.html#signup">RSVP free</a><a class="btn ghost" href="exhibit-{x["slug"]}.html">Reserve a table</a></div>
</div></div></section>
<section class="band"><div class="wrap">
<div class="sec-h"><h2>Who it's for</h2><p>{e(x["audience"])}</p></div>
<div class="three cards">{zones}</div>
</div></section>
<section class="band"><div class="wrap two">
<div><h2>Who you'll meet</h2><ul class="chips">{chips}</ul><p class="small-note">Exhibitor list posted as tables are confirmed.</p></div>
<div><h2>On the program</h2><ul class="talks">{talks}</ul></div>
</div></section>
<section class="band"><div class="wrap">
<div class="sec-h"><h2>For exhibitors</h2><p>Tables include a 6-foot table, two chairs, a listing in the event guide and the post-fair family survey results.</p></div>
<div class="tbl"><table><thead><tr><th>Option</th><th class="num">Price</th><th>Notes</th></tr></thead><tbody>{prices}</tbody></table></div>
<div class="cta"><a class="btn" href="exhibit-{x["slug"]}.html">Reserve a table</a><a class="btn ghost" href="exhibit.html">Bundles and sponsorship</a></div>
</div></section>
<section class="band"><div class="wrap">
<div class="sec-h"><h2>Questions</h2></div>
<div class="faq">
<details><summary>Does it cost anything for families?</summary><p>No. Families always get in free. RSVP so we can send you the exhibitor list and talk schedule ahead of time.</p></details>
<details><summary>Can I bring my kids?</summary><p>Yes. There's a supervised play area and activities so parents can talk with exhibitors.</p></details>
<details><summary>Is the venue accessible?</summary><p>Every Resource Commons venue is chosen for step-free access, accessible restrooms and nearby parking.</p></details>
<details><summary>What if it snows?</summary><p>Winter fairs have a published snow date. We'll email everyone who RSVPs if anything changes.</p></details>
</div></div></section>
</main>
{footer()}'''
    return head(f'{x["name"]} · {SITE}', x["tagline"]) + "\n" + body + "\n" + tail()

def exhibit():
    rows = "".join(f'<tr><td><a href="{x["slug"]}.html">{e(x["name"])}</a></td><td>{x["month"]}</td><td class="num">{e(x["prices"][0][1])}</td><td><a href="exhibit-{x["slug"]}.html">Reserve</a></td></tr>' for x in EVENTS)
    body = f'''{nav("exhibit")}
<main>
<section class="hero"><div class="wrap">
<p class="eyebrow">For exhibitors and sponsors</p>
<h1>Meet Westchester families when they're deciding.</h1>
<p class="lede">Each fair brings families who came specifically to choose a camp, a school, a therapist or a care option. You get a table, a listing in the guide and real conversations.</p>
<div class="cta"><a class="btn" data-link="exhibit" href="#">Apply to exhibit</a></div>
</div></section>
<section class="band"><div class="wrap">
<div class="sec-h"><h2>Table pricing by fair</h2><p>Starting prices. Each fair page lists every option.</p></div>
<div class="tbl"><table><thead><tr><th>Fair</th><th>Month</th><th class="num">Tables from</th><th></th></tr></thead><tbody>{rows}</tbody></table></div>
</div></section>
<section class="band"><div class="wrap three">
<div><h3>Multi-fair bundles</h3><p>Exhibit at three or more fairs in a season and save on every table.</p></div>
<div><h3>Season sponsorship</h3><p>Presenting and zone sponsorships include signage, a stage mention and placement in every family email.</p></div>
<div><h3>Category caps</h3><p>We limit how many exhibitors of the same type attend, so you aren't one of ten identical tables. Early applicants get first pick.</p></div>
</div></section>
<section class="band"><div class="wrap"><div class="split">
<div><h2>Get the exhibitor kit</h2><p>Dates, floor plan, what's included and payment terms.</p></div>
<div class="cta"><a class="btn" data-link="exhibit" href="#">Apply to exhibit</a></div>
</div></div></section>
</main>
{footer()}'''
    return head(f"Exhibit · {SITE}", "Exhibit or sponsor at Resource Commons family resource fairs in Westchester, NY.") + "\n" + body + "\n" + tail()


def vendor_page(x):
    opts = []
    for i,(a,b,c) in enumerate(x["prices"]):
        paid = b.startswith("$")
        btn = (f'<a class="btn" data-link="pay-{x["code"]}-{i+1}" href="#">Pay {e(b)}</a>' if paid
               else '<a class="btn ghost" data-link="exhibit" href="#">Apply</a>')
        opts.append(f'<div class="opt"><div class="opt-h"><h3>{e(a)}</h3><span class="opt-p">{e(b)}</span></div>'
                    f'<p>{e(c) if c else "Includes a 6-foot table, two chairs and a listing in the event guide."}</p>{btn}</div>')
    terms = "".join(f"<li>{e(t)}</li>" for t in TERMS)
    body = f"""{nav()}
<main class="event {x["hue"]}">
<section class="ev-hero"><div class="wrap"><div class="panel slim">
<a class="back" href="{x["slug"]}.html">← {e(x["name"])}</a>
<p class="eyebrow">Exhibitor checkout · {x["code"]}</p>
<h1>Reserve your table</h1>
<p class="lede">{e(x["name"])} · {e(x["when"])} · {e(x["where"])}</p>
</div></div></section>
<section class="band"><div class="wrap">
<div class="opts">{"".join(opts)}</div>
<div class="ach"><span class="ic" aria-hidden="true">ACH</span><div><h3>Pay by bank if you can</h3><p>Checkout offers card or bank transfer. Bank transfer takes a few days to clear but keeps fees, and table prices, low.</p></div></div>
</div></section>
<section class="band"><div class="wrap two">
<div><h2>Payment terms</h2><ul class="talks">{terms}</ul></div>
<div><h2>Need an invoice?</h2><p class="small-note">Schools, districts and nonprofits can request an invoice and pay by check or ACH. Sponsors are always invoiced.</p><a class="btn ghost" data-link="exhibit" href="#">Request an invoice</a></div>
</div></section>
</main>
{footer()}"""
    return head(f'Reserve a table · {x["name"]}', f'Exhibitor checkout for the {x["name"]}.') + "\n" + body + "\n" + tail()

def families():
    boxes = "".join(f'<label class="chk {x["hue"]}"><input type="checkbox" name="interest" value="{x["code"]}" id="i-{x["key"]}"><span>{e(x["name"])}</span></label>' for x in EVENTS)
    cards = "".join(f'<a class="mini {x["hue"]}" href="{x["slug"]}.html"><span class="mini-m">{x["month"]}</span><span>{e(x["name"])}</span></a>' for x in EVENTS)
    body = f"""{nav("families")}
<main>
<section class="hero"><div class="wrap">
<p class="eyebrow"><span class="live" aria-hidden="true"></span>For Westchester families · Always free</p>
<h1>Big family decisions, <span class="hl">less guesswork.</span></h1>
<p class="lede">Camps, preschools, therapists, after-school programs, care for a parent. Resource Commons puts the local options in one room, and in your inbox before you need them.</p>
<div class="cta"><a class="btn" href="#signup">Get fair updates</a><a class="btn ghost" href="guides.html">Browse the guides</a></div>
</div></section>
<section class="band" id="signup"><div class="wrap">
<div class="signup-card">
<div class="sec-h"><h2>Tell us what you're planning for.</h2><p>We'll email you before the fairs you pick, with the date, venue, exhibitor list and talk schedule. Nothing else.</p></div>
<form id="kit-form" class="kit" novalidate>
<fieldset><legend>I'm interested in</legend><div class="chks">{boxes}</div></fieldset>
<div class="row"><label class="fld"><span>First name</span><input id="f-name" name="first_name" autocomplete="given-name"></label>
<label class="fld"><span>Email</span><input id="f-email" name="email_address" type="email" autocomplete="email" required></label></div>
<div class="row end"><button class="btn" type="submit" id="f-submit">Sign me up</button><p class="small-note" id="f-msg" role="status">We never sell or share your email.</p></div>
</form>
</div>
</div></section>
<section class="band"><div class="wrap">
<div class="sec-h"><h2>This year's fairs</h2></div>
<div class="minis">{cards}</div>
</div></section>
<section class="band"><div class="wrap">
<div class="promo"><div><h2>Can't make a fair?</h2><p>Each fair has a downloadable guide that compares the local options side by side. {GUIDE_PRICE} each, or all five for {BUNDLE_PRICE}.</p></div>
<div class="cta"><a class="btn light" href="guides.html">See the guides</a></div></div>
</div></section>
</main>
{footer()}"""
    return head(f"For families · {SITE}", "Free Westchester family resource fairs and email updates for camps, preschools, special needs resources, activities and aging parents.") + "\n" + body + "\n" + tail()

def guides():
    cards = "".join(f"""<div class="guide {x["hue"]}"><div class="cover"><span class="cover-k">Resource Commons</span><span class="cover-n">{e(GUIDES[x["key"]][0])}</span><span class="cover-y">2027 edition · PDF</span></div>
<div class="guide-b"><p>{e(GUIDES[x["key"]][1])}</p><p class="small-note">Released before the {e(x["name"])}.</p>
<div class="guide-f"><span class="opt-p">{GUIDE_PRICE}</span><a class="btn" data-link="guide-{x["code"]}" href="#">Buy guide</a></div></div></div>""" for x in EVENTS)
    body = f"""{nav("guides")}
<main>
<section class="hero"><div class="wrap">
<p class="eyebrow">Resource guides · PDF download</p>
<h1>The local options, <span class="hl">side by side.</span></h1>
<p class="lede">Each guide is built from the fair's exhibitors and our own research, so you can compare hours, ages and costs at the kitchen table. You get the download link right after checkout.</p>
</div></section>
<section class="band"><div class="wrap">
<div class="guides">{cards}
<div class="guide ink bundle"><div class="guide-b"><span class="pill">Best value</span><h3>All five guides</h3><p>Every 2027 guide as it's released, for one price.</p>
<div class="guide-f"><span class="opt-p">{BUNDLE_PRICE}</span><a class="btn light" data-link="guide-BUNDLE" href="#">Buy the bundle</a></div></div></div>
</div>
<p class="small-note">Guides are free for exhibitors at that fair. Secure checkout by Stripe.</p>
</div></section>
</main>
{footer()}"""
    return head(f"Resource guides · {SITE}", "Downloadable Westchester guides to summer camps, special needs resources, fall activities, preschools and caring for aging parents.") + "\n" + body + "\n" + tail()

def guide_thanks():
    body = f"""{nav("guides")}
<main>
<section class="hero"><div class="wrap">
<p class="eyebrow"><span class="live" aria-hidden="true"></span>Payment received</p>
<h1>Thanks! Your guide is ready.</h1>
<p class="lede" id="dl-msg">Your download link is below. We also emailed your receipt.</p>
<div class="cta" id="dl-links"></div>
<p class="small-note">Trouble downloading? Reply to your receipt email and we'll send it directly.</p>
</div></section>
</main>
{footer()}"""
    return head(f"Your guide · {SITE}", "Download your Resource Commons guide.").replace('<meta name="description"','<meta name="robots" content="noindex">\n<meta name="description"') + "\n" + body + "\n" + tail()

CONFIG = """// Resource Commons settings. Paste links from Stripe and Kit here.
// Anything left blank shows as "opening soon" on the site.
window.RC = {
  // Kit (newsletter): the number in your Kit form's URL, e.g. app.kit.com/forms/1234567
  kitFormId: "",

  // Exhibitor application or invoice request form (Tally or Google Forms)
  exhibit: "",

  // Stripe Payment Links, one per table option. Name each Stripe product with its code first,
  // e.g. "SOF27 Standard table", so the reconciliation workbook can sort it by fair.
  pay: {
    "SOF27-1": "", "SOF27-2": "", "SOF27-3": "",
    "SNR27-1": "",
    "FAF27-1": "",
    "FSP27-1": "", "FSP27-2": "", "FSP27-3": "",
    "CAP27-1": ""
  },

  // Stripe Payment Links for guides. In each link's settings, choose
  // "Don't show confirmation page - redirect to your website" and use
  // https://resourcecommons.com/guide-thanks.html?g=CODE  (CODE = SOF27, ..., or BUNDLE)
  guide: { SOF27: "", SNR27: "", FAF27: "", FSP27: "", CAP27: "", BUNDLE: "" },

  // Where each guide PDF lives (e.g. a Google Drive share link). Shown only on the thank-you page.
  download: { SOF27: "", SNR27: "", FAF27: "", FSP27: "", CAP27: "" }
};
"""
SITEJS = r"""(function () {
  var C = window.RC || {}, pay = C.pay || {}, guide = C.guide || {}, dl = C.download || {};
  function lookup(key) {
    if (key.indexOf("pay-") === 0) return pay[key.slice(4)];
    if (key.indexOf("guide-") === 0) return guide[key.slice(6)];
    return C[key];
  }
  document.querySelectorAll("[data-link]").forEach(function (a) {
    var url = lookup(a.getAttribute("data-link"));
    if (url) { a.href = url; a.rel = "noopener"; }
    else {
      a.removeAttribute("href"); a.setAttribute("aria-disabled", "true");
      a.classList.add("soon"); a.title = "Opening soon";
      a.textContent = a.textContent + " · opening soon";
    }
  });

  var form = document.getElementById("kit-form");
  if (form) {
    var msg = document.getElementById("f-msg"), btn = document.getElementById("f-submit");
    if (!C.kitFormId) { btn.disabled = true; btn.classList.add("soon"); btn.textContent = "Sign-up opening soon"; }
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      if (!C.kitFormId) return;
      var email = document.getElementById("f-email");
      if (!email.value || !email.checkValidity()) { msg.textContent = "Enter a valid email address."; email.focus(); return; }
      var picks = Array.prototype.map.call(form.querySelectorAll("input[name=interest]:checked"), function (c) { return c.value; });
      var body = new URLSearchParams();
      body.append("email_address", email.value);
      body.append("fields[first_name]", document.getElementById("f-name").value);
      body.append("fields[interests]", picks.join(", "));
      btn.disabled = true; msg.textContent = "Signing you up...";
      fetch("https://app.kit.com/forms/" + C.kitFormId + "/subscriptions", { method: "POST", body: body, headers: { "Accept": "application/json" } })
        .then(function (r) { if (!r.ok) throw new Error(); form.reset(); msg.textContent = "You're on the list. Check your inbox to confirm."; })
        .catch(function () { msg.textContent = "That didn't go through. Please try again in a minute."; })
        .then(function () { btn.disabled = false; });
    });
  }

  var box = document.getElementById("dl-links");
  if (box) {
    var g = new URLSearchParams(location.search).get("g") || "";
    var keys = g === "BUNDLE" ? Object.keys(dl) : [g];
    var names = { SOF27: "Summer Camp Guide", SNR27: "Special Needs Resource Guide", FAF27: "Fall Activities Guide", FSP27: "Preschool & Pre-K Guide", CAP27: "Caring for Aging Parents Guide" };
    var made = 0;
    keys.forEach(function (k) {
      if (!names[k]) return;
      var a = document.createElement("a"); a.className = "btn";
      if (dl[k]) { a.href = dl[k]; a.rel = "noopener"; a.textContent = "Download the " + names[k]; }
      else { a.className = "btn ghost soon"; a.textContent = names[k] + " · we'll email it on release"; }
      box.appendChild(a); made++;
    });
    if (!made) document.getElementById("dl-msg").textContent = "We couldn't find your guide from this link. Check your receipt email, or reply to it and we'll send the guide directly.";
  }
})();
"""

if __name__ == "__main__":
    for d in ("site","preview"):
        shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    pages = {"index.html": home(), "exhibit.html": exhibit()}
    for x in EVENTS:
        pages[x["slug"]+".html"] = event_page(x)
        pages["exhibit-"+x["slug"]+".html"] = vendor_page(x)
    pages["families.html"] = families(); pages["guides.html"] = guides(); pages["guide-thanks.html"] = guide_thanks()
    for name, txt in pages.items():
        open(f"site/{name}","w").write(txt)
        if name != "index.html": open(f"preview/{name}","w").write(txt)
    open("preview/index.html","w").write(home(full=False))
    for d in ("site","preview"):
        shutil.copy("style.css", f"{d}/style.css")
        open(f"{d}/config.js","w").write(CONFIG); open(f"{d}/site.js","w").write(SITEJS)
    open("site/CNAME","w").write("resourcecommons.com\n")
    print("built", len(pages), "pages")
