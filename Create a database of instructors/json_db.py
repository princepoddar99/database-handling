import json
import _sqlite3

conn = _sqlite3.connect('rosterdb.sqlite')
curr = conn.cursor()

curr.executescript('''
   DROP TABLE IF EXISTS Users;
   DROP TABLE IF EXISTS Member;
   DROP TABLE IF EXISTS Course;

   CREATE TABLE User(
      id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
      name TEXT UNIQUE
    );

   CREATE TABLE Course(
      id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
      title TEXT UNIQUE
   );

   CREATE TABLE Member(
      user_id INTEGER,
      course_id INTEGER,
      role INTEGER,
      PRIMARY KEY (user_id, course_id)
   ) 
''')

#roster_data.json
fname = input('Enter the file name:')
fh = open(fname)
json_data = json.load(fh)

for entry in json_data :
    name = entry[0]
    course = entry[1]
    instructor = entry[2]

    print((name, course, instructor ))

    curr.execute(''' INSERT OR IGNORE INTO User (name) VALUES ( ? )''',(name,))
    curr.execute(''' SELECT id FROM User WHERE name = ? ''',(name,))
    user_id = curr.fetchone()[0]

    curr.execute(''' INSERT OR IGNORE INTO Course (title) VALUES ( ? )''', (course,))
    curr.execute(''' SELECT id FROM Course WHERE title = ? ''', (course,))
    course_id = curr.fetchone()[0]

    curr.execute(''' INSERT OR REPLACE INTO Member (user_id, course_id, role) VALUES (?,?,?)''', (user_id,course_id, instructor))

    conn.commit()