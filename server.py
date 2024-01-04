from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
from html import escape


html = """
<html>
<body>
   <form method="post" action="/form">
        <p>
           Age: <input type="text" name="age" value="{age}">
        </p>
        <p>
            Hobbies:
            <input
                name="hobbies" type="checkbox" value="software"
                {checked_software}
            > Software
            <input
                name="hobbies" type="checkbox" value="tunning"
                {checked_tunning}
            > Auto Tunning
        </p>
        <p>
            <input type="submit" value="Submit">
        </p>
    </form>
    <p>
        Age: {age}<br>
        Hobbies: {hobbies}
    </p>
</body>
</html>
"""


def application (environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size)
    request_dict = parse_qs(request_body.decode())

    age = request_dict.get('age', [''])[0]
    hobbies = request_dict.get('hobbies', [])

    age = escape(age)
    hobbies = [escape(h) for h in hobbies]

    response_body = html.format(
        checked_software='checked' if 'software' in hobbies else '',
        checked_tunning='checked' if 'tunning' in hobbies else '',
        age=age or 'Empty',
        hobbies=', '.join(hobbies or ['No Hobbies?']),
    )

    status = '200 OK'

    response_headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(response_body)))
    ]
    print('imhere')
    start_response(status, response_headers)
    return [response_body.encode()]


httpd = make_server ('python_wsgi', 9000, application)
httpd.serve_forever()
