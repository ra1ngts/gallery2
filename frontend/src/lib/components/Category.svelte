<script>
  import { fade } from 'svelte/transition';
  import { stateCtx } from '../../store.svelte';
  import { BalancedMasonryGrid as MasonryGrid, Frame } from '@masonry-grid/svelte';

  import { Fancybox } from '@fancyapps/ui/dist/fancybox/';
  import '@fancyapps/ui/dist/fancybox/fancybox.css';

  import '@fancyapps/ui/dist/carousel/carousel.css';

  const getRandomSize = () => Math.floor(Math.random() * 3) + 2;

  Fancybox.bind("[data-fancybox^='artwork-']", {
    hideScrollbar: true,
    wheel: 'slide',
    backdropClick: 'close',
    Hash: false,
  });

  let selectedYear = $state('All years');
  let selectedTechnique = $state('All techniques');

  const years = $derived(
    [selectedYear, ...new Set(stateCtx.artworksCategory.map((y) => y.year))].sort((a, b) => b - a),
  );
  console.log('years', years);

  const techniques = $derived([selectedTechnique, ...new Set(stateCtx.artworksCategory.map((t) => t.technique.title))]);
  console.log('techniques', techniques);
</script>

<div class="grid grid-cols-5 gap-4">
  <div class="col-span-1 h-fit p-4 rounded-2xl transition-all duration-300 bg-purple-950/20 hover:bg-purple-950/25">
    <div class="grid grid-cols-1 gap-4">
      <div class="rounded-2xl bg-purple-950/25">
        <div class="mt-2 text-purple-400 font-bold text-center">Year</div>
        <div class="p-2">
          {#each years as year}
            <div
              class="cursor-pointer p-2 transition-all duration-300 text-purple-500 hover:text-purple-400 hover:bg-purple-950 hover:p-2 hover:rounded-xl"
            >
              {year}
            </div>
          {/each}
        </div>
      </div>

      <div class="rounded-2xl bg-purple-950/25">
        <div class="mt-2 text-purple-400 font-bold text-center">Technique</div>
        <div class="p-2">
          {#each techniques as technique}
            <div
              class="cursor-pointer p-2 transition-all duration-300 text-purple-500 hover:text-purple-400 hover:bg-purple-950 hover:p-2 hover:rounded-xl"
            >
              {technique}
            </div>
          {/each}
        </div>
      </div>
    </div>
  </div>

  <div class="col-span-4">
    {#if stateCtx.artworksCategory.length > 0}
      <div transition:fade={{ duration: 500 }} class="w-full h-full">
        <MasonryGrid frameWidth={300} gap={15}>
          {#each stateCtx.artworksCategory as artwork}
            {@const randomW = getRandomSize()}
            {@const randomH = getRandomSize()}

            <Frame width={randomW} height={randomH}>
              <a
                href={artwork.image}
                data-fancybox="artwork-{artwork.id}"
                class="block w-full h-full cursor-pointer opacity-90 transition-opacity duration-300 ease-in-out hover:opacity-100"
              >
                <img
                  src={artwork.image}
                  alt={artwork.title}
                  class="block w-full h-full rounded-2xl object-cover cursor-pointer"
                />
              </a>
            </Frame>
          {/each}
        </MasonryGrid>
      </div>
    {:else}
      <div class="flex w-full items-center justify-center">
        <div class="text-center">No artworks available in current category</div>
      </div>
    {/if}
  </div>
</div>
