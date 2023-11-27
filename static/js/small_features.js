document.addEventListener('DOMContentLoaded', function () {

    /* copy feature */
    const copyBtn = document.querySelectorAll('.copyBtn');

    copyBtn.forEach(button => {
        button.addEventListener('click', function () {
            const noteContainer = button.closest('.note');
            const text = noteContainer.querySelector(".text");
            const tooltip = button.querySelector(".tooltiptext");

            navigator.clipboard.writeText(text.innerText)
            tooltip.innerHTML = "Copied";

            setTimeout(() => {
                tooltip.innerText = "Copy";
            }, 2000);
        });
    });

    /* copy feature */

    ///////////////////////////////////////////////////////////////////

    /* Edit feature */
    edit_btns = document.querySelectorAll(".edit-btn");

    edit_btns.forEach((button) => {
        button.addEventListener("click", function () {

            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });

            const edit_area = document.querySelector(".edit-note-area");
            const closestNote = this.closest(".note")

            const titleEl = closestNote.querySelector('.title').textContent;
            const contentEl = closestNote.querySelector('.text').textContent;
            const idEl = closestNote.querySelector('.id').value;


            // create a new note
            let note = document.createElement("div")
            note.classList.add("note")

            // create a form
            let form = document.createElement("form");
            form.action = "/update";
            form.method = "post";

            // get the notes id
            let id = document.createElement("input");
            id.name = "id"
            id.type = "hidden";
            id.value = idEl;
            note.appendChild(id);


            // add a time element to the note to keep track of insertion time
            let currentTime = new Date().toLocaleString();

            let time = document.createElement("div");
            time.classList.add("time")
            time.innerHTML = currentTime;
            time.name = "time";
            note.appendChild(time);


            let msg = document.createElement("h3");
            msg.innerHTML = "Edit Note";
            edit_area.appendChild(msg);

            // add an input element for the title
            let title = document.createElement("input");
            title.classList.add("title")
            title.name = "title";
            title.placeholder = "Title";
            title.autocomplete = "off";
            title.autofocus = true;
            title.required = true;
            title.value = titleEl;
            note.appendChild(title)

            // create a textarea for the note
            let textarea = document.createElement("textarea");
            textarea.name = "content";
            textarea.placeholder = "Write a note...";
            textarea.value = contentEl;
            note.appendChild(textarea);

            // create an update button to save the changes
            let button = document.createElement("button");
            button.type = "submit";
            button.classList.add("save");
            button.innerHTML = "Update";
            note.appendChild(button);

            title.addEventListener("input", function () {
                if (title.value.length > 25) {
                    title.style.borderBottom = '1px solid #d65454';
                    button.disabled = true;
                    button.style.opacity = '.5';
                    textarea.innerText = 'Title must be 25 characters or less.'
                    textarea.style.color = '#d65454'
                } else {
                    title.style.borderBottom = '1px solid #dcaf18';
                    button.disabled = false;
                    button.style.opacity = '1';
                    textarea.innerText = '';
                    textarea.style.color = '#fff'
                }
            });


            // create a cancel button to cancel the update
            let cancel_button = document.createElement("button")
            cancel_button.classList.add("cancel-button");
            cancel_button.innerHTML = "Cancel";
            note.appendChild(cancel_button);

            cancel_button.addEventListener("click", function () { 
                edit_area.innerHTML = "";
            });

            // put the note in the form
            form.appendChild(note);

            // open the note for editing
            edit_area.appendChild(form);
        });
    });
    /* Edit feature */
});