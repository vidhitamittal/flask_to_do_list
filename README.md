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
<img width="1440" alt="Screenshot 2025-01-30 at 12 50 49 PM" src="https://github.com/user-attachments/assets/03fcf0e9-d80c-43cf-8cd4-3c61235b038f" />

Login Page:
<img width="1440" alt="Screenshot 2025-01-30 at 12 51 07 PM" src="https://github.com/user-attachments/assets/b1c55c34-26a2-4958-a9cf-f10e12ff8994" />

Register Page:
<img width="1440" alt="Screenshot 2025-01-30 at 12 50 59 PM" src="https://github.com/user-attachments/assets/06ad9939-46c7-4195-88ef-71bd270f729b" />

Update Task:
<img width="1440" alt="Screenshot 2025-01-30 at 12 51 37 PM" src="https://github.com/user-attachments/assets/66d5845b-36fe-4ac0-84ff-10a798c3ea6e" />

**Contact Information**

For inquiries, support, or to report bugs and request new features, please feel free to reach out:  

**Developer:** Vidhita Mittal

**Email:** vidhitamittal@gmail.com  

Feel free to reach out with any feedback and suggestions to improve the application.
