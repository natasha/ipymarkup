

def show_html(lines):
    from IPython.display import display, HTML

    html = ''.join(lines)
    display(HTML(html))
