# Habit Tracker
#### Video Demo: https://www.youtube.com/watch?v=swFMMqwLMA8

#### Description:
Habit Tracker is a web application that helps users track their habits on a weekly basis.  
Users can create an account, log in securely, and add habits they want to complete during the week.  
Each habit has a weekly goal representing how many days the user wants to complete that habit.  

The application keeps track of completed habits and visually displays progress toward weekly goals.  
It supports multiple users, meaning each user's habits and progress are stored separately.

This project was built using **Flask**, **SQLite**, **HTML**, **CSS**, and **JavaScript**.

---

### logo.png
This is the logo of the web application. It is used as the favicon that appears on the browser tab beside the website name.

---

### styles.css
This file contains all the CSS styling used in the project.  
It defines the layout of the page, button styling, habit cards, progress bars, and includes visual effects such as prompt fade-in animations.

---

### templates
This folder contains all the HTML templates used in the application.

#### add.html
This page is displayed when the user clicks the **Add Habit** button.  
It contains a form that allows the user to enter the name of a habit and specify the number of days per week they want to complete it.

#### apology.html
This template is used to display error messages when invalid input is provided.  
For example, it appears if a username already exists, if passwords do not match, or if required form fields are missing.

#### edit.html
This page allows users to modify an existing habit.  
Users can change the habit name and update the weekly goal for that habit.

#### index.html
This is the homepage of the application.  
It displays all habits created by the user along with their weekly progress.  
From this page, users can mark habits as completed for the current day.

#### layout.html
This file acts as the base template for all other HTML pages in the application.  
It contains the main structure of the website including the navigation bar, page layout, and links to the CSS styling.

All other HTML templates extend this file using Jinja template inheritance. This allows common elements such as the navigation bar and page styling to remain consistent across the entire website without repeating the same code in every HTML file.

The navigation bar also changes depending on whether the user is logged in. Logged-in users can access pages such as **Add Habit**, while logged-out users can only see options like **Login** and **Register**.

#### login.html
It contains the login page of the application. This page allows the user to use their username and password to login to their account and see their progress. This page also allows the user to go to the register page to register for a new account if they don't already have an account.

#### progress.html
This page allows users to view their progress for each of their planned habits.  
It provides a clearer overview of their activity by displaying a progress bar, the number of days remaining in the week, and the percentage of the goal that has been completed.  
This helps users easily track how close they are to achieving their weekly habit target

#### register.html
This page contains the registration form that allows new users to create an account.  
Users are required to provide a username, password, and password confirmation.

The application validates the input by checking whether the chosen username already exists in the database.  
It also verifies that the password and confirmation password match before allowing the user to register successfully.

---

#### app.py
This is the main backend file of the project and contains the core application logic.  
It uses Flask to define the routes of the web application and handles communication between the user interface and the database.

The file includes routes for registering and logging in users, logging them out, adding new habits, editing existing habits, marking habits as completed, and viewing weekly progress.  
It also contains validation checks to ensure that inputs are correct and that users can only access their own data.

`app.py` also performs SQL queries to store and retrieve information from the SQLite database, including user account details, habit information, and daily completion logs.  
Because it controls routing, validation, and database interaction, this file is the central part of the entire Habit Tracker application.

---

#### helpers.py
This file contains helper functions that simplify and support the main logic of the application.

One of the key functions in this file is `login_required`, which is a decorator used to protect certain routes.  
It ensures that only logged-in users can access specific pages of the application. If a user tries to access a protected route without being logged in, they are automatically redirected to the login page.

Another function in this file is `apology`, which is used to display error messages to the user.  
It renders the `apology.html` template and passes an error message along with an HTTP status code. This function helps maintain consistent error handling throughout the application whenever invalid input or unexpected situations occur.

---

### Database Design

The application uses an SQLite database to store user information, habits, and habit completion records.  
The database consists of three tables: `users`, `habits`, and `habit_logs`.

#### users
The `users` table stores account information for each registered user.

Columns:
- `id` – Primary key that uniquely identifies each user. It is automatically incremented.
- `username` – The unique username chosen by the user during registration.
- `hash` – A hashed version of the user's password stored for security purposes.

This table ensures that each user has a unique account and allows the system to authenticate users during login.

#### habits
The `habits` table stores the habits created by users.

Columns:
- `id` – Primary key that uniquely identifies each habit.
- `user_id` – References the `id` of the user who created the habit.
- `name` – The name of the habit the user wants to track.
- `target_days` – The number of days per week the user aims to complete the habit.
- `created_at` – The date the habit was created. It defaults to the current date.

This table allows each user to create multiple habits while ensuring that each habit is associated with the correct user.

#### habit_logs
The `habit_logs` table stores records of when habits are completed.

Columns:
- `id` – Primary key that uniquely identifies each log entry.
- `habit_id` – References the `id` of the habit being completed.
- `completed_date` – The date on which the habit was completed.

Each time a user marks a habit as completed, a new entry is added to this table. This allows the application to calculate weekly progress and track habit completion over time.

### Design Decisions

### Design Decisions

Several design decisions were made while building this project in order to keep the application simple, scalable, and easy to maintain.

One of the major decisions was separating habit information and habit completion records into two different tables: `habits` and `habit_logs`. Instead of storing completion status directly inside the habits table, a separate `habit_logs` table was created to record each time a habit is completed. This design allows the application to track habits over time and makes it easier to calculate statistics such as weekly progress.

Another important design choice was linking habits to users using a `user_id` foreign key. This ensures that each habit belongs to a specific user and prevents users from accessing or modifying habits that do not belong to them. This structure also allows the application to support multiple users with independent habit lists.

Passwords are not stored directly in the database. Instead, they are hashed before being saved. This improves security by ensuring that even if the database were exposed, the actual passwords would not be visible.

The `login_required` decorator was implemented in `helpers.py` to restrict access to certain routes. This prevents unauthorized users from accessing pages that should only be available after logging in.

Flask was chosen as the framework because it provides a lightweight and flexible way to build web applications in Python. SQLite was selected as the database because it is simple to set up, does not require a separate server, and works well for small to medium sized applications like this project.

Finally, Jinja template inheritance was used with `layout.html` so that common elements such as the navigation bar and page styling do not need to be repeated in every HTML file. This makes the code easier to maintain and keeps the project structure clean.

---

Academic Honesty Disclosure: In accordance with the CS50 2026 policy regarding the Final Project, AI was used to assist with the structural organization, grammatical polishing, and Markdown formatting of this documentation based on the author's original project details and technical logic. The design, implementation, and core content remain the original work of the author.