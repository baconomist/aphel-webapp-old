if(window.location.href.includes("announcement") && !window.location.href.includes("user")){
    
    div = $("#editor");
    
    announcement_id = 0
    server_bridge.sendToServer("", {"function": "get_new_announcement_id", "data":JSON.parse(getCookie("login"))["email"]}, function(response){
        announcement_id = response["data"];
    });    
    
    init_quill(div, announcement_id);   
}

function init_quill(div, announcement_id){
    
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

        ['clean']                                         // add a remove formatting button
    ];

    var quill = new Quill("#" + div.attr('id'), {
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
            
            html = document.getElementById(div.attr("id")).children[0].innerHTML;

            html = quill.container.firstChild.innerHTML;
            
            server_bridge.sendToServer("/announcement", data={"data":{"login":JSON.parse(getCookie("login")), 
                                      "announcement": {"content_html":html, "id": announcement_id}}}, 
            function(response){
                console.log("Sent announcement to server!");
            });

        }
    });   

}

