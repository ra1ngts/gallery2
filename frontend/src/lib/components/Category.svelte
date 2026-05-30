<script>
  import { fade } from 'svelte/transition';
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

  let defaultSelectedTechnique = stateCtx.translation?.category.all_techniques;
  let selectedTechnique = $state(defaultSelectedTechnique);

  const years = $derived([
    defaultYear,
    ...[...new Set(stateCtx.artworksCategory.map((y) => y.year))].sort((a, b) => b - a),
  ]);
  $inspect('years', years);

  const techniques = $derived([
    defaultSelectedTechnique,
    ...[...new Set(stateCtx.artworksCategory.map((t) => t.technique.title))],
  ]);
  $inspect('techniques', techniques);

  const filteredArtworks = $derived(
    stateCtx.artworksCategory.filter((artwork) => {
      const matchYear = selectedYear === defaultYear || artwork.year === selectedYear;
      const matchTechnique =
        selectedTechnique === defaultSelectedTechnique || artwork.technique.title === selectedTechnique;
      return matchYear && matchTechnique;
    }),
  );
  $inspect('filteredArtworks', filteredArtworks);
</script>

<div class="grid grid-cols-5 gap-4">
  <div class="col-span-1 h-fit p-4 rounded-2xl transition-all duration-300 bg-purple-950/20 hover:bg-purple-950/25">
    <div class="grid grid-cols-1 gap-4">
      <div class="rounded-2xl bg-purple-950/25">
        <div class="mt-2 text-purple-400 font-bold text-center">{stateCtx.translation?.category.year}</div>
        <div class="p-2 flex flex-col gap-1">
          {#each years as year}
            <button
              onclick={() => (selectedYear = year)}
              class="block w-full p-2 transition-all duration-300 hover:p-2 hover:rounded-xl
              {selectedYear === year
                ? 'text-purple-400 bg-purple-950 rounded-xl'
                : 'cursor-pointer text-purple-500 hover:text-purple-400 hover:bg-purple-950'}"
            >
              {year}
            </button>
          {/each}
        </div>
      </div>

      <div class="rounded-2xl bg-purple-950/25">
        <div class="mt-2 text-purple-400 font-bold text-center">{stateCtx.translation?.category.technique}</div>
        <div class="p-2 flex flex-col gap-1">
          {#each techniques as technique}
            <button
              onclick={() => (selectedTechnique = technique)}
              class="block w-full p-2 transition-all duration-300 hover:p-2 hover:rounded-xl
              {selectedTechnique === technique
                ? 'text-purple-400 bg-purple-950 rounded-xl'
                : 'cursor-pointer text-purple-500 hover:text-purple-400 hover:bg-purple-950'}"
            >
              {technique}
            </button>
          {/each}
        </div>
      </div>
    </div>
  </div>

  <div class="col-span-4">
    {#if filteredArtworks.length > 0}
      <div
        class="w-full block py-4 mb-4 bg-purple-950/20 transition-colors duration-300 text-purple-400 rounded-2xl text-xl font-semibold text-center"
      >
        {stateCtx.categoryTitle}
      </div>

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
    {:else}
      <div class="flex w-full items-center justify-center">
        <div class="text-center">{stateCtx.translation?.category.warning}</div>
      </div>
    {/if}
  </div>
</div>
