const byId = (id) => {
  return document.getElementById(id);
};

const input = byId("image-uploads"),
  preview = byId("preview");
input.addEventListener("change", () => {
  byId("preview").innerHTML = "";

  const files = input.files;
  if (files.length === 0) {
    // No files selected
    const p = document.createElement("p");
    p.textContent = "No files currently selected for upload.";
    preview.appendChild(p);
  } else {
    // Create preview for each file, along with inputs for adjusting filename & metadata
    for (const file of files) {
      const reader = new FileReader();
      reader.addEventListener(
        "load",
        (evt) => {
          createImagePreview(file, evt.target.result);
        },
        false
      );
      reader.readAsDataURL(file);
    }
  }
});

function formatBytes(bytes) {
  // Formats bytes in a more human-readable format
  if (bytes < 1024) {
    return `${bytes} bytes`;
  } else if (bytes < 1048576) {
    return `${(bytes / 1024).toFixed(1)}KB`;
  } else {
    return `${(bytes / 1048576).toFixed(1)}MB`;
  }
}

function createImagePreview(file, dataUrl) {
  const template = document.getElementById("preview-template").cloneNode(true);
  template.classList.remove("hidden");

  // Add image details to template
  template.getElementsByTagName("img").item(0).src = dataUrl;
  template.getElementsByTagName("input").item(0).value = file.name.replace(
    /\.[^/.]+$/,
    ""
  );
  template.getElementsByTagName("figcaption").item(0).textContent = `${
    file.type
  } - ${formatBytes(file.size)}`;

  // Add template to preview div
  preview.append(template);
}

byId("upload-button").addEventListener("click", () => {
  // Generate 7 digits of unit time and a secure random value for filename
  const unixTime = Math.floor(Date.now() / 1000)
    .toString()
    .slice(3);
  const buf = new Uint32Array(1);
  window.crypto.getRandomValues(buf);
  const randomValue = buf[0];
  Array.from(byId("preview").children).forEach((imagePreview, i) => {
    //preview.getElementsByTagName("img").item(0).src;
    const fileName = `${randomValue}_${unixTime}_${i + 1}.jpg`;
    console.log(fileName);
  });
});
