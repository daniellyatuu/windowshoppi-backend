from app.account_post.models import AccountPost
from django.shortcuts import get_object_or_404
from background_task import background
from django.utils import timezone
import httplib2


@background(schedule=timezone.now())
def verify_url(post_id):
    post = get_object_or_404(AccountPost, pk=post_id)

    link = httplib2.Http()
    try:
        response = link.request(post.url, 'HEAD')
        status_code = int(response[0]['status'])

        if status_code < 400:
            post.is_url_valid = True
            post.save()
        else:
            post.is_url_valid = False
            post.save()
    except:
        post.is_url_valid = False
        post.save()
