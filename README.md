# Secret Santa
> This module allows to send emails in the name of Secret Santa using an SMTP email server.


This file will become your README and also the index of your documentation.

## Install

`pip install your_project_name`

## How to use

Please folllow the example below to create and send e-mails from Secret Santa.

```
from secretsanta.core import *
from pathlib2 import Path
```

```
sender_name = 'Santa Claus'
sender_email = 'santa@claus.com'
subject = 'Christmas Lottery'
input_path = Path('input_data')

lottery = SecretSanta(sender_name, sender_email, subject, input_path, True)
```

    Participants:
    -------------
    John Doe (en, m): john.doe@gmail.com
    Jane Doe (en, f): jane.doe@gmail.com
    Hans Muster (de, m): hans.muster@gmail.com
    Marta Muster (de, f): marta.muster@gmail.com
    -------------
    Rule [must] failed: John --> Marta
    Rule [must] failed: John --> Marta
    Rule [not] failed: Hans --> Marta
    Rule [must] failed: John --> Marta
    Rule [not] failed: Jane --> John
    Rule [not] failed: Marta --> Hans
    Rule [not] failed: Hans --> Marta


```
lottery.print_assignments()
```

    Participants --> Presemtees:
    ----------------------------
    John --> Marta
    Jane --> Hans
    Hans --> Jane
    Marta --> John
    ----------------------------


## Send Mail from disk

```
from email.parser import BytesParser
from email import policy

# set user and password of the smtp server
user = ''
pw = ''

name = 'Jane'
fn_email = input_path / f'message_{name}.msg'

with open(fn_email, 'rb') as fp:
    email = BytesParser(policy=policy.default).parse(fp)

# uncomment after setting user and pw above
#send_smtp_email('host', port, user, pw, email)
```

```
print('To:', email['to'])
print('From:', email['from'])
print('Subject:', email['subject'])
```

    To: jane.doe@gmail.com
    From: Santa Claus <santa@claus.com>
    Subject: Christmas Lottery


```
richest = email.get_body()
body = richest.get_body(preferencelist=('html'))
html = body.get_content()
print(html)
```

    <!DOCTYPE html>
    <html>
    
    <head>
        <title>Secret Santa</title>
        <link rel="preconnect" href="https://fonts.gstatic.com">
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@200&display=swap" rel="stylesheet">
        <style>
            div.main {
                font-family: 'Montserrat', sans-serif;
                font-size: 14px;
                max-width: 600px;
                margin: 20px 10% 10px 10%;
            }
        </style>
    </head>
    
    <body>
        <div class="main">
            <img src="cid:santa.jpg" alt="Santa Claus Image" width="auto">
            <h1>Xmas Lottery 2020</h1>
            <p>Dear Jane</p>
            <p>Soon it will be Christmas again. Unfortunately, I am far behind with my preparations, so that I am dependent
                on
                your help.
            </p>
            <p>Could you organize a little present for <b>Hans</b> until Christmas and secretly put it under the
                Christmas tree? That would be really wonderful ...
            </p>
            <p>Best regards<br>Santa Claus</p>
        </div>
    </body>
    
    </html>
    


```
import IPython

html = html.replace('cid:santa.jpg', 'input_data/santa.jpg')
print(html)
```

    <!DOCTYPE html>
    <html>
    
    <head>
        <title>Secret Santa</title>
        <link rel="preconnect" href="https://fonts.gstatic.com">
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@200&display=swap" rel="stylesheet">
        <style>
            div.main {
                font-family: 'Montserrat', sans-serif;
                font-size: 14px;
                max-width: 600px;
                margin: 20px 10% 10px 10%;
            }
        </style>
    </head>
    
    <body>
        <div class="main">
            <img src="input_data/santa.jpg" alt="Santa Claus Image" width="auto">
            <h1>Xmas Lottery 2020</h1>
            <p>Dear Jane</p>
            <p>Soon it will be Christmas again. Unfortunately, I am far behind with my preparations, so that I am dependent
                on
                your help.
            </p>
            <p>Could you organize a little present for <b>Hans</b> until Christmas and secretly put it under the
                Christmas tree? That would be really wonderful ...
            </p>
            <p>Best regards<br>Santa Claus</p>
        </div>
    </body>
    
    </html>
    


```
IPython.display.HTML(data = html)
```




<!DOCTYPE html>
<html>

<head>
    <title>Secret Santa</title>
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@200&display=swap" rel="stylesheet">
    <style>
        div.main {
            font-family: 'Montserrat', sans-serif;
            font-size: 14px;
            max-width: 600px;
            margin: 20px 10% 10px 10%;
        }
    </style>
</head>

<body>
    <div class="main">
        <img src="https://github.com/eandreas/secretsanta/raw/master/input_data/santa.jpg" alt="Santa Claus Image" width="auto">
        <h1>Xmas Lottery 2020</h1>
        <p>Dear Jane</p>
        <p>Soon it will be Christmas again. Unfortunately, I am far behind with my preparations, so that I am dependent
            on
            your help.
        </p>
        <p>Could you organize a little present for <b>Hans</b> until Christmas and secretly put it under the
            Christmas tree? That would be really wonderful ...
        </p>
        <p>Best regards<br>Santa Claus</p>
    </div>
</body>

</html>



