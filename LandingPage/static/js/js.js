ClassicEditor.create(document.querySelector("#about_project, #blog_content"), {
    toolbar: [
      "heading",
      "|",
      "bold",
      "italic",
      "link",
      "bulletedList",
      "numberedList",
      "blockQuote"
    ],
    heading: {
      options: [
        { model: "paragraph", title: "Paragraph", class: "ck-heading_paragraph" },
        {
          model: "heading1",
          view: "h1",
          title: "Heading 1",
          class: "ck-heading_heading1"
        },
        {
          model: "heading2",
          view: "h2",
          title: "Heading 2",
          class: "ck-heading_heading2"
        }
      ]
    }
  }).catch(error => {
    console.log(error);
});


var typed = new Typed('.element', {
  strings: ["Hello there!", "How can I", "Help you?", "Let me know!"],
  typeSpeed: 100,
  backSpeed: 90,
  showCursor: false,
  loop: true
});


