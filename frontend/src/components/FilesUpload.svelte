<script>
  let files = [];
  let loading = false;

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
      const chunks = [];
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        chunks.push(value);
      }

      // Combine all chunks into a single Blob
      const blob = new Blob(chunks, { type: "image/png" });
      const url = URL.createObjectURL(blob);

      // Store the image URL in an array
      files = [...files, url];

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
