<script>
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
      hideScrollbar: true,
      wheel: 'slide',
      backdropClick: 'close',
      Hash: false,
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
</script>

<div class="mb-4 overflow-hidden rounded-3xl transition-all duration-300 bg-linear-to-t from-purple-950/20 to-black">
  <div class="p-4 items-center text-center font-semibold">
    {stateCtx.featuredWork.title} ({stateCtx.featuredWork.year})
  </div>

  <div class="h-170">
    <a href={stateCtx.featuredWork.image} data-fancybox="featured-{stateCtx.featuredWork.id}">
      <img
        src={stateCtx.featuredWork.image}
        alt={stateCtx.featuredWork.title}
        class="w-full h-full object-contain cursor-pointer"
      />
    </a>
  </div>

  <div class="p-4 items-center text-center">
    {stateCtx.featuredWork.description}
  </div>
</div>

{#if availableCategories.length > 0}
  {#each availableCategories as catId}
    {@const categoryArtworks = stateCtx.artworks.filter((a) => a.category.id === catId)}
    <div class="art-work">
      {#if categoryArtworks.length > 0}
        <div class="py-4 mb-4 bg-purple-950/20 text-purple-500 rounded-2xl text-xl font-semibold text-center">
          {categoryArtworks[0].category.title}
        </div>
      {/if}

      <div class="swiper" use:swiperCreation>
        <div class="swiper-wrapper">
          {#each categoryArtworks as artwork}
            <div class="swiper-slide">
              <div
                class="h-full flex flex-col mb-4 p-4 lg:p-8 rounded-3xl transition-all duration-300 bg-purple-950/20 shadow-2xl backdrop-blur-md hover:bg-purple-950/20 lg:bg-transparent lg:hover:backdrop-blur-md
                lg:hover:shadow-2xl lg:hover:shadow-purple-600/20"
              >
                <div class="h-80 overflow-hidden rounded-2xl">
                  <a href={artwork.image} data-fancybox="gallery-{artwork.id}">
                    <img
                      src={artwork.image}
                      alt={artwork.title}
                      class="w-full h-full object-cover cursor-pointer scale-100 transition-transform duration-300 ease-in-out hover:rotate-3 hover:scale-110"
                    />
                  </a>
                </div>
              </div>
            </div>
          {/each}

          {#if categoryArtworks.length > 3}
            <div class="swiper-slide">
              <button
                onclick={() => routeChoice({ page: stateCtx.pages.category, slug: categoryArtworks[0].category.slug })}
                class="group w-full h-full cursor-pointer flex flex-col mb-4 p-4 lg:p-8 rounded-3xl transition-all duration-300 bg-purple-950/20 shadow-2xl backdrop-blur-md hover:bg-purple-950/20 lg:bg-transparent lg:hover:backdrop-blur-md
                lg:hover:shadow-2xl lg:hover:shadow-purple-600/20"
              >
                <div
                  class="h-80 flex items-center justify-center overflow-hidden rounded-2xl border-2 border-dashed border-purple-500/40 group-hover:border-purple-500 transition-colors"
                >
                  <span
                    class="text-purple-500 group-hover:text-purple-400 font-bold text-xl uppercase tracking-wider group-hover:rotate-3 transition-transform duration-300 ease-in-out group-hover:scale-110"
                  >
                    View all
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
  No artworks available
{/if}
