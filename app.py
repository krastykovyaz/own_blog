from random import randint
from flask import Flask, render_template, url_for
from faker import Faker
import os
import datetime

fake = Faker()

app = Flask(__name__)
application = app

images_ids = ['6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
              '2d2ab7df-cdbc-48a8-a936-35bba702def5',
              '7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
              'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
              'cab5b7f2-774e-4884-a200-0c0180fa777f']

def generate_comments(replies=True):
    comments = []
    for i in range(randint(1, 3)):
        comment = { 'author': fake.name(), 'text': fake.sentence(nb_words=randint(2, 5)) }
        if replies:
            comment['replies'] = generate_comments(replies=False)
        comments.append(comment)
    return comments

# def read_post_title(i):
#     directory = './app/static/text/'
#     for filename in os.listdir(directory):
#         if filename.endswith(str(i)+'.txt'):
#             handle = open(directory + filename)
#             for line in handle:
#                 title = line.strip('\n')
#                 break                
#     return title

# def get_date(i):
#     directory = './app/static/images/'
#     for filename in os.listdir(directory):
#         if filename.endswith(str(i)+'.jpg'):
#             t = os.path.getmtime(directory + filename)
#             date = str(datetime.datetime.fromtimestamp(t))
#             date = date.split(' ')
#             date = date[0].split('-')
#             date_post = str(date[2]) + '.' + str(date[1]) + '.' + str(date[0])
#     return datetime.datetime.fromtimestamp(t)

# def get_img(i):
#     directory = './app/static/images/'
#     for filename in os.listdir(directory):
#         if filename.endswith(str(i)+'.jpg'):
#             pic = filename
#     return pic


# def read_post(i):
#     directory = './app/static/text/'
#     for filename in os.listdir(directory):
#         if filename.endswith(str(i)+'.txt'):
#             handle = open(directory + filename)
#             post = ''
#             i = 0
#             for line in handle:
#                 if i > 0:
#                     post += line.strip('\n')
#                     post += '\n'
#                 i += 1
#     return post

def generate_post(i):
    return {
        'title': fake.sentence(nb_words=randint(5, 10)),
        'text': fake.paragraph(nb_sentences=100),
        'author': fake.name(),
        'date': fake.date_time_between(start_date='-2y', end_date='now'),
        'image_filename': f'{images_ids[i]}.jpg',
        'comments': generate_comments()
    }
# def create_post(i):
#     return {
#         'title': read_post_title(i),
#         'text': read_post(i),
#         'author': 'Александр Ковязин',
#         'date': get_date(1),
#         'image_filename': get_img(i),
#         'comments': generate_comments()
#     }

# print(type(create_post(1)))
f_posts = [generate_post(i) for i in range(5)]
# print(create_post(1))
# f_posts.append(create_post(1))
# print(type(full))
# posts_list = sorted([generate_post(i) for i in range(5)], key=lambda p: p['date'], reverse=True)
posts_list = sorted(f_posts, key=lambda p: p['date'], reverse=True)
# print(posts_list[0]['date'])
comments = generate_comments()

@app.route('/')
def index():
    return render_template('index.html', delete_footer=True)

@app.route('/posts')
def posts():
    title = 'Последние посты'
    return render_template('posts.html', title=title, posts=posts_list)

@app.route('/posts/<int:index>')
def post(index):
    try:
        p = posts_list[index]
    except:
        return render_template('404.html', title='Cтраница не найдена')
    return render_template('post.html', title=p['title'], post=p, comments=comments)

@app.route('/about')
def about():
    title = 'Об авторе'
    return render_template('about.html', title=title)

@app.context_processor
def inject_now():
    return {'now': datetime.datetime.utcnow()}

if __name__ == "__main__":
    app.run()