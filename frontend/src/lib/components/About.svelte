<script>
  import { stateCtx } from '../../store.svelte';
</script>

<div class="w-full block py-4 mb-4 bg-purple-950/20 text-purple-500 rounded-2xl text-xl font-semibold text-center">
  {stateCtx.translation?.app.sectionTitle.about}
</div>

<div class="grid grid-cols-3 gap-4">
  <div class="h-full flex justify-center">
    <img
      src={stateCtx.profile.image}
      alt={stateCtx.profile.name}
      class="w-full h-full object-contain rounded-3xl opacity-90 hover:opacity-100 transition-all duration-300"
      loading="lazy"
    />
  </div>

  <div class="col-span-2 text-xs sm:text-base">{stateCtx.profile.description}</div>
</div>
