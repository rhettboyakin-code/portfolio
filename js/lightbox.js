(function () {
  function openLightbox(src, alt) {
    var existing = document.getElementById("lb-root");
    if (existing) existing.remove();

    var root = document.createElement("div");
    root.id = "lb-root";
    root.className = "lb-root";
    root.setAttribute("role", "dialog");
    root.setAttribute("aria-modal", "true");
    root.innerHTML =
      '<button type="button" class="lb-close" aria-label="Close">&times;</button>' +
      '<img class="lb-img" src="" alt="">';
    root.querySelector(".lb-img").src = src;
    root.querySelector(".lb-img").alt = alt || "";

    function close() {
      root.remove();
      document.removeEventListener("keydown", onKey);
    }
    function onKey(e) {
      if (e.key === "Escape") close();
    }

    root.addEventListener("click", function (e) {
      if (e.target === root || e.target.classList.contains("lb-close")) close();
    });
    document.addEventListener("keydown", onKey);
    document.body.appendChild(root);
  }

  document.addEventListener("click", function (e) {
    var img = e.target.closest(".stills img");
    if (!img) return;
    // If the image is wrapped in a real outbound link (not #), leave it alone
    var link = img.closest("a[href]");
    if (link) {
      var href = link.getAttribute("href") || "";
      if (href && href.charAt(0) !== "#" && !href.startsWith("javascript:")) {
        return;
      }
    }
    e.preventDefault();
    openLightbox(img.currentSrc || img.src, img.alt);
  });
})();
