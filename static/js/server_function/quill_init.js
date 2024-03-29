if(window.location.href.includes("announcement") && !window.location.href.includes("edit")){
    
    div = $("#editor");
    
    announcement_id = 0
    server_bridge.sendToServer("", {"function": "get_new_announcement_id", "data": { "email": JSON.parse(getCookie("login"))["email"]} }, function(response){
        announcement_id = response["data"];
        
        console.log(announcement_id)
        //var announcement_editor = new AnnouncementEditor(div, announcement_id);
        init_quill(div, announcement_id);
    });     
}

class AnnouncementEditor
{
    constructor(editor_div, announcement_id)
    {
        this.editor_div = editor_div;
        this.announcement_id = announcement_id;
        
        this.quill = this.init_quill(editor_div, announcement_id);
    }  
    
    save()
    {
        var html = this.quill.container.firstChild.innerHTML;
            
        server_bridge.sendToServer("/", {"function": "save_announcement", "data":{"login":JSON.parse(getCookie("login")), 
                                  "announcement": {"content_html":html, "id": this.announcement_id}}}, 
        function(response){
            console.log("Sent announcement to server!");
        });   
    }
    
    get_content()
    {
        return this.quill.container.firstChild.innerHTML;
    }
    
    
    
    init_quill(div, announcement_id){
    
        var toolbarOptions = [
            ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
            //['blockquote', 'code-block'],

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

        return quill;

    }

}

function init_quill(div, announcement_id){
    
    var toolbarOptions = [
        ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
        //['blockquote', 'code-block'],

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
            
            server_bridge.sendToServer("/", {"function": "save_announcement", "data":{"login":JSON.parse(getCookie("login")), 
                                      "announcement": {"content_html":html, "id": announcement_id}}}, 
            function(response){
                console.log("Sent announcement to server!");
            });

        }
    });   

}

