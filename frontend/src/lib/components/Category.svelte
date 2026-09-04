<script>
  import { fly, fade } from 'svelte/transition';
  import { stateCtx } from '../../store.svelte';
  import { BalancedMasonryGrid as MasonryGrid, Frame } from '@masonry-grid/svelte';

  import { Fancybox } from '@fancyapps/ui/dist/fancybox/';
  import '@fancyapps/ui/dist/fancybox/fancybox.css';
  import '@fancyapps/ui/dist/carousel/carousel.css';

  const getRandomSize = () => Math.floor(Math.random() * 3) + 2;

  Fancybox.bind("[data-fancybox^='artwork-gallery']", {
    hideScrollbar: false,
    wheel: 'slide',
    backdropClick: 'close',
    Hash: false,
    Carousel: {
      Toolbar: {
        display: {
          left: ['counter'],
          middle: [],
          right: ['toggle1to1', 'thumbs', 'autoplay', 'close'],
        },
      },
    },
  });

  let defaultYear = stateCtx.translation?.category.all_years;
  let selectedYear = $state(defaultYear);

  let defaultSelectedMedium = stateCtx.translation?.category.all_mediums;
  let selectedMedium = $state(defaultSelectedMedium);

  const years = $derived([
    defaultYear,
    ...[...new Set(stateCtx.artworksCategory.map((y) => y.year))].sort((a, b) => b - a),
  ]);
  $inspect('years', years);

  const mediums = $derived([
    defaultSelectedMedium,
    ...[...new Set(stateCtx.artworksCategory.map((t) => t.medium?.title))],
  ]);
  $inspect('mediums', mediums);

  const isYearsFiltersShown = $derived(
    years.filter((item) => item !== stateCtx.translation?.category.all_years).length,
  );
  $inspect('isYearsFiltersShown', isYearsFiltersShown);

  const isMediumsFiltersShown = $derived(
    mediums.filter((item) => item !== stateCtx.translation?.category.all_mediums).length,
  );
  $inspect('isMediumsFiltersShown', isMediumsFiltersShown);

  const isFiltersShown = $derived(isYearsFiltersShown > 1 || isMediumsFiltersShown > 1);
  $inspect('isFiltersShown', isFiltersShown);

  const filteredArtworks = $derived(
    stateCtx.artworksCategory.filter((artwork) => {
      const matchYear = selectedYear === defaultYear || artwork.year === selectedYear;
      const matchMedium = selectedMedium === defaultSelectedMedium || artwork.medium.title === selectedMedium;
      return matchYear && matchMedium;
    }),
  );
  $inspect('filteredArtworks', filteredArtworks);

  let isShown = $state(false);

  const isDesktop = () => {
    isShown = !isShown;
  };

  const closeMobileMenu = () => {
    isShown = false;
  };
</script>

{#if filteredArtworks.length > 0}
  <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
    {#if isFiltersShown}
      <div
        class="hidden md:block md:col-span-1 h-fit p-2 lg:p-4 rounded-3xl transition-all duration-300 bg-purple-950/20 hover:bg-purple-950/25"
      >
        <div class="grid grid-cols-1 gap-4">
          <div class="rounded-3xl bg-purple-950/25">
            <div class="mt-2 text-purple-400 font-bold text-center text-sm lg:text-base">
              {stateCtx.translation?.category.year}
            </div>
            <div class="p-2 flex flex-col gap-1">
              {#each years as year}
                <button
                  onclick={() => (selectedYear = year)}
                  class="block w-full p-2 transition-all duration-300 hover:p-2 hover:rounded-2xl text-sm lg:text-base
                  {selectedYear === year
                    ? 'text-purple-400 bg-purple-950 rounded-2xl'
                    : 'cursor-pointer text-purple-500 hover:text-purple-400 hover:bg-purple-950'}"
                >
                  {year}
                </button>
              {/each}
            </div>
          </div>

          <div class="rounded-3xl bg-purple-950/25">
            <div class="mt-2 text-purple-400 font-bold text-center text-sm lg:text-base">
              {stateCtx.translation?.category.medium}
            </div>
            <div class="p-2 flex flex-col gap-1">
              {#each mediums as medium}
                <button
                  onclick={() => (selectedMedium = medium)}
                  class="block w-full p-2 transition-all duration-300 hover:p-2 hover:rounded-2xl text-sm lg:text-base
                  {selectedMedium === medium
                    ? 'text-purple-400 bg-purple-950 rounded-2xl'
                    : 'cursor-pointer text-purple-500 hover:text-purple-400 hover:bg-purple-950'}"
                >
                  {medium}
                </button>
              {/each}
            </div>
          </div>
        </div>
      </div>
    {/if}

    <div class="col-span-1 {isFiltersShown ? 'md:col-span-4' : 'md:col-span-5'} w-full">
      <div
        class="w-full p-2 md:p-4 mb-4 bg-purple-950/20 transition-colors duration-300 text-purple-400 rounded-3xl text-xl font-semibold text-center flex items-center {isFiltersShown
          ? 'justify-between'
          : 'justify-center'} md:block md:text-center gap-4"
      >
        {#if isFiltersShown}
          <button
            onclick={() => isDesktop()}
            class="md:hidden bg-linear-to-t from-purple-500 to-purple-400 hover:from-purple-400 hover:to-purple-300 text-purple-900 font-bold rounded-2xl transition-colors duration-300 shadow-lg shadow-purple-400/30 py-1 px-4"
            >{stateCtx.translation?.category.filters}
          </button>
        {/if}
        {stateCtx.categoryTitle}
      </div>

      <!-- Mobile filters -->
      {#if isShown}
        <div transition:fly={{ y: -50, duration: 300 }} class="fixed inset-0 z-50 pt-20 p-4">
          <button
            type="button"
            aria-label="Close filters"
            onclick={closeMobileMenu}
            class="absolute inset-0 bg-purple-900/20 bg-linear-to-b from-gray-950/90 to-purple-950/60 backdrop-blur-md"
          ></button>
          <div class="relative z-10 flex flex-col gap-4">
            <div class="grid grid-cols-1 gap-4">
              <div class="rounded-3xl bg-purple-950/25 border-t border-t-purple-500/30 border-b border-b-purple-950/60">
                <div class="mt-2 text-purple-400 font-bold text-center text-base sm:text-lg">
                  {stateCtx.translation?.category.year}
                </div>
                <div class="p-2 flex flex-col gap-1">
                  {#each years as year}
                    <button
                      onclick={() => (selectedYear = year)}
                      class="block w-full p-2 transition-all duration-300 hover:p-2 hover:rounded-2xl text-base sm:text-lg
                        {selectedYear === year
                        ? 'text-purple-400 bg-purple-950 rounded-2xl'
                        : 'cursor-pointer text-purple-500 hover:text-purple-400 hover:bg-purple-950'}"
                    >
                      {year}
                    </button>
                  {/each}
                </div>
              </div>

              <div class="rounded-3xl bg-purple-950/25 border-t border-t-purple-500/30 border-b border-b-purple-950/60">
                <div class="mt-2 text-purple-400 font-bold text-center text-base sm:text-lg">
                  {stateCtx.translation?.category.medium}
                </div>
                <div class="p-2 flex flex-col gap-1">
                  {#each mediums as medium}
                    <button
                      onclick={() => (selectedMedium = medium)}
                      class="block w-full p-2 transition-all duration-300 hover:p-2 hover:rounded-2xl text-base sm:text-lg
                        {selectedMedium === medium
                        ? 'text-purple-400 bg-purple-950 rounded-2xl'
                        : 'cursor-pointer text-purple-500 hover:text-purple-400 hover:bg-purple-950'}"
                    >
                      {medium}
                    </button>
                  {/each}
                </div>
              </div>

              <button
                onclick={() => closeMobileMenu()}
                class="block w-full p-2 text-lg sm:text-xl text-center bg-linear-to-t from-purple-500 to-purple-400 hover:from-purple-400 hover:to-purple-300 text-purple-900 font-bold rounded-2xl transition-colors duration-300 shadow-lg shadow-purple-400/30"
                >{stateCtx.translation?.category.show}
              </button>
            </div>
          </div>
        </div>
      {/if}

      <div transition:fade={{ duration: 500 }} class="w-full h-full">
        <MasonryGrid frameWidth={300} gap={15}>
          {#each filteredArtworks as artwork (artwork.id)}
            {@const randomW = getRandomSize()}
            {@const randomH = getRandomSize()}
            <Frame width={randomW} height={randomH}>
              <a
                href={artwork.image}
                data-fancybox="artwork-gallery"
                class="block w-full h-full cursor-pointer opacity-90 transition-opacity duration-300 ease-in-out hover:opacity-100"
              >
                <img
                  src={artwork.image}
                  alt={artwork.title}
                  class="block w-full h-full rounded-2xl object-cover cursor-pointer"
                  loading="lazy"
                />
              </a>
            </Frame>
          {/each}
        </MasonryGrid>
      </div>
    </div>
  </div>
{:else}
  <div class="flex w-full items-center justify-center">
    <div class="py-4 text-center">{stateCtx.translation?.category.warning}</div>
  </div>
{/if}
