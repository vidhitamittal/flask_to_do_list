**Summary**  
This is a simple Flask application that allows users to create a to-do list with text-based tasks. The application has been extended to allow users to upload multiple images for each task. The images are stored in a separate database table linked to each task.

**Features**
- User authentication: Register, login, and logout.
- Add tasks with text and multiple images.
- View, update, and delete tasks.
- View images associated with each task.
- Delete images from tasks.

**Prerequisites**
- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Pillow (PIL)
- werkzeug

**Installation Guide**  
Step-by-step instructions for setting up the application:  
- Download the project code.  
- Install required dependencies using the provided `requirements.txt` file (pip install -r requirements.txt)
- If using a cloud-based IDE or a codespace, forward the port to localhost (default: `127.0.0.1:5000`) or the desired port.  
- Run the application by executing the main Python file (python app.py)

**Usage Instructions**  
- Start the application by running the Python file.  
- Access the app by navigating to the configured port in a web browser.  
- Create an account, log in, and start managing your tasks!  

**Database Setup**
- The app uses SQLite for database management. On the first run, the database will be created automatically. You can find the database file (`test.db`) in the same directory as the `app.py` file.

**Technologies Used**  
- **Frameworks/Libraries:** Flask, SQLAlchemy, Flask-LoginManager, Pillow (PIL).  
- **Database:** SQLite (`test.db` with three tables for tasks, users, and images).  
- **Other:** Base64 encoding for image storage.  

**Application Structure**
- `app.py`: The main Flask application file that handles routing, user authentication, and database operations.
- `templates/`: Contains the HTML templates for rendering the pages.
  - `home.html`: The home page.
  - `index.html`: The page displaying the to-do list.
  - `signup.html`: User registration page.
  - `login.html`: User login page.
  - `update.html`: Task update page.
  - `wrongPassword.html`: Error page when the password is incorrect.
  - `unregistered.html`: Error page for unregistered users.
  - `alreadyRegistered.html`: Error page when a user tries to register with an existing username.

**Key Routes**

**`/` - Home Page**
Displays the welcome page of the application.

**`/index` - To-Do List**
Displays a list of tasks for the currently logged-in user. Allows adding new tasks with images, deleting tasks, and updating task content or images.

**`/register` - User Registration**
Allows new users to register by providing a username and password.

**`/login` - User Login**
Allows registered users to log in with their username and password.

**`/logout` - User Logout**
Logs the current user out and redirects to the home page.

**`/update/<int:id>` - Update Task**
Allows users to update the content and images of an existing task.

**`/delete/<int:id>` - Delete Task**
Deletes a task and any associated images.

**`/deleteimage/<int:id>` - Delete Image**
Deletes an image associated with a task.


How It Works:
1. **Task Creation**: 
   - Users can create tasks by entering text and uploading images.
   - The images are saved in the database as base64-encoded strings, linked to the task using a foreign key.
2. **Task Update**: 
   - Users can update the task content and upload new images.
3. **Task Deletion**:
   - Users can delete tasks and associated images.
4. **Image Handling**:
   - Uploaded images are saved and encoded in base64 format before being stored in the database.

**Screenshots**

Welcome page:
![https://private-user-images.githubusercontent.com/122602734/402298131-52f57ed2-cb49-4478-b700-220477e7869e.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzY2NDA5NTAsIm5iZiI6MTczNjY0MDY1MCwicGF0aCI6Ii8xMjI2MDI3MzQvNDAyMjk4MTMxLTUyZjU3ZWQyLWNiNDktNDQ3OC1iNzAwLTIyMDQ3N2U3ODY5ZS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwMTEyJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDExMlQwMDEwNTBaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0yY2IzN2YxMzZiNDBjOGZiMTdmMGYzYjY3YzBmYWRjMGE5ZGQ2MjkxZTg0NDcyODQyOTk2MDUxMDFkYzBjYWVkJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.XLG28cGvQQquIBUwTKxDw6cO9T5J2z1PPqMY9964TU4](https://private-user-images.githubusercontent.com/122602734/402298131-52f57ed2-cb49-4478-b700-220477e7869e.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzY2NDEzMzAsIm5iZiI6MTczNjY0MTAzMCwicGF0aCI6Ii8xMjI2MDI3MzQvNDAyMjk4MTMxLTUyZjU3ZWQyLWNiNDktNDQ3OC1iNzAwLTIyMDQ3N2U3ODY5ZS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwMTEyJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDExMlQwMDE3MTBaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1iYjJiNjJjNzc3YmVkMjljZmFjMTVkNDUxZmMwMTViNDUxNTRmNmJiNTIyYTgyODM0ZmVjYjc5OWMzNWE1OTIxJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.8p-RhMWGBBxOEjGCAvtaL0bvKzOfkk0DCjOoTQV5XY8)

Home Page:
<img width="1440" alt="Screenshot 2025-01-13 at 8 37 03 PM" src="https://github.com/user-attachments/assets/53291d9b-1f5a-4d1f-8073-25d8d75ceb84" />


Update Task:
<img width="1440" alt="Screenshot 2025-01-13 at 8 37 22 PM" src="https://github.com/user-attachments/assets/537b5a60-e3f8-4a6e-a42d-04075d4b4c05" />


**Contact Information**

For inquiries, support, or to report bugs and request new features, please feel free to reach out:  

**Developer:** Vidhita Mittal

**Email:** vidhitamittal@gmail.com  

Feel free to reach out with any feedback and suggestions to improve the application.
