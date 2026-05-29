<script>
  import { stateCtx } from '../../store.svelte';
  import { fade, fly } from 'svelte/transition';
</script>

{#if stateCtx.toast.show}
  <div
    in:fly={{ y: 50, duration: 300 }}
    out:fade
    class="fixed bottom-10 left-1/2 -translate-x-1/2 flex items-center p-5 mb-8 rounded-2xl shadow-2xl text-cyan-800 bg-cyan-400"
  >
    <div class="text-sm font-bold">
      {stateCtx.toast.message}
    </div>
    <button onclick={() => (stateCtx.toast.show = false)} class="ml-4 hover:opacity-70 transition-opacity"> ✕ </button>
  </div>
{/if}