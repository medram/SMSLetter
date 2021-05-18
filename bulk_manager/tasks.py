from background_task import background


@background
def campaign_task(campaign_id):
    print('task created.')
    print('start sending sms messages...')
