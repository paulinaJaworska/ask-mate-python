# Ask mate

Ask mate is a stack overflow like website.

##Features
- you can perform CRUD operations on questions, answers and comments
- you can add and delete tags
- you can add images
- MVC was pattern used 

##Tech stack 
- Flask
- PostgreSQL
- HTML & CSS 

##Clean code
All the modules have been named according to clean code rules.
Modules are named like that:
![moodule_division](static/readme/module_division.png)

so you can use their methods like this:
question.add(form_data)
answer.add(form_data, question_id) 

which greatly increase readability of code.

## Question view
![question_view](static/readme/question_view.png)

## Add answer view
![add_answer](static/readme/add_answer.png)