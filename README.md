# MyNotes

#### Video Demo: <https://youtu.be/X-6PPe6HsBw>

#### Description:
My project is a Notes Flask application with user authentication. the app has a dark theme palette, which is made up of these colours:
{
"background-colour": "`#2525252`",
"note-background": "`#4e4d4d93`",
"note-foreground": "`#fff`",
"note-details": [
"`#e0b21b`",
"`#e15f2"`,
"`#37e2e2`"
]
}

Upon running the app the login page will be opened as the default pop-up page forcing the user to be logged in to access the application. if the user does not have an account they can register for an account by clicking on the "don't have an account? register here" option below the log-in form. To register for an account you are asked for three main things

- A unique username.
- A strong password which is enforced by both the front end and the back end.
- A confirmation for that password.

Upon signing up for an account you will be redirected to the login page with a flashing message from the Python Flask library that will inform you that your account has been created. There you can log in using your new credentials. upon logging in and opening the app for the first time you will see a message in the middle of the page telling you that you do not have any notes yet. to create a note you can click on the add button at the bottom right of the page. the new note opens up in the new notes area of the page below the search bar. To create a note you are required to provide two main things:

- A unique title that is less than 25 characters and more than one in length which enables the search by title feature.
- Content for your note.

At the bottom of the new note, you have two options:

- A cancel button to cancel the creation of the new note.
- A save button to save the note to the database and show the note in the saved notes area.

You can also see a search bar at the top of the page along with a hamburger menu that includes four options:

- **Profile:** This option will open the profile page where you can update or delete your account. Both options will require you to provide your current password.
- **Archives:** This option will open the archives page where you can view all of your archived notes.
- **Clear Notes:** This option will delete all of your notes from the database.
- **Logout:** This option will log you out of your account and clear all of your session data.

The saved notes consist of two primary parts and two secondaries. the primary parts are:

- **A Title:** The note's title enables the search by title feature at the top of the home page.
- **Content:** the actual note.

The secondary parts are:

- **Time stamp:** which stamps the time of the note's creation.
- **The bottom function bar:** which consists of features like:

  - **Delete:** The delete button below each note can be used to delete a specific note by choice.

  - **Pin:** The pin icon will pin the note to the top of your page, and it features a dark orangish colour, specifically #e15f28 to tell it apart from the other notes. Note that you can pin more than one note!

  - **Edit:** The edit icon will open the selected note for editing in the edit notes area with two options one being update to save the changes and the other being cancel to discard the changes.

  - **Copy:** The copy icon can be used to quickly copy the note content to your clipboard.

  - **Archive:** The archive icon can be used to hide the note from prying eyes. You can access the archived notes by clicking on the drop-down menu button at the top right of the page by selecting the Archives option.

- ### File Structure:

  - **static :**

    - **css :**
      - bolierPlate.css: contains all the basic and global styling of the page.
      - style.css: contains note styling that is extended by every other file.
      - login-register: contains styling for the login and register forms.
      - profile.css: contains styling for the profile page.
      - saved.notes.css: contains styling for the saved notes.
      - search.css: contains styling for the search page.
    - **images :**
      - Contains all the images used throughout the app.
    - **js :**
      - index.js: contains most of the basic functionality used by the index(home) page like the new note button and the hamburger menu button.
      - login-register.js: contains all of the functionality used by the login/register page that forces the user to have all forms filled out and have a strong password before proceeding.
      - profile.js: contains most of the basic functionality used by the profile page.
      - small-features.js: contains all of the functionality used throughout the page that enables the edit and the copy features.

  - **templates:** contains all the html files. of which are 7 files.

  - **app.py:** contains all the routes used by the app which are:

    - "/": opens the home page if you are logged in it will redirect you to the login page.
    - "/login": checks if your username and password are valid if so it will redirect you to the "/" route.
    - "/register": Create your new account if you don't already have an account.
    - "/logout": logs you out and clears all session data.
    - /profile": opens the profile page and handles password and account deletion requests.
    - "/delete": deletes a targeted note.
    - "/clear-notes": delete all notes of the current user.
    - "/search": searches the user's notes for a targeted note.
    - "/update": updates a pre-existing note.
    - "/archive": archives and unarchives a note based on its current state.
    - "/archives": opens the archives page and shows all the archived notes if any.
    - "/pin": pins and unpins a note based on its current status

  - **notes.db:** is the database used by the app and contains the used tables which are:
    - ```
      CREATE TABLE users (
      id INTEGER,
      username TEXT UNIQUE CHECK (LENGTH(username) <= 25),
      password TEXT,
      PRIMARY KEY(id)
      );
      ```
    - ```
      CREATE TABLE notes (
      id INTEGER,
      title NOT NULL CHECK(LENGTH(title) <= 25),
      content TEXT NOT NULL,
      date_time DATETIME,
      pin_status INTEGER DEFAULT 0,
      archive_status DEFAULT 0,
      user_id INTEGER NOT NULL,
      FOREIGN KEY(user_id) REFERENCES users(id),
      PRIMARY KEY(id)
      );
      ```
