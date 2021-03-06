(function() {
  document.getElementById("id_csv_file").onchange = function(){
    var files = document.getElementById("id_csv_file").files;
    var file = files[0];
    if(!file){
      return alert("No file selected.");
    }
    getSignedRequest(file);
  };
})();
    function getSignedRequest(file){
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/admin/products/product/import-csv/?file_name="+file.name+"&file_type="+file.type);
  xhr.onreadystatechange = function(){
    if(xhr.readyState === 4){
      if(xhr.status === 200){
        var response = JSON.parse(xhr.responseText);
        uploadFile(file, response.data, response.url);
      }
      else{
        alert("Could not get signed URL.");
      }
    }
  };
  xhr.send();
}
function uploadFile(file, s3Data, url){
  var xhr = new XMLHttpRequest();
  xhr.open("POST", s3Data.url);

  xhr.upload.addEventListener('progress', function (e) {
        var fileSize = file.size;

        if (e.loaded <= fileSize) {
            var percent = Math.round(e.loaded / fileSize * 100);
            $('#progress-bar-file').width(percent + '%').html('Uploading...' + percent + '%');
        }

        if(e.loaded === e.total){
            document.getElementById("file-name").value = file.name;
            document.getElementById("submit-button").disabled = false;
            document.getElementById("id_csv_file").value = null;
            $('#progress-bar-file').width(100 + '%').html(100 + '%' + ' Uploaded');
        }
    });

  var postData = new FormData();
  for(key in s3Data.fields){
    postData.append(key, s3Data.fields[key]);
  }
  postData.append('file', file);

  xhr.onreadystatechange = function() {
    if(xhr.readyState === 4){
      if(xhr.status === 200 || xhr.status === 204){
        document.getElementById("id_csv_file").src = url;
      }
      else{
        alert("Could not upload file.");
      }
   }
  };
  xhr.send(postData);
}