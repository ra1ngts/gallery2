<script>
  import { stateCtx } from '../../store.svelte';
</script>

<div class="">
  {#each stateCtx.artworksCategory as artwork}
    {artwork.title}
  {/each}
</div>
