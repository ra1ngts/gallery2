<script>
  import { stateCtx } from '../../store.svelte';

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

    Fancybox.bind("[data-fancybox^='artwork-']", {
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

<div class="h-100 overflow-hidden rounded-2xl">
  <a href={stateCtx.featuredWork.image}>
    <img
      src={stateCtx.featuredWork.image}
      alt={stateCtx.featuredWork.title}
      class="w-full h-full object-cover cursor-pointer scale-100 transition-transform duration-300 ease-in-out hover:rotate-3 hover:scale-110"
    />
  </a>
</div>

{#each availableCategories as catId}
  <div class="pb-4 art-work">
    <div class="swiper" use:swiperCreation>
      <div class="swiper-wrapper">
        {#each stateCtx.artworks.filter((a) => a.category.id === catId) as artwork}
          <div class="swiper-slide pb-4">
            <div
              class="h-full flex flex-col p-4 lg:p-8 rounded-3xl transition-all duration-300 bg-purple-950/40 shadow-2xl backdrop-blur-md hover:bg-purple-950/40 lg:bg-transparent lg:hover:backdrop-blur-md
                lg:hover:shadow-2xl lg:hover:shadow-purple-500/10"
            >
              <div class="h-80 overflow-hidden rounded-2xl">
                <a href={artwork.image} data-fancybox="artwork-{artwork.id}">
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
      </div>
      <div class="swiper-button-prev"></div>
      <div class="swiper-button-next"></div>
    </div>

    <div class="swiper-pagination-artworks"></div>
  </div>
{/each}
