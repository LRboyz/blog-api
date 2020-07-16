# -*- coding: utf8 -*-
from apps import create_app

app = create_app()


@app.route('/', methods=['GET'])
def blog_test():
    return """<style type="text/css">*{ padding: 0; margin: 0; } div{ padding: 4px 48px;} a{color:#2E5CD5;cursor: 
    pointer;text-decoration: none} a:hover{text-decoration:underline; } body{ background: #fff; font-family: 
    "Century Gothic","Microsoft yahei"; color: #333;font-size:18px;} h1{ font-size: 100px; font-weight: normal; 
    margin-bottom: 12px; } p{ line-height: 1.6em; font-size: 42px }</style><div style="padding: 24px 48px;"><p> 
    Hello <br/><span style="font-size:30px">欢迎光临，这是 LRboy 的博客API。</span></p></div> """


if __name__ == '__main__':
    if app.debug:
        # 使用Flask的Debug工具，如果不要可以在config.cfg的 DEBUG_TB_ENABLED = False
        from flask_debugtoolbar import DebugToolbarExtension
        toolbar = DebugToolbarExtension(app)

    app.run(host="0.0.0.0", debug=True, port=5000)  #
