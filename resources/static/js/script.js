
function pollComplete(data, graph_id) {
 console.log(data);
 // If Errored, explode.
 if (data.error != "") {
   console.log("Error Encountered while building image");
   $('#graph-image').hide();
   $('#error-container').show();
   $('#error-message').text(data.error);
 }
 // If still building, wait 3 seconds then try again
 else if (data.building == true) {
   console.log("Still Building, Polling Again");
   var pollPath = '/poll/' + graph_id;
   setTimeout(function() { pollImage(graph_id); }, 3000);
 }
 // If completed, Display the imaage
 else if (data.building == false) {
   console.log("Build Complete, Loading Image");
   $('#graph-image').attr('src', '/graph/images/' + graph_id);
 }
}

function pollImage(graph_id) {
   $('#error-container').hide();

   var pollPath = '/poll/' + graph_id;
   $.get(pollPath, function( data ){
     pollComplete(data, graph_id);
   }, "json");
}

