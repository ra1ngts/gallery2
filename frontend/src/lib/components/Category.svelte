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
</script>

{#if stateCtx.artworksCategory.length > 0}
  <div transition:fade={{ duration: 500 }} class="w-full h-full">
    <MasonryGrid frameWidth={300} gap={15}>
      {#each stateCtx.artworksCategory as artwork}
        {@const randomW = getRandomSize()}
        {@const randomH = getRandomSize()}

        <Frame width={randomW} height={randomH}>
          <a href={artwork.image} data-fancybox="artwork-{artwork.id}" class="block w-full h-full">
            <img src={artwork.image} alt={artwork.title} class="block w-full h-full object-cover cursor-pointer" />
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
