from background_task import background


@background(schedule=5)
def notify_user(user_id):
    print('send email and normal sms to user with this id', user_id)
    # # lookup user by id and send them a message
    # user = User.objects.get(pk=user_id)
    # user.email_user('Here is a notification', 'You have been notified')
