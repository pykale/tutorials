/*
 * PyKale Tutorials — page feedback + homepage scroll-spy. Vanilla JS, no backend, no analytics.
 *
 * "Send detailed feedback" / "Report a problem" open a *prefilled* GitHub issue (built with
 * URLSearchParams, never string concatenation) that the user reviews and submits themselves.
 * "Yes / Not really" record a lightweight, session-only acknowledgement.
 */
(function () {
  "use strict";

  function pageTitle() {
    // document.title is "<page> — PyKale Tutorials"; keep just the page part.
    return (document.title || "").split(" — ")[0].trim() || "PyKale Tutorials";
  }

  function issueUrl(repo, version, category) {
    var title = "[Docs feedback] " + pageTitle();
    var body =
      "### Page\n\n" + pageTitle() +
      "\n\n### URL\n\n" + window.location.href +
      "\n\n### PyKale version\n\n" + (version || "unknown") +
      "\n\n### Category\n\n" + category +
      "\n\n### Feedback\n\nPlease describe what was unclear, incorrect or missing.\n" +
      "\n### Additional context\n\n<!-- Add screenshots or other details here. -->\n";
    var params = new URLSearchParams({ title: title, body: body, labels: "documentation" });
    return "https://github.com/" + repo + "/issues/new?" + params.toString();
  }

  function initFeedback(box) {
    var repo = box.getAttribute("data-repo");
    var version = box.getAttribute("data-version");
    var send = box.querySelector(".pky-fb-send");
    var problem = box.querySelector(".pky-fb-problem");
    var yes = box.querySelector(".pky-fb-yes");
    var no = box.querySelector(".pky-fb-no");
    var thanks = box.querySelector(".pky-fb-thanks");

    if (send) send.href = issueUrl(repo, version, "feedback");
    if (problem) problem.href = issueUrl(repo, version, "bug");

    var key = "pky-fb:" + window.location.pathname;

    function acknowledge(msg) {
      if (thanks) {
        thanks.textContent = msg;
        thanks.hidden = false;
      }
      try { sessionStorage.setItem(key, "1"); } catch (e) { /* ignore */ }
    }

    if (yes) yes.addEventListener("click", function () { acknowledge("Thanks — that helps."); });
    if (no) no.addEventListener("click", function () {
      acknowledge("Thanks. Please tell us more:");
      if (send) send.classList.add("pky-fb-emphasis");
    });

    try {
      if (sessionStorage.getItem(key) === "1" && thanks) thanks.hidden = false;
    } catch (e) { /* ignore */ }
  }

  function initScrollSpy() {
    var nav = document.querySelector(".pky-onthispage");
    if (!nav || !("IntersectionObserver" in window)) return;
    var links = Array.prototype.slice.call(nav.querySelectorAll("a[href^='#']"));
    var byId = {};
    links.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });
    var targets = Object.keys(byId)
      .map(function (id) { return document.getElementById(id); })
      .filter(Boolean);
    if (!targets.length) return;

    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          links.forEach(function (a) { a.removeAttribute("aria-current"); });
          var a = byId[e.target.id];
          if (a) a.setAttribute("aria-current", "true");
        }
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    targets.forEach(function (t) { obs.observe(t); });
  }

  function relocateTutorialActions() {
    // article_header_end renders the toolbar above the article title; move it to just after the
    // first heading so it appears "after the title and essential metadata", per the design.
    var actions = document.querySelector(".pky-actions");
    if (!actions) return;
    var article = document.querySelector(".bd-article");
    var h1 = article && article.querySelector("h1");
    if (h1 && h1.parentNode) {
      h1.parentNode.insertBefore(actions, h1.nextSibling);
    }
    // Draft tutorials have only a stub notebook, so hiding the sphinx-gallery download block (a class
    // on <body> drives the CSS) avoids offering an incomplete .ipynb/.py/.zip to download.
    if (actions.getAttribute("data-draft") === "true") {
      document.body.classList.add("pky-draft-tutorial");
    }
  }

  function init() {
    Array.prototype.forEach.call(document.querySelectorAll(".pky-feedback"), initFeedback);
    initScrollSpy();
    relocateTutorialActions();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
