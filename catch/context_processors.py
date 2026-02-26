import os
import random

from django.conf import settings


def random_background(request):
    """Return a randomly selected background image path stored in session.

    The function will choose a random file from
    ``static/images/fishing`` the first time it is called for a given
    session.  That value is kept in ``request.session['background']`` so
    the same picture persists until the session is flushed (which happens
    on logout by default).  A new login therefore triggers a new random
    selection.

    The returned dictionary provides ``random_bg`` for templates, which is
    the relative path (from ``STATIC_URL``) of the chosen image.
    """
    if 'background' not in request.session:
        images_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'fishing')
        try:
            pics = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]
        except FileNotFoundError:
            pics = []
        if pics:
            choice = random.choice(pics)
            request.session['background'] = f'images/fishing/{choice}'
    return {'random_bg': request.session.get('background', '')}
