# -*- coding: utf-8 -*-

import re
from django.template.loader import render_to_string


# En cada llamada counter.next() devuelve el prox valor de xrange
counter = iter(xrange(100))


def parse_tags(text, files):
    """
    Image:   {{img_name}}
    Resize:  {{img_name size}}
    Thumb:   {{img_name size target_name}}

    Audio:   {{audio path}}
    """
    tags = get_tags(text)
    tags_count = len(tags)

    for tag in tags:
        align = get_align(tag)
        tokens = tag.strip('{} ').split()
        html = get_html(tokens, align, files, tags_count)
        if html:
            text = text.replace(tag, html)

    return text

def get_tags(text):
    tags = re.findall('\{\{[^\}]+\}\}', text)
    return tags

def get_align(tag):
    if tag[2] == ' ' and tag[-3] == ' ':
        return 'align-center'
    elif tag[2] == ' ':
        return 'align-right'
    elif tag[-3] == ' ':
        return 'align-left'
    else:
        return ''

def get_html(tokens, align, files, tags_count):
    tokens_count = len(tokens)
    if tokens_count not in (1, 2, 3, 4):
        return

    if tokens[0] == '#audio' and tokens_count == 2:
        file = get_file(tokens[1], files)
        filepath = tokens[1] if not file else file.get_absolute_url()
        return render_to_string(
            'revista/minibloques/audio_cuerpo.html',
            {'filepath': filepath, 'id': counter.next()})

    image = get_file(tokens[0], files)
    if not image:
        return

    if tokens_count > 1:
        if not tokens[1].isdigit():
            return
        image_width = int(tokens[1])

    if tokens_count > 2:
        target = get_file(tokens[2], files)
        if not target:
            return
        rel = 'gallery' if tags_count == 1 else 'gallery[body]'

    if tokens_count > 3:
        if not tokens[3].isdigit():
            return
        target_width = int(tokens[3])

    return render_to_string('revista/minibloques/imagen_cuerpo.html', locals())

    html = '<div%s>' % (' class="%s"' % align if align else '')
    image = get_file(tokens[0], files)
    if len(tokens) == 1:
        html += '<img src="%s" alt="%s" title="%s" />' % (image.get_absolute_url(), image.alt, image.epigrafe)
    if len(tokens) == 2:
        width = int(tokens[1])
        html += '<img src="/cache/%d%s" alt="%s" title="%s" />' % (width, image.get_absolute_url(), image.alt, image.epigrafe)
    if len(tokens) == 3:
        image2 = get_file(tokens[2], files)
        width = int(tokens[1])
        rel = 'prettyPhoto' if tags_count == 1 else 'prettyPhoto[gallery]'
        html += '<a href="%s" title="%s", rel="%s"><img src="/cache/%d%s" alt="%s" title="%s"></a>' % (image2.get_absolute_url(), image2.epigrafe, rel, width, image.get_absolute_url(), image.alt, image.epigrafe)
    html += '</div>'
    return html

def get_file(file_name, files):
    for file in files:
        if file.nombre == file_name:
            return file

def get_audio_paths(text, files):
    """
    Audio:   {{audio path}}
    """
    paths = []
    for tag in get_tags(text):
        tokens = tag.strip('{} ').split()
        if tokens[0] == '#audio' and len(tokens) == 2:
            file = get_file(tokens[1], files)
            if file:
                paths.append(file.get_absolute_url())
            else:
                paths.append(tokens[1])

    return paths

