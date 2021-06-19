from django.contrib import admin
from django.contrib.auth import get_user_model
from sms.models import Contact, ContactList, SMS, Subscription
from bulk_manager.models import Campaign
from . import settings

User = get_user_model()


class MyAdminSite(admin.AdminSite):
    index_title = 'Dashboard'
    #enable_nav_sidebar = False

    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}

        subscription = Subscription.objects.first()

        # Adding my context here
        extra_context.update({
            'insight': {
                'users': User.objects.count(),
                'contact_lists': ContactList.objects.count(),
                'contacts': Contact.objects.count(),
                'sms': SMS.objects.count(),
                'campaigns': Campaign.objects.count(),
                'subscription': subscription,
                'contact_us': {
                    'description': settings.CONTACT_US_AND_SUPPORT_DESCRIPTION,
                    'url': settings.CONTACT_US_AND_SUPPORT_URL
                },
            }
        })

        return super().index(request, extra_context=extra_context)
