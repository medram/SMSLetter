from django.contrib import admin
from django.contrib.auth import get_user_model
from sms.models import Contact, ContactList, SMS, ContactUs, Subscription
from bulk_manager.models import Campaign

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
                'contact_and_support': """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
		    tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
		    quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
		    consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
		    cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
		    proident, sunt in culpa qui officia deserunt mollit anim id est laborum.""",
            }
        })

        return super().index(request, extra_context=extra_context)
