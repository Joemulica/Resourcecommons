(function () {
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
