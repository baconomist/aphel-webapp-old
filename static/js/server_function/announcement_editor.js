class AnnouncementEditor
{
    constructor(editor_div, announcement_id)
    {
        this.editor_div = editor_div;
        this.announcement_id = announcement_id;
        
        this.quill = this.init_quill(editor_div, announcement_id);
    }  
    
    get_content()
    {
        return this.quill.root.innerHTML;
    }
    
    
    
    init_quill(editor_div, toolbar_div, announcement_id){       
        
        var toolbarOptions = [
            
            ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
            //['blockquote', 'code-block'],

            [{ 'header': 1 }, { 'header': 2 }],               // custom button values
            [{ 'list': 'ordered'}, { 'list': 'bullet' }],
            [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
            [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
            [{ 'direction': 'rtl' }],                         // text direction

            [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
            //[{ 'header': [1, 2, 3, 4, 5, 6, false] }], //disable header sizes cus those break the displaying announcements

            [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
            [{ 'font': [] }],
            [{ 'align': [] }],

            ['clean']                                        // add a remove formatting button,
            
            
        ];

        var quill = new Quill("#" + editor_div.attr('id'), {
                theme: 'snow',
                modules: {
                toolbar: toolbarOptions
            }
        });

        return quill;

    }

}