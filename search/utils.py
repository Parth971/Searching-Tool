from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from administrator.models import SearchData, ViewData
from search.models import Framework


def get_model_object(model_class, query):
    """
    Retrieve a single object from the specified model class based on the provided query.

    Args:
        model_class (Model): The model class to retrieve the object from.
        query (dict): The query parameters used to filter the objects.

    Returns:
        Model: The retrieved object or None if not found.
    """
    return model_class.objects.filter(**query).first()


def send_inquiry_email(user, message, framework):
    """
    Send an inquiry email to the specified user regarding a framework.

    Args:
        user (User): The user to send the email to.
        message (str): The inquiry message.
        framework (Framework): The framework related to the inquiry.

    Returns:
        None
    """
    context = {
        'subject': 'Inquiry',
        'username': f"{user.first_name} {user.last_name}",
        'user_email': user.email,
        'message': message,
        'framework_name': framework.name,
        'framework_id': framework.id,
    }
    send_mail(settings.INQUIRY_EMAIL, 'inquiry', context)


def send_mail(to, template, context):
    """
    Send an email with the specified template and context to the given recipient.

    Args:
        to (str): The email recipient.
        template (str): The email template name.
        context (dict): The context data for the email template.

    Returns:
        None
    """
    html_content = render_to_string(f'search/inquiry/{template}.html', context)
    msg = EmailMessage(context['subject'], html_content, to=[to])
    msg.send()


def search_data(data, user):
    """
    Store search data in the database for the specified user and frameworks.

    Args:
        data (list): The search data containing framework information.
        user (User): The user associated with the search data.

    Returns:
        None
    """
    for framework in data:
        framework_instance = get_model_object(Framework, query={'id': framework.get('framework_id')})
        SearchData.objects.create(framework=framework_instance, user=user)

