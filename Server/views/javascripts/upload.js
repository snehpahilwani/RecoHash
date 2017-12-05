$('.upload-btn').on('click', function (){
    $('#upload-input').click();
    $('.progress-bar').text('0%');
    $('.progress-bar').width('0%');
});

$('#upload-input').on('change', function(){
    var files = $(this).get(0).files;
    console.log(files)
    var formData = new FormData();
    // Loop through each of the selected files.
    for (var i = 0; i < files.length; i++) {
      var file = files[i];
      // Add the file to the request.
      formData.append('uploads[]', file, file.name);
    }
    for (var pair of formData.entries()) {
    console.log('key: '+pair[0]+ ' ,  val: '+ pair[1]); 
    }
    $.ajax({
      url: 'http://localhost:5000/upload',
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      cache: false,
      success: function(data){
          console.log('upload successful!\n' + data);
          if (typeof data.redirect == 'string'){
                    window.location = data.redirect;
                }
      },
      xhr: function() {
        // create an XMLHttpRequest
        var xhr = new XMLHttpRequest();

        // listen to the 'progress' event
        xhr.upload.addEventListener('progress', function(evt) {

          if (evt.lengthComputable) {
            // calculate the percentage of upload completed
            var percentComplete = evt.loaded / evt.total;
            percentComplete = parseInt(percentComplete * 100);

            // update the Bootstrap progress bar with the new percentage
            $('.progress-bar').text(percentComplete + '%');
            $('.progress-bar').width(percentComplete + '%');

            // once the upload reaches 100%, set the progress bar text to done
            if (percentComplete === 100) {
              $('.progress-bar').html('Done');
            }

          }

        }, false);

        return xhr;
      }
    });

  
});
