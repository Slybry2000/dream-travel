(() => {
  const header = document.querySelector('[data-header]');
  const menu = document.querySelector('#mobile-menu');
  const openMenu = document.querySelector('[data-menu-open]');
  const closeMenu = document.querySelector('[data-menu-close]');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const flourishes = [...document.querySelectorAll('.flourish')];
  if (document.body.dataset.flourishes === 'on' && flourishes.length) {
    if (!reduceMotion && 'IntersectionObserver' in window) {
      document.documentElement.classList.add('flourish-animate');
      const flourishObserver = new IntersectionObserver((entries, instance) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-drawn');
          instance.unobserve(entry.target);
        });
      }, { threshold: .25 });
      flourishes.forEach((flourish) => flourishObserver.observe(flourish));
    } else {
      flourishes.forEach((flourish) => flourish.classList.add('is-drawn'));
    }
  }

  if (header) {
    const syncHeader = () => header.classList.toggle('is-scrolled', window.scrollY > 24);
    syncHeader();
    window.addEventListener('scroll', syncHeader, { passive: true });
  }

  const showMenu = () => {
    if (!menu || menu.open) return;
    menu.showModal();
    openMenu?.setAttribute('aria-expanded', 'true');
    document.documentElement.classList.add('menu-open');
  };
  const hideMenu = () => {
    if (!menu?.open) return;
    menu.close();
    openMenu?.setAttribute('aria-expanded', 'false');
    document.documentElement.classList.remove('menu-open');
  };
  openMenu?.addEventListener('click', showMenu);
  closeMenu?.addEventListener('click', hideMenu);
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menu?.open) hideMenu();
  });
  menu?.addEventListener('click', (event) => {
    if (event.target === menu || event.target.closest('[data-menu-link]')) hideMenu();
  });
  menu?.addEventListener('close', () => {
    openMenu?.setAttribute('aria-expanded', 'false');
    document.documentElement.classList.remove('menu-open');
  });

  const orbitStage = document.querySelector('[data-orbit-stage]');
  if (orbitStage && document.body.dataset.discoveryLayout === 'orbit') {
    const items = [...orbitStage.querySelectorAll('[data-orbit-item]')];
    const toggleOrbit = document.querySelector('[data-orbit-toggle]');
    const resetOrbit = document.querySelector('[data-orbit-reset]');
    const orbitSection = orbitStage.closest('.discovery-orbit');
    const motionShell = document.querySelector('[data-orbit-motion]');
    const motionVideos = [...(motionShell?.querySelectorAll('[data-orbit-motion-video]') || [])];
    const motionLabel = document.querySelector('[data-orbit-motion-label]');
    const motionCredit = document.querySelector('[data-orbit-motion-credit]');
    const saveData = Boolean(navigator.connection?.saveData);
    const allowMotionPreview = document.body.dataset.motionPreview === 'on' && !reduceMotion && !saveData && motionVideos.length === 2;
    const goldenAngle = Math.PI * (3 - Math.sqrt(5));
    const points = items.map((item, index) => {
      const y = 1 - ((index + .5) / items.length) * 2;
      const radius = Math.sqrt(1 - y * y);
      const theta = goldenAngle * index;
      return { item, x: Math.cos(theta) * radius, y, z: Math.sin(theta) * radius };
    });
    let yaw = .18;
    let pitch = -.12;
    let dragging = false;
    let moved = false;
    let hovering = false;
    let manualPause = reduceMotion;
    let startX = 0;
    let startY = 0;
    let previousX = 0;
    let previousY = 0;
    let velocityYaw = 0;
    let velocityPitch = 0;
    let previousTime = 0;
    let activeMotionItem = null;
    let activeMotionVideo = 0;
    let motionVisible = false;
    let motionSwapToken = 0;

    const updateMotionMeta = (item) => {
      if (motionLabel && item.dataset.motionLabel) motionLabel.textContent = item.dataset.motionLabel;
      if (motionCredit && item.dataset.motionCredit) motionCredit.href = item.dataset.motionCredit;
    };
    const syncMotionPlayback = () => {
      motionVideos.forEach((video, index) => {
        if (allowMotionPreview && motionVisible && !manualPause && index === activeMotionVideo) {
          video.play().catch(() => {});
        } else {
          video.pause();
        }
      });
    };
    const setMotionItem = (item, force = false) => {
      if (!item?.dataset.motionSrc || (!force && item === activeMotionItem)) return;
      activeMotionItem = item;
      updateMotionMeta(item);

      const poster = item.dataset.motionPoster || '';
      if (!allowMotionPreview || !motionVisible) {
        const current = motionVideos[activeMotionVideo];
        if (current && poster) current.poster = poster;
        return;
      }

      const token = ++motionSwapToken;
      const nextIndex = activeMotionVideo === 0 ? 1 : 0;
      const next = motionVideos[nextIndex];
      const previous = motionVideos[activeMotionVideo];
      next.classList.remove('is-active');
      if (poster) next.poster = poster;
      if (next.getAttribute('src') !== item.dataset.motionSrc) {
        next.src = item.dataset.motionSrc;
        next.load();
      }
      const reveal = () => {
        if (token !== motionSwapToken) return;
        if (!manualPause) next.play().catch(() => {});
        next.classList.add('is-active');
        previous.classList.remove('is-active');
        activeMotionVideo = nextIndex;
        window.setTimeout(() => {
          if (previous !== motionVideos[activeMotionVideo]) previous.pause();
        }, 950);
      };
      if (next.readyState >= 3) reveal();
      else next.addEventListener('canplay', reveal, { once: true });
    };

    const renderOrbit = () => {
      const cosYaw = Math.cos(yaw);
      const sinYaw = Math.sin(yaw);
      const cosPitch = Math.cos(pitch);
      const sinPitch = Math.sin(pitch);
      const radiusX = Math.min(orbitStage.clientWidth * .31, 350);
      const radiusY = Math.min(orbitStage.clientHeight * .33, 205);
      const radiusZ = Math.min(orbitStage.clientWidth * .24, 280);
      let frontMotionItem = null;
      let frontMotionDepth = -Infinity;
      points.forEach(({ item, x, y, z }) => {
        const rotatedX = x * cosYaw + z * sinYaw;
        const yawZ = -x * sinYaw + z * cosYaw;
        const rotatedY = y * cosPitch - yawZ * sinPitch;
        const rotatedZ = y * sinPitch + yawZ * cosPitch;
        const depth = (rotatedZ + 1) / 2;
        const scale = .68 + depth * .38;
        item.style.transform = `translate(-50%, -50%) translate3d(${(rotatedX * radiusX).toFixed(2)}px, ${(rotatedY * radiusY).toFixed(2)}px, ${(rotatedZ * radiusZ).toFixed(2)}px) scale(${scale.toFixed(3)})`;
        item.style.opacity = (.36 + depth * .64).toFixed(3);
        item.style.zIndex = String(Math.round(depth * 100));
        item.style.filter = depth < .35 ? 'saturate(.72) brightness(.68)' : 'none';
        if (item.dataset.motionSrc && rotatedZ > frontMotionDepth) {
          frontMotionDepth = rotatedZ;
          frontMotionItem = item;
        }
      });
      if (frontMotionItem) setMotionItem(frontMotionItem);
    };
    const syncOrbitToggle = () => {
      if (!toggleOrbit) return;
      toggleOrbit.setAttribute('aria-pressed', String(manualPause));
      toggleOrbit.setAttribute('aria-label', manualPause ? 'Play sphere and background motion' : 'Pause sphere and background motion');
      const icon = toggleOrbit.querySelector('i');
      icon?.classList.toggle('fa-pause', !manualPause);
      icon?.classList.toggle('fa-play', manualPause);
      syncMotionPlayback();
    };
    const resetPosition = () => {
      yaw = .18;
      pitch = -.12;
      velocityYaw = 0;
      velocityPitch = 0;
      renderOrbit();
    };
    const animateOrbit = (time) => {
      const elapsed = previousTime ? Math.min(time - previousTime, 40) : 16;
      previousTime = time;
      if (!dragging) {
        if (!manualPause && !hovering && !document.hidden) yaw += elapsed * .000085;
        if (!reduceMotion) {
          yaw += velocityYaw;
          pitch = Math.max(-.72, Math.min(.72, pitch + velocityPitch));
          velocityYaw *= .94;
          velocityPitch *= .9;
          if (Math.abs(velocityYaw) < .00005) velocityYaw = 0;
          if (Math.abs(velocityPitch) < .00005) velocityPitch = 0;
        }
      }
      renderOrbit();
      requestAnimationFrame(animateOrbit);
    };

    document.querySelectorAll('a[href="#journeys"], a[href^="#trip-"]').forEach((link) => link.setAttribute('href', '#orbit'));
    document.body.classList.add('has-orbit');
    document.documentElement.classList.toggle('motion-static', !allowMotionPreview);
    orbitStage.classList.add('orbit-ready');
    renderOrbit();
    syncOrbitToggle();
    requestAnimationFrame(animateOrbit);

    if (orbitSection && 'IntersectionObserver' in window) {
      const motionObserver = new IntersectionObserver(([entry]) => {
        motionVisible = entry.isIntersecting;
        if (motionVisible && activeMotionItem) setMotionItem(activeMotionItem, true);
        else syncMotionPlayback();
      }, { rootMargin: '120px 0px', threshold: .08 });
      motionObserver.observe(orbitSection);
    } else {
      motionVisible = true;
      if (activeMotionItem) setMotionItem(activeMotionItem, true);
    }

    orbitStage.addEventListener('pointerdown', (event) => {
      if (event.pointerType === 'mouse' && event.button !== 0) return;
      dragging = true;
      moved = false;
      startX = previousX = event.clientX;
      startY = previousY = event.clientY;
      velocityYaw = velocityPitch = 0;
      orbitStage.classList.add('is-dragging');
      orbitStage.setPointerCapture(event.pointerId);
    });
    orbitStage.addEventListener('pointermove', (event) => {
      if (!dragging) return;
      const dx = event.clientX - previousX;
      const dy = event.clientY - previousY;
      if (Math.hypot(event.clientX - startX, event.clientY - startY) > 5) moved = true;
      yaw += dx * .006;
      if (event.pointerType !== 'touch') pitch = Math.max(-.72, Math.min(.72, pitch - dy * .0045));
      velocityYaw = dx * .0012;
      velocityPitch = event.pointerType === 'touch' ? 0 : -dy * .0008;
      previousX = event.clientX;
      previousY = event.clientY;
      renderOrbit();
    });
    const endOrbitDrag = (event) => {
      if (!dragging) return;
      dragging = false;
      orbitStage.classList.remove('is-dragging');
      if (orbitStage.hasPointerCapture(event.pointerId)) orbitStage.releasePointerCapture(event.pointerId);
    };
    orbitStage.addEventListener('pointerup', endOrbitDrag);
    orbitStage.addEventListener('pointercancel', endOrbitDrag);
    orbitStage.addEventListener('click', (event) => {
      if (!moved) return;
      event.preventDefault();
      event.stopPropagation();
      moved = false;
    }, true);
    orbitStage.addEventListener('mouseenter', () => { hovering = true; });
    orbitStage.addEventListener('mouseleave', () => { hovering = false; });
    orbitStage.addEventListener('focusin', () => { hovering = true; });
    orbitStage.addEventListener('focusout', () => { hovering = false; });
    orbitStage.addEventListener('keydown', (event) => {
      const rotationKeys = ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', ' '];
      if (!rotationKeys.includes(event.key)) return;
      event.preventDefault();
      if (event.key === 'ArrowLeft') yaw -= .22;
      if (event.key === 'ArrowRight') yaw += .22;
      if (event.key === 'ArrowUp') pitch = Math.max(-.72, pitch - .14);
      if (event.key === 'ArrowDown') pitch = Math.min(.72, pitch + .14);
      if (event.key === 'Home') resetPosition();
      if (event.key === ' ') {
        manualPause = !manualPause;
        syncOrbitToggle();
      }
      renderOrbit();
    });
    toggleOrbit?.addEventListener('click', () => {
      manualPause = !manualPause;
      syncOrbitToggle();
    });
    resetOrbit?.addEventListener('click', resetPosition);
    if (reduceMotion && toggleOrbit) {
      toggleOrbit.disabled = true;
      toggleOrbit.setAttribute('aria-label', 'Automatic rotation disabled by motion preference');
    }
    window.addEventListener('resize', renderOrbit, { passive: true });
  }

  document.querySelectorAll('[data-carousel]').forEach((carousel) => {
    if (document.body.dataset.discoveryLayout === 'orbit' && carousel.closest('.journey-picker, .trip-showcase')) return;
    const rail = carousel.querySelector('[data-carousel-rail]');
    const previous = carousel.querySelector('[data-carousel-prev]');
    const next = carousel.querySelector('[data-carousel-next]');
    const toggle = carousel.querySelector('[data-carousel-toggle]');
    if (!rail) return;

    let timer = 0;
    let manuallyPaused = reduceMotion;
    let hovering = false;
    let dragging = false;
    let moved = false;
    let pointerStart = 0;
    let scrollStart = 0;

    const stepSize = () => {
      const item = rail.firstElementChild;
      if (!item) return rail.clientWidth * .8;
      const styles = getComputedStyle(rail);
      return item.getBoundingClientRect().width + (parseFloat(styles.columnGap || styles.gap) || 0);
    };
    const go = (direction) => {
      const max = rail.scrollWidth - rail.clientWidth;
      let left = rail.scrollLeft + direction * stepSize();
      if (direction > 0 && left >= max - 8) left = 0;
      if (direction < 0 && left <= 8) left = max;
      rail.scrollTo({ left, behavior: reduceMotion ? 'auto' : 'smooth' });
    };
    const stop = () => { window.clearInterval(timer); timer = 0; };
    const start = () => {
      stop();
      if (manuallyPaused || hovering || document.hidden || carousel.dataset.autoplay !== 'true') return;
      timer = window.setInterval(() => go(1), 4200);
    };
    const syncToggle = () => {
      if (!toggle) return;
      toggle.setAttribute('aria-pressed', String(manuallyPaused));
      toggle.setAttribute('aria-label', manuallyPaused ? 'Play carousel' : 'Pause carousel');
      const icon = toggle.querySelector('i');
      icon?.classList.toggle('fa-pause', !manuallyPaused);
      icon?.classList.toggle('fa-play', manuallyPaused);
    };

    previous?.addEventListener('click', () => { go(-1); start(); });
    next?.addEventListener('click', () => { go(1); start(); });
    toggle?.addEventListener('click', () => {
      manuallyPaused = !manuallyPaused;
      syncToggle();
      start();
    });
    carousel.addEventListener('mouseenter', () => { hovering = true; stop(); });
    carousel.addEventListener('mouseleave', () => { hovering = false; start(); });
    carousel.addEventListener('focusin', stop);
    carousel.addEventListener('focusout', start);
    rail.addEventListener('keydown', (event) => {
      if (!['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
      event.preventDefault();
      go(event.key === 'ArrowRight' ? 1 : -1);
    });
    rail.addEventListener('pointerdown', (event) => {
      if (event.pointerType === 'mouse' && event.button !== 0) return;
      dragging = true;
      moved = false;
      pointerStart = event.clientX;
      scrollStart = rail.scrollLeft;
      rail.classList.add('is-dragging');
      rail.setPointerCapture(event.pointerId);
      stop();
    });
    rail.addEventListener('pointermove', (event) => {
      if (!dragging) return;
      const distance = event.clientX - pointerStart;
      if (Math.abs(distance) > 4) moved = true;
      rail.scrollLeft = scrollStart - distance;
    });
    const endDrag = (event) => {
      if (!dragging) return;
      dragging = false;
      rail.classList.remove('is-dragging');
      if (rail.hasPointerCapture(event.pointerId)) rail.releasePointerCapture(event.pointerId);
      start();
    };
    rail.addEventListener('pointerup', endDrag);
    rail.addEventListener('pointercancel', endDrag);
    rail.addEventListener('click', (event) => {
      if (!moved) return;
      event.preventDefault();
      event.stopPropagation();
      moved = false;
    }, true);
    document.addEventListener('visibilitychange', start);
    syncToggle();
    start();
  });

  if (!reduceMotion && 'IntersectionObserver' in window) {
    const observed = document.querySelectorAll('.intro__inner, .quote-rail, .section-heading, .carousel-shell, .host-options__grid, .story-row__copy, .story-row__media, .why__grid, .final-cta > div');
    document.documentElement.classList.add('motion-ready');
    const observer = new IntersectionObserver((entries, instance) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        instance.unobserve(entry.target);
      });
    }, { threshold: .12 });
    observed.forEach((element) => observer.observe(element));
  }
})();
