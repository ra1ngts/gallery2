<script>
  import { onMount, tick } from 'svelte';
  import { fly, fade } from 'svelte/transition';
  import { stateCtx } from '../../store.svelte';
  import { routeChoice } from '../../utils';

  import Main from './Main.svelte';
  import Category from './Category.svelte';
  import About from './About.svelte';
  import Contact from './Contact.svelte';
  import Loader from './Loader.svelte';
  import Toast from './Toast.svelte';
  import enFlag from 'svg/en.svg';
  import ruFlag from 'svg/ru.svg';

  const getMain = async (lang = '') => {
    try {
      stateCtx.page = stateCtx.pages.loading;

      const url = lang ? `/?lang=${lang}` : '/';

      const response = await fetch(url, {
        method: 'GET',
        headers: {
          Accept: 'application/json',
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      if (data.status === 'success') {
        stateCtx.profile = data.profile;
        stateCtx.artworks = data.artworks;
        stateCtx.featuredWork = data.featured_work;
        stateCtx.categories = data.categories;
        stateCtx.form = data.form;
        stateCtx.translation = data.translation;
        stateCtx.locale = data.locale;
        stateCtx.page = stateCtx.pages.main;
        console.log('index (GET) successfully sending:', data);
      } else {
        stateCtx.page = stateCtx.pages.main;
        console.error('index (GET) sending error:', data);
      }
    } catch (error) {
      console.error('Fetch error:', error);
    }
  };

  let isOpen = $state(false);

  const toggleMobileMenu = () => {
    isOpen = !isOpen;
  };

  const closeMobileMenu = () => {
    isOpen = false;
  };

  let isCategoryOpen = $state(false);

  const goToCategory = () => {
    isCategoryOpen = !isCategoryOpen;
  };

  const closeGoToCategory = () => {
    isCategoryOpen = false;
  };

  const menuSections = $derived([
    { id: 'main', title: stateCtx.translation?.app.sectionTitle.main },
    { id: 'category', title: stateCtx.translation?.app.sectionTitle.category },
    { id: 'about', title: stateCtx.translation?.app.sectionTitle.about },
    { id: 'contact', title: stateCtx.translation?.app.sectionTitle.contact },
  ]);

  async function scrollTo(id) {
    if (stateCtx.page !== stateCtx.pages.main) {
      stateCtx.page = stateCtx.pages.main;
      await tick();
    }

    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  }

  onMount(() => {
    getMain();
  });

  $effect(() => {
    const currentPage = stateCtx.page;
    if (currentPage !== stateCtx.pages.main) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            stateCtx.activeSection = entry.target.id;
          }
        });
      },
      {
        rootMargin: '-20px 0px -60% 0px',
        threshold: 0,
      },
    );

    setTimeout(() => {
      menuSections.forEach((section) => {
        const el = document.getElementById(section.id);
        if (el) {
          observer.observe(el);
        }
      });
    }, 50);

    return () => {
      observer.disconnect();
    };
  });

  let mouseX = $state(-100);
  let mouseY = $state(-100);
  let isHovered = $state(false);
  let isFancyboxOpen = $state(false);

  function handleMouseMove(e) {
    mouseX = e.clientX;
    mouseY = e.clientY;

    const target = e.target;
    if (!target) return;

    isFancyboxOpen = !!document.querySelector('.fancybox__container');

    const isClickable =
      target.closest('a') ||
      target.closest('button') ||
      target.closest('[role="button"]') ||
      target.closest('.swiper-button-next') ||
      target.closest('.swiper-button-prev') ||
      target.closest('.swiper-pagination-bullet');

    isHovered = !!isClickable;
  }

  let isLangSwitcherOpen = $state(false);

  const avalibleLanguages = [
    { code: 'en', url: enFlag },
    { code: 'ru', url: ruFlag },
  ];

  let currentLanguage = $derived(avalibleLanguages.find((l) => l.code === stateCtx.locale) || avalibleLanguages[0]);

  const selectLanguage = (code) => {
    getMain(code);
    isLangSwitcherOpen = false;
  };
</script>

<svelte:window onclick={closeGoToCategory} onmousemove={handleMouseMove} />

{#if stateCtx.page === stateCtx.pages.loading}
  <Loader />
{:else}
  {#if !isFancyboxOpen}
    <div
      class="fixed pointer-events-none rounded-full border-2"
      style="
    z-index: 9999999;
    transform: translate(calc({mouseX}px - 50%), calc({mouseY}px - 50%));
    transition: width 0.3s ease-out, height 0.3s ease-out, background-color 0.3s ease-out;
    width: {isHovered ? '24px' : '20px'}; 
    height: {isHovered ? '24px' : '20px'};
    background-color: {isHovered ? 'rgba(255, 255, 255, 0.15)' : 'rgba(255, 255, 255, 0.05)'};
    border-color: #ffffff;
    box-shadow: 0 0 10px 2px rgba(255, 255, 255, 0.35);
  "
    >
      <div
        class="absolute inset-0 rounded-full transition-opacity duration-700 ease-out"
        style="
      opacity: {isHovered ? '1' : '0'};
      box-shadow: 
        0 0 25px 6px rgba(255, 255, 255, 0.8), 
        0 0 50px 15px rgba(255, 255, 255, 0.35), 
        inset 0 0 8px rgba(255, 255, 255, 0.6);
    "
      ></div>
    </div>
  {/if}

  <div class="fixed top-0 z-100 w-full bg-linear-to-b from-gray-950/90 to-purple-950/60 backdrop-blur-md">
    <div class="container p-4">
      <nav class="flex items-center justify-between gap-4">
        <div
          transition:fade={{ duration: 1500 }}
          class="flex items-center gap-2 md:gap-4 font-bold text-2xl bg-linear-to-r from-purple-400 to-purple-700 bg-clip-text text-transparent sm:[&_svg]:h-7 sm:[&_svg]:w-7 [&_svg]:h-6 [&_svg]:w-6 [&_svg]:fill-purple-500 [&_svg]:hover:fill-purple-400 [&_svg]:transition-colors [&_svg]:duration-300"
        >
          {#if stateCtx.profile}
            {#if stateCtx.profile?.name || stateCtx.profile?.lastname}
              <div class="text-sm sm:text-2xl">{stateCtx.profile.name ?? ''} {stateCtx.profile.lastname ?? ''}</div>
            {/if}

            <div class="flex gap-2">
              {#if stateCtx.profile.whatsapp}
                <a
                  href={stateCtx.profile.whatsapp}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={stateCtx.profile.whatsapp}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640"
                    ><path
                      d="M476.9 161.1C435 119.1 379.2 96 319.9 96C197.5 96 97.9 195.6 97.9 318C97.9 357.1 108.1 395.3 127.5 429L96 544L213.7 513.1C246.1 530.8 282.6 540.1 319.8 540.1L319.9 540.1C442.2 540.1 544 440.5 544 318.1C544 258.8 518.8 203.1 476.9 161.1zM319.9 502.7C286.7 502.7 254.2 493.8 225.9 477L219.2 473L149.4 491.3L168 423.2L163.6 416.2C145.1 386.8 135.4 352.9 135.4 318C135.4 216.3 218.2 133.5 320 133.5C369.3 133.5 415.6 152.7 450.4 187.6C485.2 222.5 506.6 268.8 506.5 318.1C506.5 419.9 421.6 502.7 319.9 502.7zM421.1 364.5C415.6 361.7 388.3 348.3 383.2 346.5C378.1 344.6 374.4 343.7 370.7 349.3C367 354.9 356.4 367.3 353.1 371.1C349.9 374.8 346.6 375.3 341.1 372.5C308.5 356.2 287.1 343.4 265.6 306.5C259.9 296.7 271.3 297.4 281.9 276.2C283.7 272.5 282.8 269.3 281.4 266.5C280 263.7 268.9 236.4 264.3 225.3C259.8 214.5 255.2 216 251.8 215.8C248.6 215.6 244.9 215.6 241.2 215.6C237.5 215.6 231.5 217 226.4 222.5C221.3 228.1 207 241.5 207 268.8C207 296.1 226.9 322.5 229.6 326.2C232.4 329.9 268.7 385.9 324.4 410C359.6 425.2 373.4 426.5 391 423.9C401.7 422.3 423.8 410.5 428.4 397.5C433 384.5 433 373.4 431.6 371.1C430.3 368.6 426.6 367.2 421.1 364.5z"
                    /></svg
                  >
                </a>
              {/if}

              {#if stateCtx.profile.telegram}
                <a
                  href={stateCtx.profile.telegram}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={stateCtx.profile.telegram}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640"
                    ><path
                      d="M320 72C183 72 72 183 72 320C72 457 183 568 320 568C457 568 568 457 568 320C568 183 457 72 320 72zM435 240.7C431.3 279.9 415.1 375.1 406.9 419C403.4 437.6 396.6 443.8 390 444.4C375.6 445.7 364.7 434.9 350.7 425.7C328.9 411.4 316.5 402.5 295.4 388.5C270.9 372.4 286.8 363.5 300.7 349C304.4 345.2 367.8 287.5 369 282.3C369.2 281.6 369.3 279.2 367.8 277.9C366.3 276.6 364.2 277.1 362.7 277.4C360.5 277.9 325.6 300.9 258.1 346.5C248.2 353.3 239.2 356.6 231.2 356.4C222.3 356.2 205.3 351.4 192.6 347.3C177.1 342.3 164.7 339.6 165.8 331C166.4 326.5 172.5 322 184.2 317.3C256.5 285.8 304.7 265 328.8 255C397.7 226.4 412 221.4 421.3 221.2C423.4 221.2 427.9 221.7 430.9 224.1C432.9 225.8 434.1 228.2 434.4 230.8C434.9 234 435 237.3 434.8 240.6z"
                    /></svg
                  >
                </a>
              {/if}

              {#if stateCtx.profile.email}
                <a class="group" href="mailto:{stateCtx.profile.email}" aria-label="Mail to: {stateCtx.profile.email}">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640"
                    ><path
                      d="M320 128C214 128 128 214 128 320C128 426 214 512 320 512C337.7 512 352 526.3 352 544C352 561.7 337.7 576 320 576C178.6 576 64 461.4 64 320C64 178.6 178.6 64 320 64C461.4 64 576 178.6 576 320L576 352C576 405 533 448 480 448C450.7 448 424.4 434.8 406.8 414.1C384 435.1 353.5 448 320 448C249.3 448 192 390.7 192 320C192 249.3 249.3 192 320 192C347.9 192 373.7 200.9 394.7 216.1C400.4 211.1 407.8 208 416 208C433.7 208 448 222.3 448 240L448 352C448 369.7 462.3 384 480 384C497.7 384 512 369.7 512 352L512 320C512 214 426 128 320 128zM384 320C384 284.7 355.3 256 320 256C284.7 256 256 284.7 256 320C256 355.3 284.7 384 320 384C355.3 384 384 355.3 384 320z"
                    /></svg
                  >
                </a>
              {/if}

              {#if stateCtx.profile.cv}
                <a
                  href={stateCtx.profile.cv}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={stateCtx.profile.cv}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640"
                    ><path
                      d="M304 112L192 112C183.2 112 176 119.2 176 128L176 512C176 520.8 183.2 528 192 528L448 528C456.8 528 464 520.8 464 512L464 272L376 272C336.2 272 304 239.8 304 200L304 112zM444.1 224L352 131.9L352 200C352 213.3 362.7 224 376 224L444.1 224zM128 128C128 92.7 156.7 64 192 64L325.5 64C342.5 64 358.8 70.7 370.8 82.7L493.3 205.3C505.3 217.3 512 233.6 512 250.6L512 512C512 547.3 483.3 576 448 576L192 576C156.7 576 128 547.3 128 512L128 128z"
                    /></svg
                  >
                </a>
              {/if}
            </div>
          {/if}
        </div>

        <!-- Desktop menu -->
        <div class="hidden md:flex items-center gap-4 overflow-visible">
          {#if isLangSwitcherOpen}
            <div class="overlay" onclick={() => false} role="presentation"></div>
          {/if}

          <div class="custom-select">
            <button class="select-trigger" onclick={() => (isLangSwitcherOpen = !isLangSwitcherOpen)}>
              <img src={currentLanguage.url} alt={currentLanguage.code} class="flag-icon" />
              <span class="label">{currentLanguage.code}</span>
              <span class="arrow" class:rotated={isLangSwitcherOpen}>▼</span>
            </button>

            {#if isLangSwitcherOpen}
              <ul class="select-options">
                {#each avalibleLanguages as lang}
                  <li>
                    <button
                      class="option-btn"
                      class:selected={lang.code === stateCtx.locale}
                      onclick={() => selectLanguage(lang.code)}
                    >
                      <img src={lang.url} alt={lang.code} class="flag-icon" />
                      <span>{lang.code}</span>
                    </button>
                  </li>
                {/each}
              </ul>
            {/if}
          </div>

          {#each menuSections as section}
            {#if section.id !== 'category'}
              <div class="flex gap-2 relative">
                <button
                  class="neon-glow-hover text-xl font-semibold {stateCtx.page === stateCtx.pages.main &&
                  stateCtx.activeSection === section.id
                    ? 'neon-glow-active'
                    : 'text-purple-700 cursor-pointer'}"
                  onclick={() => scrollTo(section.id)}>{section.title}</button
                >
              </div>
            {/if}

            {#if section.id === 'category'}
              <div class="relative inline-block" onclick={(e) => e.stopPropagation()} aria-hidden="true">
                <button
                  class="neon-glow-hover text-xl font-semibold cursor-pointer {stateCtx.page === section.id
                    ? 'neon-glow-active'
                    : 'text-purple-700'}"
                  onclick={goToCategory}
                >
                  {section.title}
                </button>
                {#if isCategoryOpen}
                  <div
                    transition:fly={{ y: -10, duration: 300 }}
                    class="min-w-50 absolute left-1/2 -translate-x-1/2 mt-5 p-3 bg-gray-950/90 backdrop-blur-md rounded-3xl shadow-purple-500/30 shadow-2xl"
                  >
                    {#each stateCtx.categories as category}
                      <div>
                        <button
                          class="w-full p-2 rounded-2xl neon-glow-hover hover:bg-purple-950 text-sm sm:text-base md:text-xl font-semibold {stateCtx.categorySlug ===
                          category.slug
                            ? 'neon-glow-active'
                            : 'text-purple-700 cursor-pointer'}"
                          onclick={() => (routeChoice({ page: section.id, slug: category.slug }), closeGoToCategory())}
                          >{category.title}</button
                        >
                      </div>
                    {/each}
                  </div>
                {/if}
              </div>
            {/if}
          {/each}
        </div>

        <!-- Mobile menu -->
        <div class="flex md:hidden items-center relative">
          <button class="text-purple-500 focus:outline-none" aria-label="mobile-menu" onclick={toggleMobileMenu}>
            <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {#if !isOpen}
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              {:else}
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              {/if}
            </svg>
          </button>
        </div>
      </nav>
    </div>
  </div>

  <!-- Mobile menu -->
  {#if isOpen}
    <div
      transition:fly={{ y: -50, duration: 300 }}
      class="fixed inset-0 z-90 pt-20 bg-purple-900/20 bg-linear-to-b from-gray-950/90 to-purple-950/60 backdrop-blur-md p-4"
    >
      <div class="flex flex-col gap-4">
        {#each menuSections as section}
          {#if section.id !== 'category'}
            <div class="relative">
              <button
                class="neon-glow-hover text-xl font-semibold {stateCtx.page === stateCtx.pages.main &&
                stateCtx.activeSection === section.id
                  ? 'neon-glow-active'
                  : 'text-purple-700 cursor-pointer'}"
                onclick={() => {
                  scrollTo(section.id);
                  closeMobileMenu();
                }}>{section.title}</button
              >
            </div>
          {/if}

          {#if section.id === 'category'}
            <div class="relative">
              <button class="neon-glow-hover text-xl font-semibold text-purple-700" onclick={goToCategory}>
                {section.title}
              </button>

              <div class="my-2 space-y-2">
                {#each stateCtx.categories as category}
                  <button
                    class="
                    block
                    w-full
                    text-left
                    p-2
                    pl-6
                    rounded-3xl
                    neon-glow-hover
                    hover:bg-purple-950
                    text-base
                    font-semibold
                    {stateCtx.categorySlug === category.slug ? 'neon-glow-active' : 'text-purple-700'}
                  "
                    onclick={() => (
                      routeChoice({
                        page: section.id,
                        slug: category.slug,
                      }),
                      closeGoToCategory(),
                      closeMobileMenu()
                    )}
                  >
                    {category.title}
                  </button>
                {/each}
              </div>
            </div>
          {/if}
        {/each}
      </div>
    </div>
  {/if}

  <div class="container pt-20">
    {#if stateCtx.page === stateCtx.pages.main}
      <section id="main" class="scroll-mt-20">
        <Main />
      </section>

      <section id="about" class="pb-4 scroll-mt-20">
        <About />
      </section>

      <section id="contact" class="scroll-mt-20">
        <Contact />
      </section>
    {:else if stateCtx.page === stateCtx.pages.category}
      <Category />
      <!-- {:else if stateCtx.page === stateCtx.pages.loading}
      <Loader /> -->
    {/if}

    <footer>
      <div
        class="flex flex-col sm:flex-row py-8 items-center justify-center text-purple-950 gap-2 transition-colors duration-300 group"
      >
        <a
          href="mailto:{stateCtx.profile.email}"
          class="flex items-center gap-2 text-xs sm:text-base transition-colors duration-300 group-hover:text-purple-400"
          aria-label="Mail to: {stateCtx.profile.email}"
        >
          <svg
            class="h-7 w-7 fill-purple-950 transition-colors duration-300 group-hover:fill-purple-400"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12.24 15.25C13.02 15.25 13.79 14.96 14.38 14.44C14.69 14.17 15.17 14.2 15.44 14.51C15.71 14.82 15.68 15.3 15.37 15.57C14.5 16.34 13.39 16.76 12.24 16.76C9.62 16.76 7.49 14.63 7.49 12.01C7.49 9.39 9.62 7.26 12.24 7.26C13.39 7.26 14.51 7.68 15.37 8.45C15.68 8.72 15.71 9.2 15.44 9.51C15.16 9.82 14.69 9.85 14.38 9.58C13.79 9.06 13.03 8.77 12.24 8.77C10.45 8.77 8.99 10.23 8.99 12.02C8.99 13.81 10.45 15.25 12.24 15.25Z"
            />
          </svg>

          {new Date().getFullYear()}
          {stateCtx.profile?.name}
          {stateCtx.profile?.lastname}.
        </a>

        <a
          href="mailto:david.khurts@gmail.com"
          class="flex items-center gap-2 text-xs sm:text-base transition-colors duration-300 group-hover:text-purple-400"
          aria-label="Mail to: david.khurts@gmail.com"
        >
          {stateCtx.translation?.app.copyright}
          <svg
            class="h-7 w-7 fill-purple-950 transition-colors duration-300 group-hover:fill-purple-400"
            version="1.0"
            xmlns="http://www.w3.org/2000/svg"
            width="512.000000pt"
            height="512.000000pt"
            viewBox="0 0 512.000000 512.000000"
            preserveAspectRatio="xMidYMid meet"
          >
            <g transform="translate(0.000000,512.000000) scale(0.100000,-0.100000)">
              <path
                d="M3301 4675 c-35 -8 -87 -22 -115 -31 -160 -52 -426 -236 -587 -407
                -53 -56 -117 -117 -142 -134 l-45 -33 -114 104 c-207 187 -324 250 -515 276
                -270 36 -531 -96 -726 -368 -218 -305 -320 -748 -276 -1198 60 -617 355 -1219
                876 -1789 192 -210 520 -515 553 -515 38 0 60 19 60 50 0 25 -37 66 -241 272
                -456 458 -659 718 -836 1068 -213 421 -315 868 -284 1249 33 413 148 699 365
                917 90 90 199 153 303 174 88 19 243 8 325 -22 174 -65 317 -187 389 -333 l43
                -86 -34 -72 c-48 -106 -94 -247 -146 -451 -41 -156 -47 -196 -48 -286 -1 -86
                3 -118 22 -173 58 -166 162 -246 285 -216 125 30 222 200 246 431 14 147 -4
                278 -88 623 l-39 160 40 70 c67 117 147 221 237 308 135 130 261 207 431 263
                76 25 100 28 225 28 128 1 147 -1 228 -28 344 -113 545 -463 524 -911 -3 -74
                -14 -153 -28 -205 -37 -146 -211 -527 -340 -746 -127 -216 -391 -587 -694
                -974 -305 -390 -612 -839 -726 -1061 -30 -60 -80 -199 -70 -199 14 0 125 76
                148 101 11 13 45 60 74 104 153 233 562 812 968 1370 390 535 474 662 565 848
                228 465 285 814 190 1168 -86 322 -314 564 -609 645 -83 23 -309 28 -394 9z
                m-851 -1087 c57 -121 73 -207 74 -378 0 -143 -2 -161 -27 -237 -30 -90 -61
                -134 -107 -153 -42 -17 -86 10 -119 75 -25 47 -26 58 -26 200 1 134 4 160 28
                240 26 83 130 315 143 315 3 0 18 -28 34 -62z"
              />
            </g>
          </svg>
        </a>
      </div>
    </footer>
  </div>
{/if}

<style>
  :global(body),
  :global(body *) {
    cursor: none !important;
  }
  :global(.fancybox__container),
  :global(.fancybox__container *) {
    cursor: auto !important;
  }
  :global(.fancybox__container a),
  :global(.fancybox__container button),
  :global(.fancybox__container .f-button) {
    cursor: pointer !important;
  }
  .custom-select {
    position: relative;
    width: 60px;
    z-index: 999;
  }
  .select-trigger {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    padding: 6px;
    background: #ffffff;
    border: 1px solid #ccc;
    border-radius: 6px;
    cursor: pointer;
  }
  .flag-icon {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    object-fit: cover;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
  }
  .arrow {
    font-size: 8px;
    color: #666;
    transition: transform 0.2s ease;
  }
  .arrow.rotated {
    transform: rotate(180deg);
  }
  .select-options {
    position: absolute;
    top: 110%;
    left: 0;
    width: 100%;
    background: #ffffff;
    border: 1px solid #ccc;
    border-radius: 6px;
    margin: 0;
    padding: 4px 0;
    list-style: none;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
  }
  .option-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    padding: 6px 0;
    background: none;
    border: none;
    cursor: pointer;
  }
  .option-btn:hover {
    background-color: #f5f5f5;
  }
  .option-btn.selected {
    background-color: #e6f7ff;
  }
  .overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 99;
  }
</style>
