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
    links = "".join(f'<a href="{x}.html"{" aria-current=\"page\"" if active==x else ""}>{t}</a>' for x,t in [("index","Fairs"),("exhibit","Exhibit")])
    return f'''<header class="top"><div class="wrap top-in">
<a class="brand" href="index.html"><span class="mark" aria-hidden="true"></span>Resource Commons</a>
<nav class="nav">{links}<a class="btn small" data-link="signup" href="#">Get updates</a></nav>
</div></header>'''

def footer():
    return f'''<footer class="foot"><div class="wrap foot-in">
<div><a class="brand" href="index.html"><span class="mark" aria-hidden="true"></span>Resource Commons</a>
<p>Family resource fairs in Westchester, New York. Free for families.</p></div>
<div class="foot-links">{"".join(f'<a href="{x["slug"]}.html">{e(x["name"])}</a>' for x in EVENTS)}<a href="exhibit.html">Exhibit or sponsor</a></div>
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
<div class="cta"><a class="btn" data-link="signup" href="#">Join the email list</a></div>
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
<div class="cta"><a class="btn" data-link="rsvp-{x["key"]}" href="#">RSVP free</a><a class="btn ghost" data-link="exhibit-{x["key"]}" href="#">Reserve a table</a></div>
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
<div class="cta"><a class="btn" data-link="exhibit-{x["key"]}" href="#">Reserve a table</a><a class="btn ghost" href="exhibit.html">Bundles and sponsorship</a></div>
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
    rows = "".join(f'<tr><td><a href="{x["slug"]}.html">{e(x["name"])}</a></td><td>{x["month"]}</td><td class="num">{e(x["prices"][0][1])}</td></tr>' for x in EVENTS)
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
<div class="tbl"><table><thead><tr><th>Fair</th><th>Month</th><th class="num">Tables from</th></tr></thead><tbody>{rows}</tbody></table></div>
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

CONFIG = '''// Paste your form and payment links here. Any link left blank shows as "Opening soon".
// Good free options: Tally or Google Forms for RSVPs and exhibitor applications,
// Stripe Payment Links for table payments, Mailchimp or Buttondown for the email list.
window.RC_LINKS = {
  signup: "",              // email list sign-up page
  exhibit: "",             // general exhibitor application
  "rsvp-summer": "",       "exhibit-summer": "",
  "rsvp-specialneeds": "", "exhibit-specialneeds": "",
  "rsvp-fall": "",         "exhibit-fall": "",
  "rsvp-preschool": "",    "exhibit-preschool": "",
  "rsvp-aging": "",        "exhibit-aging": ""
};
'''
SITEJS = '''(function () {
  var links = window.RC_LINKS || {};
  document.querySelectorAll("[data-link]").forEach(function (a) {
    var key = a.getAttribute("data-link");
    var url = links[key] || (key.indexOf("exhibit-") === 0 ? links.exhibit : "");
    if (url) { a.href = url; a.target = "_blank"; a.rel = "noopener"; }
    else {
      a.removeAttribute("href"); a.setAttribute("aria-disabled", "true");
      a.classList.add("soon"); a.title = "Opening soon";
      if (!a.classList.contains("small")) a.textContent = a.textContent + " · opening soon";
    }
  });
})();
'''

if __name__ == "__main__":
    for d in ("site","preview"):
        shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    pages = {"index.html": home(), "exhibit.html": exhibit()}
    for x in EVENTS: pages[x["slug"]+".html"] = event_page(x)
    for name, txt in pages.items():
        open(f"site/{name}","w").write(txt)
        if name != "index.html": open(f"preview/{name}","w").write(txt)
    open("preview/index.html","w").write(home(full=False))
    for d in ("site","preview"):
        shutil.copy("style.css", f"{d}/style.css")
        open(f"{d}/config.js","w").write(CONFIG); open(f"{d}/site.js","w").write(SITEJS)
    open("site/CNAME","w").write("resourcecommons.com\n")
    print("built", len(pages), "pages")
