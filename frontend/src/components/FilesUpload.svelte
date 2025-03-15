<script>
  const PNG_START = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
  const PNG_END = [0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82];

  let files = [];
  let loading = false;

  function onImageReceived(chunks) {
      const blob = new Blob(chunks, { type: "image/png" });
      const url = URL.createObjectURL(blob);

      files = [...files, url];
  }

  async function uploadImages(event) {
    const images = event.target.files;
    if (images.length === 0) return;

    loading = true;

    const formData = new FormData();
    for (let image of images) {
      formData.append("images", image);
    }

    try {
      const response = await fetch("http://localhost:8080/generate-saliency/", {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        throw new Error("Failed to process images");
      }

      // Stream processing
      const reader = response.body.getReader();
      let chunks = [];
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        if (value) {
          chunks.push(value);
          const firstBytes = [...value.slice(0, 8)];
          const lastBytes = [...value.slice(-8)];

          if (JSON.stringify(lastBytes) === JSON.stringify(PNG_END)) {
              onImageReceived(chunks);
              chunks = [];
          }
        }
      }

    } catch (error) {
      console.error("Error fetching stream:", error);
    } finally {
      loading = false;
    }
  }

  function downloadImage(url) {
    const a = document.createElement("a");
    a.href = url;
    a.download = "saliency_map.png";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }
</script>

<input type="file" multiple accept="image/*" on:change={uploadImages} />
{#if loading}
  <p>Processing images...</p>
{/if}

{#each files as file}
  <div>
    <img src={file} alt="Saliency Map" />
    <button on:click={() => downloadImage(file)}>Download</button>
  </div>
{/each}
