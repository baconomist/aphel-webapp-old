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

    enable()
    {
        this.quill.enable(true);
    }

    disable()
    {
        this.quill.enable(false);
    }

    destroy()
    {
        // Need to destroy quill on use because after saving, it doesn't edit anymore
        // Toolbar is the only thing that needs to be destroyed
        // TODO: Find a better fix for this
        this.editor_div.parent().find(".ql-toolbar").remove();
    }


    init_quill(editor_div, announcement_id){

        let toolbarOptions = [

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

        let quill = new Quill("#" + editor_div.attr('id'), {
                theme: 'snow',
                modules: {
                toolbar: toolbarOptions
            }
        });

        return quill;

    }

}
