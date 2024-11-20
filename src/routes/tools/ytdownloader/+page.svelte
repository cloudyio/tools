<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    let videoLink = '';
    let lastProcessedUrl = '';
    let videoData: { 
        title: string, 
        thumbnail_url: string,
        length: number,
        available_resolutions: string[],
        stream_details: {
            resolution: string,
            fps: number,
            is_progressive: boolean,
            filesize: number
        }[]
    } | null = null;
    let selectedResolution: string | null = null;
    let loading = false;
    let loadingInfo = false;
    let checkInterval: number;

    onMount(() => {
        checkInterval = setInterval(checkVideoUrl, 1000);
    });

    onDestroy(() => {
        clearInterval(checkInterval);
    });

    function checkVideoUrl() {
        if (isValidYouTubeUrl(videoLink) && videoLink !== lastProcessedUrl) {
            lastProcessedUrl = videoLink;
            fetchVideoInfo(videoLink);
        }
    }

    function isValidYouTubeUrl(url: string) {
        const pattern = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+/;
        return pattern.test(url);
    }

    async function fetchVideoInfo(url: string) {
        if (!isValidYouTubeUrl(url)) return;
        
        try {
            loadingInfo = true;
            const res = await fetch("http://127.0.0.1:5000/info", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url })
            });
            const data = await res.json();
            if (res.ok) {
                videoData = data;
                selectedResolution = data.available_resolutions[0];
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            console.error("Failed to fetch video data:", error);
            videoData = null;
            lastProcessedUrl = ''; // Reset on error to allow retrying
        } finally {
            loadingInfo = false;
        }
    }

    async function downloadVideo() {
        try {
            loading = true;
            const res = await fetch('http://127.0.0.1:5000/download', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    url: videoLink,
                    resolution: selectedResolution
                })
            });

            if (!res.ok) {
                const errorData = await res.json();
                throw new Error(errorData.error || 'Download failed');
            }

            const data = await res.json();
            const a = document.createElement('a');
            a.href = data.url;
            a.download = `${data.title}.mp4`;
            document.body.appendChild(a);
            a.click();
            a.remove();

        } catch (error: any) {
            console.error('Download failed:', error);
            alert(error.message || 'Download failed. Please try again.');
        } finally {
            loading = false;
        }
    }

    function formatFileSize(bytes: number): string {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
        return (bytes / (1024 * 1024 * 1024)).toFixed(1) + ' GB';
    }

    $: if (!videoLink) {
        videoData = null;
        lastProcessedUrl = '';
    }
</script>

<div class="flex justify-center items-center min-h-screen">
    <div class="card bg-primary text-primary-content w-[48rem] h-96">
        <div class="card-body flex flex-col justify-between">
            <div>
                <h2 class="card-title">YouTube Video Downloader</h2>

                <h3 class="text-md pt-6 font-semibold">Video link</h3>
                <input
                    type="text"
                    placeholder="https://youtube.com/watch?v=..."
                    class="input input-bordered w-full max-w-xs"
                    bind:value={videoLink}
                    id="videoLink"
                />
            </div>

            {#if loadingInfo}
                <div class="mt-4">
                    <span class="loading loading-spinner loading-md"></span>
                </div>
            {:else if videoData}
                <div class="mt-4">
                    <h3 class="text-lg font-semibold">Video Title: {videoData.title}</h3>
                    {#if videoData.stream_details?.length > 0}
                        <label for="resolution" class="block text-md font-semibold mt-2">Select Resolution:</label>
                        <select id="resolution" 
                                bind:value={selectedResolution} 
                                class="select select-bordered w-full max-w-xs">
                            {#each videoData.stream_details as stream}
                                <option value={stream.resolution}>
                                    {stream.resolution} ({stream.fps}fps) - {formatFileSize(stream.filesize)}
                                    {stream.is_progressive ? '(Progressive)' : ''}
                                </option>
                            {/each}
                        </select>
                    {/if}
                </div>
            {/if}
            <div class="card-actions justify-end">
                <button class="btn" disabled={!videoData} on:click={downloadVideo}>Download</button>
            </div>
        </div>
    </div>
</div>