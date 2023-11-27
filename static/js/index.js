document.addEventListener('DOMContentLoaded', function () {

    // Drop down menu
    const menuBtn = document.getElementById("menu-button")
    menuBtn.addEventListener("click", function () {
        const menu = document.querySelector(".menu");
        menu.classList.toggle("hidden")
        menu.classList.toggle("visible")
    });

    function newNote() {

        const new_note_area = document.querySelector(".new-note");

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

        // create a form
        let form = document.createElement("form");
        form.action = "/";
        form.method = "post";


        // create a new note
        let note = document.createElement("div");
        note.classList.add("note");

        // add a time element to the note to keep track of insertion time
        let currentTime = new Date().toLocaleString();

        let time = document.createElement("div");
        time.classList.add("time")
        time.innerHTML = currentTime;
        time.name = "time";
        note.appendChild(time);


        let msg = document.createElement("h3")
        msg.innerHTML = "New Note";
        new_note_area.appendChild(msg)

        // add an input element for the title of each note
        let title = document.createElement("input");
        title.classList.add("title")
        title.name = "title";
        title.placeholder = "Title";
        title.autocomplete = "off";
        title.autofocus = true;
        title.required = true;
        note.appendChild(title)

        // create a textarea for the note
        let textarea = document.createElement("textarea");
        textarea.name = "note";
        textarea.placeholder = "Write a note...";
        note.appendChild(textarea);

        // create a save button to save the note to a data base
        let button = document.createElement("button");
        button.type = "submit";
        button.classList.add("save");
        button.innerHTML = "Save";
        button.disabled = true
        button.style.opacity = '.5';
        note.appendChild(button);

        // make sure users gives a title of 25 letters or less
        title.addEventListener("input", function () {
            if (title.value.length > 25 || title.value.length < 1) {
                title.style.borderBottom = '1px solid #d65454';
                button.disabled = true;
                button.style.opacity = '.5';
                textarea.innerText = 'Please ensure that your title is between 1 and 25 characters in length.'
                textarea.style.color = '#d65454'
            } else {
                title.style.borderBottom = '1px solid #dcaf18';
                button.disabled = false;
                button.style.opacity = '1';
                textarea.innerText = '';
                textarea.style.color = '#fff'
            }
        });

        // create a cancel button to cancel new note creations
        let cancel_button = document.createElement("button")
        // cancel_button.href = "/";
        cancel_button.id = "cancelBtn"
        cancel_button.classList.add("cancel-button");
        cancel_button.innerHTML = "Cancel";
        note.appendChild(cancel_button);

        cancel_button.addEventListener("click", function () {
            new_note_area.innerHTML = "";
        });

        // put the note in the form
        form.appendChild(note);

        // add the new note to mian
        new_note_area.appendChild(form);
    }

    let no_notesEl = document.querySelector(".no-notes");
    let add_button = document.querySelector(".add-button");

    add_button.addEventListener("click", function () {
        no_notesEl.style.display = "none";
    });
    add_button.addEventListener("click", newNote);

});