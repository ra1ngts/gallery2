<div class="flex h-screen w-full flex-col items-center justify-center">
  <div class="loader"></div>
</div>

<style>
  .loader {
    margin: auto;
    width: 150px;
    height: 150px;
    border: 2px solid #eae4ea;
    border-bottom: 2px solid #2a2a2a;
    border-radius: 50%;
    animation: loader 2s linear infinite;
  }

  @keyframes loader {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
</style>
