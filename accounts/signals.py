from .utils import (
    generate_student_credentials,
    generate_lecturer_credentials,
    generate_parent_credentials,
    send_new_account_email,
    generate_password,
)


def post_save_account_receiver(instance=None, created=False, *args, **kwargs):
    """
    Send email notification
    """
    if created:
        if instance.is_student:
            if not instance.username:
                username, password = generate_student_credentials()
                instance.username = username
            else:
                password = generate_password()
            
            instance.set_password(password)
            instance.save()
            send_new_account_email(instance, password)

        if instance.is_lecturer:
            if not instance.username:
                username, password = generate_lecturer_credentials()
                instance.username = username
            else:
                password = generate_password()

            instance.set_password(password)
            instance.save()
            send_new_account_email(instance, password)
        
        if instance.is_parent:
            if not instance.username:
                username, password = generate_parent_credentials()
                instance.username = username
            else:
                password = generate_password()

            instance.set_password(password)
            instance.save()
            send_new_account_email(instance, password)
