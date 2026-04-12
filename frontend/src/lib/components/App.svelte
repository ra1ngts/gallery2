<script>
  import { onMount } from 'svelte';
  import { fly, fade } from 'svelte/transition';
  import { stateCtx } from '../../store.svelte';

  import Main from './Main.svelte';
  import Category from './Category.svelte';
  import Contact from './Contact.svelte';
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
        stateCtx.featuredWork = data.featured_work;
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

  let isCategoryOpen = $state(false);

  const goToCategory = () => {
    isCategoryOpen = !isCategoryOpen;
  };

  const closeGoToCategory = () => {
    isCategoryOpen = false;
  };

  const routeChoice = (route) => {
    stateCtx.page = route.page;
    console.log(route.page);

    if (route.page === stateCtx.pages.category) {
      console.log('category route', route.page === stateCtx.pages.category);
      stateCtx.categorySlug = route.slug;
      console.log('category slug', route.slug);
      getCategory(route.slug);
    } else {
      stateCtx.categorySlug = null;
    }
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

<svelte:window onclick={closeGoToCategory} />

<div class="fixed top-0 z-100 w-full bg-linear-to-b from-gray-950/90 to-purple-950/60 backdrop-blur-md">
  <div class="container p-4">
    <nav class="grid grid-cols-2">
      <div
        transition:fade={{ duration: 1500 }}
        class="flex items-center font-bold text-2xl bg-linear-to-r from-purple-300 to-purple-950 bg-clip-text text-transparent"
      >
        Agata Khurtsidze
      </div>

      <div class="flex items-center gap-4 overflow-visible">
        {#each stateCtx.menu as item}
          {#if item.id !== 'category'}
            <div class="flex gap-2 relative">
              <button
                class="transition-colors duration-300 hover:text-purple-400 text-sm sm:text-base md:text-xl font-semibold {stateCtx.page ===
                item.id
                  ? 'text-purple-500'
                  : 'text-gray-400 cursor-pointer'}"
                onclick={() => routeChoice({ page: item.id })}>{item.title}</button
              >
            </div>
          {/if}

          {#if item.id === 'category'}
            <div class="relative inline-block" onclick={(e) => e.stopPropagation()} aria-hidden="true">
              <button
                class="transition-colors duration-300 hover:text-purple-400 text-sm sm:text-base md:text-xl font-semibold cursor-pointer {stateCtx.page ===
                item.id
                  ? 'text-purple-500'
                  : 'text-gray-400'}"
                onclick={goToCategory}
              >
                {item.title}
              </button>
              {#if isCategoryOpen}
                <div
                  transition:fly={{ y: -10, duration: 300 }}
                  class="min-w-50 absolute left-1/2 -translate-x-1/2 mt-5 p-4 bg-gray-950/90 backdrop-blur-md rounded-3xl shadow-purple-500/30 shadow-2xl"
                >
                  {#each stateCtx.categories as category}
                    <div>
                      <button
                        class="w-full transition-colors duration-300 px-3 py-1.5 rounded-2xl hover:bg-purple-950 hover:text-purple-400 text-sm sm:text-base md:text-xl font-semibold {stateCtx.categorySlug ===
                        category.slug
                          ? 'text-purple-500'
                          : 'text-gray-400 cursor-pointer'}"
                        onclick={() => (routeChoice({ page: item.id, slug: category.slug }), closeGoToCategory())}
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
    </nav>
  </div>
</div>

<div class="container pt-20">
  <!-- <div class="text-2xl font-bold text-white">
    {stateCtx.menu.find((m) => m.id === stateCtx.page)?.title}
  </div> -->

  {#if stateCtx.page === stateCtx.pages.main}
    <Main />
  {:else if stateCtx.page === stateCtx.pages.category}
    <Category />
  {:else if stateCtx.page === stateCtx.pages.contact}
    <Contact />
  {:else if stateCtx.page === stateCtx.pages.loading}
    <Loader />
  {/if}
</div>
