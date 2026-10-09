
    const navLinks = [...document.querySelectorAll(".site-nav a")];
    const navTargets = navLinks
      .map((link) => ({ link, target: document.querySelector(link.hash) }))
      .filter(({ target }) => target);

    function setActiveLink(activeLink) {
      navLinks.forEach((link) => {
        const isActive = link === activeLink;
        link.classList.toggle("is-active", isActive);
        if (isActive) {
          link.setAttribute("aria-current", "location");
        } else {
          link.removeAttribute("aria-current");
        }
      });
    }

    function revealTarget(target) {
      if (!target) return;
      target.classList.add("is-visible");
    }

    function smoothScrollToTarget(target, link) {
      if (!target) return;
      const offset = target.getBoundingClientRect().top + window.scrollY - 72;
      window.scrollTo({ top: offset, behavior: "smooth" });
      setActiveLink(link);
      history.replaceState(null, "", link.getAttribute("href"));
      setTimeout(() => revealTarget(target), 180);
    }

    navLinks.forEach((link) => {
      link.addEventListener("click", (event) => {
        const target = document.querySelector(link.hash);
        if (target) {
          event.preventDefault();
          smoothScrollToTarget(target, link);
        } else {
          setActiveLink(link);
        }
      });
    });

    let scrollUpdatePending = false;
    function updateActiveLinkFromScroll() {
      scrollUpdatePending = false;
      const passedTargets = navTargets
        .map(({ link, target }) => ({ link, top: target.getBoundingClientRect().top }))
        .filter(({ top }) => top <= 84)
        .sort((first, second) => second.top - first.top);
      if (passedTargets.length) setActiveLink(passedTargets[0].link);
    }

  const revealSections = document.querySelectorAll(".reveal-section");

  const revealObserver = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.05,
      rootMargin: "0px 0px -30px 0px"
    }
  );

  revealSections.forEach((section) => {
    revealObserver.observe(section);
  });
