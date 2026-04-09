<script>
  import { onMount } from 'svelte';
  import { stateCtx } from '../../store.svelte';
  import Main from './Main.svelte';

  const getCtx = async () => {
    try {
      const response = await fetch('/', {
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
        stateCtx.artworks = data.artworks;
        console.log('index (GET) successfully sending:', data);
      } else {
        console.error('index (GET) sending error:', data);
      }
    } catch (error) {
      console.error('Fetch error:', error);
    }
  };

  function scrollTo(id) {
    const el = document.getElementById(id);

    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  }

  onMount(() => {
    getCtx();
  });
</script>

<div class="fixed top-0 z-100 w-full bg-linear-to-b from-black to-gray-900/40 backdrop-blur-md">
  <div class="container p-4">
    <nav class="flex justify-between items-center gap-2 overflow-x-auto no-scrollbar">
      {#each stateCtx.menu as section}
        <button
          onclick={() => scrollTo(section.id)}
          class="transition-colors duration-300 hover:text-purple-300 text-sm sm:text-base md:text-xl font-semibold {stateCtx.activeMenu ===
          section.id
            ? 'text-purple-500'
            : 'text-gray-500 cursor-pointer'}"
        >
          {section.title}
        </button>
      {/each}
    </nav>
  </div>
</div>

<div class="container pt-20">
  <div class="py2">
    <Main />
  </div>

  <div class="flex py-4 items-center justify-center text-gray-800 gap-2 transition-colors duration-300 group">
    <a
      href="mailto:#"
      class="flex items-center gap-2 transition-colors duration-300 group-hover:text-cyan-200 text-xs sm:text-lg"
      aria-label="Mail to:#"
    >
      <svg
        class="h-7 w-7 sm:h-8 sm:w-8 fill-gray-800 transition-colors duration-300 group-hover:fill-cyan-200"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12.24 15.25C13.02 15.25 13.79 14.96 14.38 14.44C14.69 14.17 15.17 14.2 15.44 14.51C15.71 14.82 15.68 15.3 15.37 15.57C14.5 16.34 13.39 16.76 12.24 16.76C9.62 16.76 7.49 14.63 7.49 12.01C7.49 9.39 9.62 7.26 12.24 7.26C13.39 7.26 14.51 7.68 15.37 8.45C15.68 8.72 15.71 9.2 15.44 9.51C15.16 9.82 14.69 9.85 14.38 9.58C13.79 9.06 13.03 8.77 12.24 8.77C10.45 8.77 8.99 10.23 8.99 12.02C8.99 13.81 10.45 15.25 12.24 15.25Z"
        />
      </svg>
      <div>
        {new Date().getFullYear()}
      </div>
    </a>
  </div>
</div>
