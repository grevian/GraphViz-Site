
function pollComplete(data, graph_id) {
 console.log(data);
 // If still building, wait 3 seconds then try again
 if (data.building == true) {
   console.log("Still Building, Polling Again");
   var pollPath = '/poll/' + graph_id;
   $.get(pollPath, function(data) { setTimeout(pollComplete(data, graph_id), 3000); }, "json");
 }
 // If completed, Display the imaage
 else if (data.building == false) {
   console.log("Build Complete, Loading Image");
   $('#graph-image').attr('src', '/graph/images/' + graph_id);
   $('#graph-image').show();
 }
 // If Errored, explode.
 else if (data.error != "") {
   console.log("Error Encountered while building image");
   $('#error-container').show();
   $('#error-message').text(data.error);
 }
}

function pollImage(graph_id) {
   $('#graph-image').hide();
   $('#error-container').hide();

   var pollPath = '/poll/' + graph_id;
   $.get(pollPath, function( data ){
     pollComplete(data, graph_id);
   }, "json");
}

