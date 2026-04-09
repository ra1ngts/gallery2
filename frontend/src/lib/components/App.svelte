<script>
  import { onMount } from 'svelte';
  import { stateCtx } from '../../store.svelte';

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

  onMount(() => {
    getCtx();
  });
</script>

<div class="container">
  Test 2
</div>
