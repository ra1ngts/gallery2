<script>
  import { fade } from 'svelte/transition';
  import { stateCtx } from '../../store.svelte';
  import { routeChoice } from '../../utils';

  import Swiper from 'swiper';
  import { Navigation, Pagination, Mousewheel } from 'swiper/modules';
  import 'swiper/css';
  import 'swiper/css/navigation';
  import 'swiper/css/pagination';

  import { Fancybox } from '@fancyapps/ui/dist/fancybox/';
  import '@fancyapps/ui/dist/fancybox/fancybox.css';

  import { Carousel } from '@fancyapps/ui/dist/carousel/';
  import '@fancyapps/ui/dist/carousel/carousel.css';

  function swiperCreation(swiperObj) {
    const swiperArtworks = new Swiper(swiperObj, {
      modules: [Navigation, Pagination, Mousewheel],
      slidesPerView: 3,
      spaceBetween: 16,
      watchOverflow: true,
      lazyPreloadPrevNext: 1,
      loop: false,
      pagination: {
        el: swiperObj.closest('.art-work').querySelector('.swiper-pagination-artworks'),
        clickable: true,
      },
      navigation: {
        nextEl: swiperObj.querySelector('.swiper-button-next'),
        prevEl: swiperObj.querySelector('.swiper-button-prev'),
      },
      breakpoints: {
        320: {
          slidesPerView: 1,
          navigation: {
            enabled: false,
          },
          pagination: {
            enabled: true,
          },
        },
        640: {
          slidesPerView: 2,
          navigation: {
            enabled: false,
          },
          pagination: {
            enabled: true,
          },
        },
        768: {
          slidesPerView: 3,
          navigation: {
            enabled: false,
          },
          pagination: {
            enabled: true,
          },
        },
        1024: {
          slidesPerView: 3,
          navigation: {
            enabled: true,
          },
          pagination: {
            enabled: true,
          },
        },
      },
    });

    if (stateCtx.artworks && stateCtx.artworks.length > 0) {
      setTimeout(() => {
        if (swiperArtworks) {
          swiperArtworks.update();
        }
      }, 100);
    }

    Fancybox.bind("[data-fancybox^='featured-'], [data-fancybox^='gallery-']", {
      hideScrollbar: false,
      wheel: 'slide',
      backdropClick: 'close',
      Hash: false,
      Carousel: {
        Toolbar: {
          display: {
            left: [],
            middle: [],
            right: ['close'],
          },
        },
      },
    });

    const carouselInstances = Array.from(document.querySelectorAll('.f-carousel')).map((el) => {
      return Carousel(el, {
        infinite: true,
      });
    });

    return {
      destroy() {
        swiperArtworks.destroy();
      },
    };
  }

  function getCategories(arr) {
    const idCategories = [...new Set(arr.map((obj) => obj.category.id))];
    // console.log('idCategories', idCategories);
    return idCategories;
  }

  const availableCategories = $derived(getCategories(stateCtx.artworks));

  let isLoaded = $state(false);
</script>

{#if stateCtx.featuredWork.title}
  <div
    transition:fade={{ duration: 500 }}
    class="mb-4 overflow-hidden rounded-3xl transition-all duration-300 card-background backdrop-blur-md py-0 px-4 lg:px-8 opacity-90 hover:opacity-100 lg:hover:shadow-lg lg:hover:shadow-purple-500/20 border-t border-purple-500/30 lg:border-transparent lg:hover:border-purple-500/30"
  >
    <div
      class="p-2 sm:p-4 items-center text-center font-semibold"
      class:opacity-0={!isLoaded}
      class:opacity-100={isLoaded}
      onload={() => (isLoaded = true)}
    >
      {stateCtx.featuredWork.title} ({stateCtx.featuredWork.year})
    </div>

    <div class="h-100 sm:h-170">
      <a href={stateCtx.featuredWork.image} data-fancybox="featured-{stateCtx.featuredWork.id}">
        <img
          src={stateCtx.featuredWork.image}
          alt={stateCtx.featuredWork.title}
          class="w-full h-full object-cover rounded-2xl cursor-pointer"
          class:opacity-0={!isLoaded}
          class:opacity-100={isLoaded}
          onload={() => (isLoaded = true)}
        />
      </a>
    </div>

    <div class="p-2 sm:p-4 items-center text-center text-xs sm:text-base">
      {@html stateCtx.featuredWork.description}
    </div>
  </div>
{/if}

{#if availableCategories.length > 0}
  {#each availableCategories as catId}
    {@const categoryArtworks = stateCtx.artworks.filter((a) => a.category.id === catId)}
    <div class="art-work">
      {#if categoryArtworks.length > 0}
        <button
          onclick={() => routeChoice({ page: stateCtx.pages.category, slug: categoryArtworks[0].category.slug })}
          class="w-full block cursor-pointer py-4 mb-4 bg-linear-to-t from-purple-950/20 to-purple-900/20 text-purple-500 neon-glow-hover rounded-3xl text-xl font-semibold text-center border-t border-purple-500/30"
        >
          {categoryArtworks[0].category.title}
        </button>
      {/if}

      <div class="swiper" use:swiperCreation>
        <div class="swiper-wrapper">
          {#each categoryArtworks as artwork}
            <div class="swiper-slide">
              <div
                class="h-full flex flex-col mb-4 p-4 lg:p-8 rounded-3xl transition-all duration-300 card-background backdrop-blur-md shadow-lg
                lg:hover:shadow-lg lg:hover:shadow-purple-500/20 lg:backdrop-blur-md border-t border-purple-500/30 lg:border-transparent lg:hover:border-purple-500/30"
              >
                <div class="h-80 overflow-hidden rounded-2xl">
                  <a
                    class="relative block w-full h-full overflow-hidden"
                    href={artwork.image}
                    data-fancybox="gallery-{artwork.id}"
                  >
                    <img
                      src={artwork.image}
                      alt={artwork.title}
                      class="w-full h-full object-cover transition-all duration-300 ease-in-out cursor-pointer scale-100 hover:scale-110 opacity-90 hover:opacity-100"
                      loading="lazy"
                    />
                    <div class="swiper-lazy-preloader"></div>
                  </a>
                </div>
              </div>
            </div>
          {/each}

          {#if categoryArtworks.length > 3}
            <div class="swiper-slide">
              <button
                onclick={() => routeChoice({ page: stateCtx.pages.category, slug: categoryArtworks[0].category.slug })}
                class="group cursor-pointer w-full h-full flex flex-col mb-4 p-4 lg:p-8 rounded-3xl transition-all duration-300 card-background backdrop-blur-md shadow-lg
                lg:hover:shadow-lg lg:hover:shadow-purple-500/20 lg:backdrop-blur-md border-t border-purple-500/30 lg:border-transparent lg:hover:border-purple-500/30"
              >
                <div
                  class="h-80 flex items-center justify-center overflow-hidden rounded-2xl border-2 border-dashed border-purple-500 group-hover:border-purple-400 transition-colors"
                >
                  <span
                    class="text-purple-500 group-hover:text-purple-400 font-bold text-xl uppercase tracking-wider transition-all duration-300 ease-in-out"
                  >
                    {stateCtx.translation?.main.view_all}
                  </span>
                </div>
              </button>
            </div>
          {/if}
        </div>
        <div class="swiper-button-prev"></div>
        <div class="swiper-button-next"></div>
      </div>

      <div class="swiper-pagination-artworks"></div>
    </div>
  {/each}
{:else}
  <div
    class="flex w-full items-center justify-center"
    class:opacity-0={!isLoaded}
    class:opacity-100={isLoaded}
    onload={() => (isLoaded = true)}
  >
    <div class="py-4 text-center">{stateCtx.translation?.main.warning}</div>
  </div>
{/if}
