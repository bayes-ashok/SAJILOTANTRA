const dropArea = document.getElementById('dropArea');
    const fileInput = document.getElementById('user_avatar');
    const filePreview = document.getElementById('filePreview');
    let selectedFiles = [];

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
      e.preventDefault();
      e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
      dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
      dropArea.classList.add('dragged-over');
    }

    function unhighlight() {
      dropArea.classList.remove('dragged-over');
    }

    dropArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
      const dt = e.dataTransfer;
      const files = dt.files;

      handleFiles(files);
    }

    dropArea.addEventListener('click', function() {
      fileInput.click();
    });

    fileInput.addEventListener('change', function(e) {
      handleFiles(e.target.files);
    });

    function handleFiles(files) {
      selectedFiles = [...selectedFiles, ...files];

      filePreview.innerHTML = '';

      selectedFiles.forEach(file => {
        if (!file.type.startsWith('image/')) {
          const nonImageFile = document.createElement('p');
          nonImageFile.textContent = file.name;
          filePreview.appendChild(nonImageFile);
        } else {
          const img = document.createElement('img');
          img.classList.add('image-preview');
          img.src = URL.createObjectURL(file);
          img.onload = function() {
            URL.revokeObjectURL(this.src);
          }
          filePreview.appendChild(img);
        }
      });
    }