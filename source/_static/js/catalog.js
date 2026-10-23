/*
 * PyKale Tutorials — faceted catalogue.
 *
 * Vanilla JS, no framework. Reads the generated tutorials.json, renders a metadata-rich card grid,
 * and filters it client-side by facet chips + text search. On pages with data-sync-url, the active
 * filters are mirrored to the URL query string so a filtered view can be shared and survives reload.
 *
 * Accessibility: facet chips are real <button aria-pressed>; the result count is an aria-live status;
 * cards are <a> with descriptive text (domain/status are words, not colour alone).
 */
(function () {
  "use strict";

  function pkyInit() {
  var root = document.getElementById("pky-catalog");
  if (!root) return;
  document.body.classList.add("pky-landing");
  if (root.hasAttribute("data-home")) document.body.classList.add("pky-home");
  var siteRoot = root.getAttribute("data-root") || "";

  var FACETS = [
    { key: "domain", label: "Domain" },
    { key: "task", label: "Task" },
    { key: "modality", label: "Modality" },
    { key: "difficulty", label: "Difficulty" },
    { key: "hardware", label: "Runtime" },
    { key: "status", label: "Status" }
  ];

  var grid = document.getElementById("pky-grid");
  var facetBox = document.getElementById("pky-facets");
  var countEl = document.getElementById("pky-count");
  var emptyEl = document.getElementById("pky-empty");
  var searchEl = document.getElementById("pky-q");
  var clearEl = document.getElementById("pky-clear");
  var filterDetails = root.querySelector(".pky-filter-details");
  var filterSummary = document.getElementById("pky-filter-summary");
  var syncUrl = root.hasAttribute("data-sync-url");

  if (filterDetails) {
    var compactFilters = window.matchMedia("(max-width: 768px)");
    filterDetails.open = !compactFilters.matches;
    compactFilters.addEventListener("change", function (event) {
      filterDetails.open = !event.matches;
    });
  }

  var domainLabels = {};
  var tutorials = [];
  var active = {}; // key -> Set of selected values
  var query = "";

  FACETS.forEach(function (f) { active[f.key] = new Set(); });

  function statusOf(t) { return t.draft ? "draft" : "written"; }
  function valuesFor(t, key) {
    if (key === "status") return [statusOf(t)];
    if (key === "modality") return t.modality || [];
    return t[key] != null ? [t[key]] : [];
  }
  function prettyDomain(d) { return domainLabels[d] || d; }
  function prettyHardware(h) { return (h || "").replace(/_/g, " "); }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function readUrl() {
    if (!syncUrl) return;
    var params = new URLSearchParams(window.location.search);
    FACETS.forEach(function (f) {
      var v = params.get(f.key);
      if (v) v.split(",").forEach(function (x) { active[f.key].add(x); });
    });
    if (params.get("q")) { query = params.get("q"); searchEl.value = query; }
  }

  function writeUrl() {
    if (!syncUrl) return;
    var params = new URLSearchParams();
    FACETS.forEach(function (f) {
      if (active[f.key].size) params.set(f.key, Array.from(active[f.key]).join(","));
    });
    if (query) params.set("q", query);
    var qs = params.toString();
    history.replaceState(null, "", qs ? "?" + qs : window.location.pathname);
  }

  function matches(t) {
    for (var i = 0; i < FACETS.length; i++) {
      var key = FACETS[i].key, sel = active[key];
      if (sel.size) {
        var vals = valuesFor(t, key);
        var hit = vals.some(function (v) { return sel.has(v); });
        if (!hit) return false;
      }
    }
    if (query) {
      var hay = (t.title + " " + t.summary + " " + (t.method || []).join(" ") + " " +
        (t.modality || []).join(" ")).toLowerCase();
      if (hay.indexOf(query.toLowerCase()) === -1) return false;
    }
    return true;
  }

  function card(t) {
    var thumb = siteRoot + "_static/thumbnails/" + t.slug + ".svg";
    var tags = (t.modality || []).slice(0, 3).map(function (m) {
      return '<span class="pky-tag">' + esc(m) + "</span>";
    }).join("");
    var statusBadge = t.draft
      ? '<span class="pky-chip pky-chip-draft">Draft</span>'
      : '<span class="pky-chip pky-chip-written">Written</span>';
    var href = siteRoot + "_gallery/" + t.path + "/plot_" + t.slug + ".html";
    return (
      '<a class="pky-card pky-' + esc(t.domain) + '" href="' + esc(href) + '">' +
      '<img class="pky-card-thumb" src="' + thumb + '" alt="" loading="lazy">' +
      '<div class="pky-card-body">' +
      '<div class="pky-card-badges"><span class="pky-chip pky-chip-domain">' +
      esc(prettyDomain(t.domain)) + "</span>" + statusBadge + "</div>" +
      '<h3 class="pky-card-title">' + esc(t.title) + "</h3>" +
      '<p class="pky-card-summary">' + esc(t.summary) + "</p>" +
      '<div class="pky-card-tags">' + tags + "</div>" +
      '<div class="pky-card-meta"><span>' + esc(t.difficulty) + "</span><span>" +
      esc(t.estimated_runtime) + "</span><span>" + esc(prettyHardware(t.hardware)) + "</span></div>" +
      "</div></a>"
    );
  }

  function render() {
    var shown = tutorials.filter(matches);
    grid.innerHTML = shown.map(card).join("");
    emptyEl.hidden = shown.length !== 0;
    countEl.textContent = shown.length + " of " + tutorials.length + " tutorials";
    if (filterSummary) {
      var selectedCount = FACETS.reduce(function (total, f) { return total + active[f.key].size; }, 0);
      filterSummary.textContent = selectedCount ? "Filters (" + selectedCount + " active)" : "Filters";
    }
    writeUrl();
  }

  function facetValueLabel(key, v) {
    if (key === "domain") return prettyDomain(v);
    if (key === "hardware") return prettyHardware(v);
    return v;
  }

  function buildFacets() {
    FACETS.forEach(function (f) {
      var values = {};
      tutorials.forEach(function (t) {
        valuesFor(t, f.key).forEach(function (v) { values[v] = (values[v] || 0) + 1; });
      });
      var keys = Object.keys(values).sort();
      if (!keys.length) return;

      var group = document.createElement("div");
      group.className = "pky-facet-group";
      var legend = document.createElement("span");
      legend.className = "pky-facet-label";
      legend.textContent = f.label;
      group.appendChild(legend);

      keys.forEach(function (v) {
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "pky-facet-chip";
        btn.setAttribute("aria-pressed", active[f.key].has(v) ? "true" : "false");
        btn.textContent = facetValueLabel(f.key, v) + " (" + values[v] + ")";
        btn.addEventListener("click", function () {
          if (active[f.key].has(v)) active[f.key].delete(v);
          else active[f.key].add(v);
          btn.setAttribute("aria-pressed", active[f.key].has(v) ? "true" : "false");
          render();
        });
        group.appendChild(btn);
      });
      facetBox.appendChild(group);
    });
  }

  function clearAll() {
    FACETS.forEach(function (f) { active[f.key].clear(); });
    query = "";
    searchEl.value = "";
    facetBox.querySelectorAll(".pky-facet-chip").forEach(function (b) {
      b.setAttribute("aria-pressed", "false");
    });
    render();
  }

  searchEl.addEventListener("input", function () { query = searchEl.value.trim(); render(); });
  clearEl.addEventListener("click", clearAll);

  var src = root.getAttribute("data-src");
  fetch(src).then(function (r) { return r.json(); }).then(function (data) {
    (data.buckets || []).forEach(function (b) { domainLabels[b.id] = b.label; });
    tutorials = data.tutorials || [];
    readUrl();
    buildFacets();
    render();
  }).catch(function () {
    countEl.textContent = "Could not load the catalogue.";
  });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", pkyInit);
  } else {
    pkyInit();
  }
})();
