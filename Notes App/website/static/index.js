// take the nodeid that we pass, send a post request to delete-note endpoint
// after getting response from delete-note endpoint => reload the page

function deleteNote(noteId){
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId })      // turns the noteId into a string
    }).then((_res)=>{
        window.location.href = "/";         // redirect to the home page
    });
}
