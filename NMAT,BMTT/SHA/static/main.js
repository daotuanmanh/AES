document.addEventListener("DOMContentLoaded", () => {
  // Dark mode toggle
  const toggle = document.getElementById("toggle-darkmode");
  toggle.addEventListener("change", () => {
    document.body.classList.toggle("dark-mode", toggle.checked);
  });

  // Toast notification
  const toast = document.getElementById("toast");
  function showToast(msg, duration = 3000) {
    toast.textContent = msg;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), duration);
  }

  // Upload form with progress
  const form = document.getElementById("upload-form");
  const progressWrapper = document.getElementById("progress-wrapper");
  const progressBar = document.getElementById("upload-progress");
  const progressText = document.getElementById("progress-text");

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const fileInput = document.getElementById("file-input");
    if (!fileInput.files.length) {
      showToast("Vui lòng chọn file trước khi gửi.");
      return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    progressWrapper.hidden = false;
    progressBar.value = 0;
    progressText.textContent = "0%";

    fetch("/", {
      method: "POST",
      body: formData,
    }).then((response) => {
      if (!response.ok) {
        showToast("Lỗi khi gửi file!");
        progressWrapper.hidden = true;
        return;
      }
      return response.text();
    }).then((text) => {
      showToast("Gửi file thành công!");
      progressWrapper.hidden = true;
      progressBar.value = 0;
      progressText.textContent = "0%";
      fileInput.value = "";
      // Reload lại trang để cập nhật danh sách file nhận
      setTimeout(() => location.reload(), 1000);
    }).catch(() => {
      showToast("Lỗi mạng hoặc server!");
      progressWrapper.hidden = true;
    });
  });
});
