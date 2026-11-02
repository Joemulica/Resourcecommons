(function () {
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
