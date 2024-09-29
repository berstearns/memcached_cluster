#!/usr/bin/python
from jinja2 import Template
from datetime import datetime
import os
import time

script_folderpath = os.path.dirname(os.path.abspath(__file__))
print(script_folderpath)
while True:
    time.sleep(30)
    print("new render")
    now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    blog_template = Template(open(os.path.join(script_folderpath, "blog.jinja2")).read())
    content = blog_template.render(render_time=now)
    with open(os.path.join(script_folderpath, "blog.html"),"w") as outf:
        outf.write(content)
