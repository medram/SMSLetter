from background_task import background

from .models import Campaign
from sms.models import Subscription
from sms.common import send_sms
from .exceptions import StoppedCampaign


@background
def campaign_task(payload):
    campaign_id = payload.get('campaign_id')
    subscription = Subscription.objects.first()

    print(f'Campaign {campaign_id} started...')
    campaign_stopped = False
    try:
        c = Campaign.objects.get(pk=campaign_id)
        contacts = []

        # changing Campaign status
        c.status = c.Status.SENDING
        c.save()

        for l in c.contact_lists.all():
            contacts.extend(l.contacts.all())

        messages = c.messages.all()

        for contact in contacts:
            try:
                send_sms(contact, messages, subscription, campaign=c)
            except StoppedCampaign:
                campaign_stopped = True
                break
            except Exception as e:
                print(e)

    except Campaign.DoesNotExist:
        print(f'campaign ({campaign_id}) not found.')
    finally:
        if campaign_stopped is False:
            # changing Campaign status
            c.status = c.Status.COMPLETED
            c.save()
