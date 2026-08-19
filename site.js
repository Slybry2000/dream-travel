(() => {
  const hero = document.querySelector('.hero');
  const chrome = document.querySelector('.hero__chrome');
  const toggle = document.querySelector('.menu-toggle');
  const menu = document.querySelector('#mobile-menu');
  const menuFrame = menu?.querySelector('.mobile-menu__frame');
  const mobileQuery = window.matchMedia('(max-width: 768px)');
  const menuQuery = window.matchMedia('(max-width: 768px), (orientation: landscape) and (max-height: 540px)');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const journeyRail = document.querySelector('#journeys .journeys-list');
  const pageSections = [hero, ...document.querySelectorAll('.surface[id]')].filter(Boolean);
  const sectionLinks = [...document.querySelectorAll('.nav a[href^="#"], .mobile-menu__nav a[href^="#"]')];

  const enableSmoothScrolling = () => {
    document.documentElement.classList.add('smooth-scroll-ready');
  };
  if (window.location.hash) {
    if (document.readyState === 'complete') window.requestAnimationFrame(enableSmoothScrolling);
    else window.addEventListener('load', () => window.requestAnimationFrame(enableSmoothScrolling), { once: true });
  } else {
    enableSmoothScrolling();
  }

  if (hero && chrome) {
    const setPastHero = (pastHero) => {
      chrome.classList.toggle('is-past-hero', pastHero);
    };

    if ('IntersectionObserver' in window) {
      const heroObserver = new IntersectionObserver(
        ([entry]) => setPastHero(!entry.isIntersecting),
        { rootMargin: '-64px 0px 0px 0px', threshold: 0 }
      );
      heroObserver.observe(hero);
    } else {
      let navFrame = 0;
      const updateChrome = () => {
        navFrame = 0;
        setPastHero(hero.getBoundingClientRect().bottom <= 64);
      };
      const requestChromeUpdate = () => {
        if (!navFrame) navFrame = window.requestAnimationFrame(updateChrome);
      };
      updateChrome();
      window.addEventListener('scroll', requestChromeUpdate, { passive: true });
      window.addEventListener('resize', requestChromeUpdate, { passive: true });
    }
  }

  if (journeyRail) {
    const journeys = [...journeyRail.querySelectorAll('.journey')];
    let activeJourney = 0;
    let journeyFrame = 0;
    let commandedJourney = null;
    let journeySettleTimer = 0;

    const finishJourneyScroll = () => {
      window.clearTimeout(journeySettleTimer);
      journeySettleTimer = 0;
      commandedJourney = null;
      updateJourneyFromScroll();
    };

    const selectJourney = (nextIndex, shouldScroll = false) => {
      activeJourney = Math.max(0, Math.min(journeys.length - 1, nextIndex));
      journeys.forEach((journey, index) => {
        const isActive = index === activeJourney;
        journey.classList.toggle('is-active', isActive);
        if (isActive) journey.setAttribute('aria-current', 'true');
        else journey.removeAttribute('aria-current');
      });

      if (!shouldScroll || !mobileQuery.matches) return;
      const journey = journeys[activeJourney];
      const railLeft = journeyRail.getBoundingClientRect().left;
      const journeyLeft = journey.getBoundingClientRect().left;
      const scrollPadding = Number.parseFloat(getComputedStyle(journeyRail).scrollPaddingLeft) || 0;
      commandedJourney = activeJourney;
      journeyRail.scrollTo({
        left: journeyRail.scrollLeft + journeyLeft - railLeft - scrollPadding,
        behavior: reducedMotion.matches ? 'auto' : 'smooth'
      });
      window.clearTimeout(journeySettleTimer);
      if (reducedMotion.matches) {
        window.requestAnimationFrame(finishJourneyScroll);
      } else {
        journeySettleTimer = window.setTimeout(finishJourneyScroll, 700);
      }
    };

    selectJourney(0);
    journeyRail.addEventListener('keydown', (event) => {
      if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
      event.preventDefault();
      selectJourney(activeJourney + (event.key === 'ArrowRight' ? 1 : -1), true);
    });

    const updateJourneyFromScroll = () => {
      journeyFrame = 0;
      if (!mobileQuery.matches) return;
      if (commandedJourney !== null) {
        selectJourney(commandedJourney);
        return;
      }
      const railRect = journeyRail.getBoundingClientRect();
      const railCenter = railRect.left + railRect.width / 2;
      const nearestIndex = journeys.reduce((nearest, journey, index) => {
        const rect = journey.getBoundingClientRect();
        const distance = Math.abs(rect.left + rect.width / 2 - railCenter);
        return distance < nearest.distance ? { index, distance } : nearest;
      }, { index: 0, distance: Number.POSITIVE_INFINITY }).index;
      selectJourney(nearestIndex);
    };

    journeyRail.addEventListener('scroll', () => {
      if (!journeyFrame) journeyFrame = window.requestAnimationFrame(updateJourneyFromScroll);
    }, { passive: true });
    journeyRail.addEventListener('scrollend', () => {
      if (commandedJourney !== null) finishJourneyScroll();
    });

    const syncJourneyViewport = ({ matches }) => {
      if (matches) window.requestAnimationFrame(updateJourneyFromScroll);
    };
    if (typeof mobileQuery.addEventListener === 'function') {
      mobileQuery.addEventListener('change', syncJourneyViewport);
    } else {
      mobileQuery.addListener(syncJourneyViewport);
    }
  }

  // The hosting and traveler rails are native touch scrollers. Mirror the
  // journey rail's item-by-item arrow-key behavior without adding controls or
  // changing their desktop layouts.
  document.querySelectorAll('#hosting .tier-grid, #travelers .praise-list').forEach((rail) => {
    const items = [...rail.children];
    if (!items.length) return;

    const nearestItemIndex = () => {
      const railLeft = rail.getBoundingClientRect().left;
      const scrollPadding = Number.parseFloat(getComputedStyle(rail).scrollPaddingLeft) || 0;
      return items.reduce((nearest, item, index) => {
        const distance = Math.abs(item.getBoundingClientRect().left - railLeft - scrollPadding);
        return distance < nearest.distance ? { index, distance } : nearest;
      }, { index: 0, distance: Number.POSITIVE_INFINITY }).index;
    };

    rail.addEventListener('keydown', (event) => {
      if (!mobileQuery.matches || (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight')) return;
      event.preventDefault();
      const nextIndex = Math.max(0, Math.min(
        items.length - 1,
        nearestItemIndex() + (event.key === 'ArrowRight' ? 1 : -1)
      ));
      const railLeft = rail.getBoundingClientRect().left;
      const itemLeft = items[nextIndex].getBoundingClientRect().left;
      const scrollPadding = Number.parseFloat(getComputedStyle(rail).scrollPaddingLeft) || 0;
      rail.scrollTo({
        left: rail.scrollLeft + itemLeft - railLeft - scrollPadding,
        behavior: reducedMotion.matches ? 'auto' : 'smooth'
      });
    });
  });

  if (pageSections.length && sectionLinks.length) {
    let commandedSectionId = null;
    let pendingFocusTarget = null;
    let sectionSettleTimer = 0;
    let sectionHardStopTimer = 0;

    const setActiveSection = (sectionId) => {
      sectionLinks.forEach((link) => {
        const isCurrent = sectionId && link.getAttribute('href') === `#${sectionId}`;
        if (isCurrent) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    };

    const updateActiveSection = () => {
      if (commandedSectionId !== null) {
        setActiveSection(commandedSectionId);
        return;
      }
      const readingLine = window.innerHeight * 0.28;
      const activeSection = pageSections.find((section) => {
        const rect = section.getBoundingClientRect();
        return rect.top <= readingLine && rect.bottom > readingLine;
      });
      setActiveSection(activeSection === hero ? '' : activeSection?.id || '');
    };

    if ('IntersectionObserver' in window) {
      const sectionObserver = new IntersectionObserver(updateActiveSection, {
        rootMargin: '-24% 0px -66% 0px',
        threshold: 0
      });
      pageSections.forEach((section) => sectionObserver.observe(section));
    } else {
      let sectionFrame = 0;
      const requestSectionUpdate = () => {
        if (sectionFrame) return;
        sectionFrame = window.requestAnimationFrame(() => {
          sectionFrame = 0;
          updateActiveSection();
        });
      };
      window.addEventListener('scroll', requestSectionUpdate, { passive: true });
      window.addEventListener('resize', requestSectionUpdate, { passive: true });
    }
    updateActiveSection();

    const resolveHashTarget = (hash) => {
      if (!hash || hash === '#') return hero;
      try {
        return document.getElementById(decodeURIComponent(hash.slice(1)));
      } catch {
        return null;
      }
    };

    const focusDestination = (target) => {
      const focusTarget = target?.querySelector('h1, h2') || target;
      if (!focusTarget) return;
      const hadTabIndex = focusTarget.hasAttribute('tabindex');
      const previousTabIndex = focusTarget.getAttribute('tabindex');
      if (!hadTabIndex) focusTarget.setAttribute('tabindex', '-1');
      focusTarget.dataset.hashFocus = '';
      const cleanup = () => {
        delete focusTarget.dataset.hashFocus;
        if (!hadTabIndex) focusTarget.removeAttribute('tabindex');
        else focusTarget.setAttribute('tabindex', previousTabIndex);
      };
      focusTarget.addEventListener('blur', cleanup, { once: true });
      focusTarget.focus({ preventScroll: true });
    };

    const finishSectionNavigation = () => {
      window.clearTimeout(sectionSettleTimer);
      window.clearTimeout(sectionHardStopTimer);
      sectionSettleTimer = 0;
      sectionHardStopTimer = 0;
      const focusTarget = pendingFocusTarget;
      commandedSectionId = null;
      pendingFocusTarget = null;
      if (focusTarget?.isConnected) focusDestination(focusTarget);
      updateActiveSection();
    };

    const queueSectionSettle = () => {
      window.clearTimeout(sectionSettleTimer);
      sectionSettleTimer = window.setTimeout(
        finishSectionNavigation,
        reducedMotion.matches ? 0 : 120
      );
    };

    const beginSectionNavigation = (target, shouldFocus = false) => {
      if (!target) return;
      window.clearTimeout(sectionSettleTimer);
      window.clearTimeout(sectionHardStopTimer);
      commandedSectionId = target === hero ? '' : target.id;
      pendingFocusTarget = shouldFocus ? target : null;
      setActiveSection(commandedSectionId);
      window.requestAnimationFrame(queueSectionSettle);
      sectionHardStopTimer = window.setTimeout(
        finishSectionNavigation,
        reducedMotion.matches ? 32 : 1600
      );
    };

    document.addEventListener('click', (event) => {
      if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      const link = event.target.closest('a[href^="#"]');
      if (!link) return;
      const target = resolveHashTarget(link.getAttribute('href'));
      if (!target) return;
      const shouldFocus = event.detail === 0 || Boolean(link.closest('#mobile-menu'));
      beginSectionNavigation(target, shouldFocus);
    });

    window.addEventListener('scroll', () => {
      if (commandedSectionId !== null) queueSectionSettle();
    }, { passive: true });

    if ('onscrollend' in window) {
      window.addEventListener('scrollend', () => {
        if (commandedSectionId !== null) finishSectionNavigation();
      }, { passive: true });
    }

    window.addEventListener('hashchange', () => {
      const target = resolveHashTarget(window.location.hash);
      if (!target) return;
      const targetId = target === hero ? '' : target.id;
      if (commandedSectionId === targetId) return;
      const shouldFocus = Boolean(document.activeElement?.hasAttribute('data-hash-focus'));
      beginSectionNavigation(target, shouldFocus);
    });

    const syncDeepLink = () => {
      if (!window.location.hash) return;
      beginSectionNavigation(resolveHashTarget(window.location.hash));
    };
    if (document.readyState === 'complete') window.requestAnimationFrame(syncDeepLink);
    else window.addEventListener('load', () => window.requestAnimationFrame(syncDeepLink), { once: true });
  }

  if (!reducedMotion.matches && 'IntersectionObserver' in window) {
    const deepLinkedSection = document.getElementById(window.location.hash.slice(1));
    const motionSections = pageSections.filter((section) => section.matches?.('#method, #about'));
    motionSections.forEach((section) => {
      const inner = section.querySelector(':scope > .surface__inner');
      if (!inner) return;
      inner.classList.add('motion-step');
      section.classList.add('motion-pending');
      if (section === deepLinkedSection) section.classList.add('is-entered');
    });

    document.documentElement.classList.add('motion-ready');
    const motionObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-entered');
        observer.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.04 });
    motionSections.forEach((section) => motionObserver.observe(section));
  }

  if (!toggle || !menu || !menuFrame) return;

  let closeTimer = 0;
  let restoreFocus = true;

  const lockPage = () => {
    const gap = Math.max(0, window.innerWidth - document.documentElement.clientWidth);
    document.body.style.setProperty('--nav-scrollbar-gap', `${gap}px`);
    document.body.classList.add('menu-open');
  };

  const unlockPage = () => {
    document.body.classList.remove('menu-open');
    document.body.style.removeProperty('--nav-scrollbar-gap');
  };

  const finishClose = () => {
    window.clearTimeout(closeTimer);
    closeTimer = 0;
    menu.classList.remove('is-ready');
    if (menu.open) menu.close();
    toggle.setAttribute('aria-expanded', 'false');
    unlockPage();
    if (restoreFocus && menuQuery.matches) toggle.focus({ preventScroll: true });
    restoreFocus = true;
  };

  const closeMenu = ({ immediate = false, returnFocus = true } = {}) => {
    if (!menu.open) return;
    restoreFocus = returnFocus;
    menu.classList.remove('is-ready');
    if (immediate || reducedMotion.matches) {
      finishClose();
      return;
    }
    closeTimer = window.setTimeout(finishClose, 500);
  };

  const openMenu = () => {
    if (!menuQuery.matches || menu.open) return;
    window.clearTimeout(closeTimer);
    lockPage();
    menu.showModal();
    toggle.setAttribute('aria-expanded', 'true');
    window.requestAnimationFrame(() => {
      menu.classList.add('is-ready');
      menu.querySelector('.mobile-menu__nav a')?.focus({ preventScroll: true });
    });
  };

  toggle.addEventListener('click', () => {
    if (menu.open) closeMenu();
    else openMenu();
  });

  menu.addEventListener('cancel', (event) => {
    event.preventDefault();
    closeMenu();
  });

  menu.addEventListener('click', (event) => {
    if (event.target === menu || event.target.closest('[data-menu-close]')) {
      closeMenu();
      return;
    }

    if (event.target.closest('.mobile-menu a[href^="#"]')) {
      closeMenu({ immediate: true, returnFocus: false });
    }
  });

  menu.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      event.preventDefault();
      closeMenu();
      return;
    }
    if (event.key !== 'Tab') return;
    const focusable = [...menu.querySelectorAll('a[href], button:not([disabled])')];
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });

  const handleViewportChange = ({ matches }) => {
    if (!matches && menu.open) closeMenu({ immediate: true, returnFocus: false });
  };

  if (typeof menuQuery.addEventListener === 'function') {
    menuQuery.addEventListener('change', handleViewportChange);
  } else {
    menuQuery.addListener(handleViewportChange);
  }
})();
