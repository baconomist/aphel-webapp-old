if(window.location.href.includes("announcement")){
    div = $("#editor");

    // Clear editor html
    div.html("");

    var toolbarOptions = [
        ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
        ['blockquote', 'code-block'],

        [{ 'header': 1 }, { 'header': 2 }],               // custom button values
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
        [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
        [{ 'direction': 'rtl' }],                         // text direction

        [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],

        [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
        [{ 'font': [] }],
        [{ 'align': [] }],

        ['clean']                                         // remove formatting button
    ];

    var quill = new Quill('#editor', {
            theme: 'snow',
            modules: {
            toolbar: toolbarOptions
        }
    });

    quill.on('text-change', function(delta, oldDelta, source) {
        if (source == 'api') {
            console.log("An API call triggered this change.");
        } else if (source == 'user') {
            console.log("A user action triggered this change.");
            console.log(document.getElementById("editor").children[0].innerHTML)
            html = document.getElementById("editor").children[0].innerHTML;

            server_bridge.sendToServer("/announcement", data={"data":{"login":JSON.parse(getCookie("login")), "announcement": html}}, function(response){
                console.log("Sent announcement to server!");
            });

        }
    });   

}


