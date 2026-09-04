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

  function stillTarget(el) {
    return el && el.closest ? el.closest(".stills img") : null;
  }

  function shouldBypass(img) {
    var link = img.closest("a[href]");
    if (!link) return false;
    var href = link.getAttribute("href") || "";
    return !!(href && href.charAt(0) !== "#" && href.indexOf("javascript:") !== 0);
  }

  function openFromImg(img, e) {
    if (!img || shouldBypass(img)) return false;
    if (e) e.preventDefault();
    openLightbox(img.currentSrc || img.src, img.alt);
    return true;
  }

  document.addEventListener("click", function (e) {
    openFromImg(stillTarget(e.target), e);
  });

  // Make stills keyboard-activatable
  document.querySelectorAll(".stills img").forEach(function (img) {
    if (!img.hasAttribute("tabindex")) img.setAttribute("tabindex", "0");
    if (!img.hasAttribute("role")) img.setAttribute("role", "button");
    img.setAttribute("aria-label", img.getAttribute("aria-label") || "View larger");
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Enter" && e.key !== " ") return;
    var img = stillTarget(e.target);
    if (!img) return;
    openFromImg(img, e);
  });
})();
