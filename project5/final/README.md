## HarvardX CS50W: Web Programming with Python and JavaScript

### Course's link
See [here](https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript).

### Requirements
The final project is your opportunity to design and implement a dynamic website of your own. So long as your final project draws upon this course’s lessons, the nature of your website will be entirely up to you, albeit subject to the staff’s approval.

In this project, you are asked to build a web application of your own. The nature of the application is up to you, subject to a few requirements:

  - Your web application must utilize at least two of Python, JavaScript, and SQL.
  - Your web application must be mobile-responsive.
  - In README.md, include a short writeup describing your project, what’s contained in each file you created or modified, and (optionally) any other additional information the staff should know about your project.
  - If you’ve added any Python packages that need to be installed in order to run your web application, be sure to add them to requirements.txt!

Beyond these requirements, the design, look, and feel of the website are up to you!

### Final project

My final project is Instagram clone. Users are able to register, post photos with descriptions, "like" other users' photos, write comments. They can also search through photos and users (search is case insensitive) and apply various filters when uploading photos.

The project was built using Django as a backend framework and JavaScript as a frontend programming language. All generated information are saved in database (SQLite by default).

All webpages of the project are mobile-responsive.

#### Installation
  - Install project dependencies by running `pip install -r requirements.txt`. Dependencies include Django and Pillow module that allows Django to work with images.
  - Make and apply migrations by running `python manage.py makemigrations` and `python manage.py migrate`.
  - Create superuser with `python manage.py createsuperuser`. This step is optional.
  - Go to website address and register an account.

#### Files and directories
  - `djangoapp` - main application directory.
    - `static/djangoapp` contains all static content.
        - `css` contains compiled CSS file and its map.
        - `js` - all JavaScript files used in project.
            - `post.js` - script that run in `post.html` template.
            - `search.js` - this script run in every template because it is included in base template. It validates the search field.
            - `upload.js` - script that run in `upload.html` template.
            - `user.js` - script that run in `user.html` template.
            - `welcome.js` - script that run in `welcome.html` template.
        - `scss` - source SCSS files.
    - `templates/djangoapp` contains all application templates.
        - `_base.html` - base templates. All other tempalates extend it.
        - `_posts_list.html` - subtemplate that is used in a couple of other templates with `include` directive. Contains HTML for posts lists.
        - `_users_list.html` - same as previous one but contains HTML for users lists.
        - `followers.html` and `following.html` - templates for users lists.
        - `index.html` - main templates that shows new photos feed (only for registered users).
        - `post.html` - template that shows a single post.
        - `search.html` - this template shows search result.
        - `upload.html` - template for uploading new photo.
        - `user.html` - this one shows user details.
        - `welcome.html` - main template for unregistered users. It shows login and registration forms.
    - `admin.py` - here I added some admin classes and re-registered User model.
    - `models.py` contains three models I used in the project. `UserExtended` model extends the standard User model, `Post` model is for posts, and `Comment` represents users comments.
    - `urls.py` - all application URLs.
    - `views.py` respectively, contains all application views.
  - `djangogram` - project directory.
  - `media` - this directory contains two default images (`no_avatar.png` and `no_image.png`), and here will be saved all users photos.

The project's video: https://youtu.be/JiG6MyEWxtA
