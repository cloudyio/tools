<script lang="ts">
    import Sun from '../components/sun.svelte';

   
</script>

<div class="flex justify-center relative">
    <h1 class="font-semibold text-4xl mt-8 absolute left-1/2 transform -translate-x-1/2">Toolbox</h1>
    
</div>
<div class="flex mt-28 justify-center flex-wrap">
    <div class="card bg-base-100 w-96 shadow-xl mt-5 mr-5">
        <div class="card-body">
          <h2 class="card-title">Youtube Downloader</h2>
          <p>Download a youtube video at any resolution with no ads.</p>
          <div class="card-actions justify-end">
            <button class="btn btn-primary">Download</button>
          </div>
        </div>
      </div>
 
      <div class="card bg-base-100 w-96 shadow-xl mt-5 mr-5">
        <div class="card-body">
          <h2 class="card-title">More comming soon</h2>
          <p>Eventually there will be many other tools to use.</p>
          <div class="card-actions justify-end">
            <button class="btn btn-primary" disabled="disabled">Time travel</button>
          </div>
        </div>
      </div>
</div>