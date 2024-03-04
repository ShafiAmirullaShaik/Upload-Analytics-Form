document.addEventListener('DOMContentLoaded', function () {
  // Get references to the select and input elements
  let data_source = document.getElementById('datasource');
  let userDataSource = document.getElementById('userDataSource');

  data_source.addEventListener('change', function () {
      userDataSource.value = data_source.options[data_source.selectedIndex].value.trim();
  });
});

document.getElementById("uploadBtn").addEventListener("click", function () {
    let file_name = document.getElementById("filename").value.trim();
    let extension_select = document.getElementById("extensionSelect");
    let extension_name = extension_select.options[extension_select.selectedIndex].value.trim();
    let Upload_ErrorMsg = document.getElementById("UploadErrorMsg");
    let extension_error = document.getElementById("extensionError");
    let msg = document.getElementById('msg')

    

  
    Upload_ErrorMsg.textContent = "";
    extension_error.textContent = "";
    msg.textContent = ''
  
    if (
      (file_name === "" || file_name == null) &&
      (extension_name === "" || extension_name == null)
    ) {
      Upload_ErrorMsg.textContent = "Please upload the file";
      extension_error.textContent = "Please select extension";
      return;
    }
  
    if (file_name === "" || file_name == null) {
      Upload_ErrorMsg.textContent = "Please upload the file";
      return;
    }
  
    if (extension_name === "" || extension_name == null) {
      extension_error.textContent = "Please select extension";
      return;
    }
  
    if (Upload_ErrorMsg.textContent || extension_error.textContent) {
      return;
    }
    document.getElementById("uploadForm").submit();
  });

let confirmReplaceModal = document.getElementById('confirmReplaceModal')
confirmReplaceModal.style.display = 'block'

let confirmReplaceBtn = document.getElementById('confirmReplaceBtn');

    confirmReplaceBtn.addEventListener('click', function (e) {
      let new_Filename = document.getElementById('newFilename').value.trim();
      let extensionSelect_1 = document.getElementById('extensionSelect1').value.trim();

      fetch(`/replace_filename/?getNewName=${new_Filename}&getExtension=${extensionSelect_1}`)
        .then(response => response.json())
        .then(data => {
          if (data.Bool) {
            document.getElementById('reEntername').innerText = data.reEntername;
          } else {
            let msg = document.getElementById('msg')
            // let link = document.getElementById('link')
            msg.textContent = 'File renamed Successfully and Uploaded to Bucket!'
            // link.textContent = 'Go for analysis'
            document.getElementById('reEntername').innerText = 'File renamed successfully!!';
            setTimeout(() => {
              closeModal();
            }, 2000);
          }
        })
        .catch(error => console.error('Error:', error));
    });

    function closeModal() {
      let confirmReplaceModal = document.getElementById('confirmReplaceModal');
      if (confirmReplaceModal) {
        confirmReplaceModal.style.display = 'none';
      }
    }