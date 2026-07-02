import html


def escape_html(value):
    return html.escape(str(value), quote=True)
