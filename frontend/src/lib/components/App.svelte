<script>
  import { onMount } from 'svelte';
  import { stateCtx } from '../../store.svelte';
  import Main from './Main.svelte';
  import Category from './Category.svelte';
  import Loader from './Loader.svelte';

  const getMain = async () => {
    try {
      stateCtx.page = stateCtx.pages.loading;

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
        stateCtx.categories = data.categories;
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

  const goToMain = () => {
    stateCtx.page = stateCtx.pages.main;
  };

  const getCategory = async (slug) => {
    try {
      stateCtx.page = stateCtx.pages.loading;

      const response = await fetch(`/${slug}/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      if (data.status === 'success') {
        stateCtx.page = stateCtx.pages.category;
        console.log('category (POST) successfully sending:', data);
      } else {
        stateCtx.page = stateCtx.pages.main;
        console.error('category (POST) sending error:', data);
      }
    } catch (error) {
      console.error('Error in getCategory has been caught:', error);
    }
  };

  onMount(() => {
    getMain();
  });
</script>

<div class="fixed top-0 z-100 w-full bg-linear-to-b from-gray-950/90 to-purple-950/40 backdrop-blur-md">
  <div class="container p-4">
    <nav class="flex justify-between items-center gap-2 overflow-x-auto no-scrollbar">
      <div class="text-white">
        <button onclick={goToMain}>main</button>

        {#each stateCtx.categories as category}
          <button onclick={() => getCategory(category.slug)}>{category.title}</button>
        {/each}
      </div>

      <!-- {#each stateCtx.menu as page}
        <button
          class="transition-colors duration-300 hover:text-purple-400 text-sm sm:text-base md:text-xl font-semibold {stateCtx.menu ===
          page.id
            ? 'text-purple-500'
            : 'text-gray-500 cursor-pointer'}"
        >
          {page.title}
        </button>
      {/each} -->
    </nav>
  </div>
</div>

<div class="container pt-20">
  {#if stateCtx.page === stateCtx.pages.main}
    <Main />
  {:else if stateCtx.page === stateCtx.pages.category}
    <Category />
  {:else if stateCtx.page === stateCtx.pages.loading}
    <Loader />
  {/if}
</div>
