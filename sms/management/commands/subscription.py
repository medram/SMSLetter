import djclick as click

from sms.models import Subscription


@click.group()
def subscription():
    pass


@subscription.command('upgrade', short_help='Upgrade subscription plan (e.g. 1000/1000).')
@click.argument('plan')
# @click.option('--plan', type=click.STRING, help='Upgrade subscription plan (e.g. 1000/1000).')
def upgrade(plan):
    if plan:
        upgrade = [int(n) for n in plan.split('/')]
        subscription = Subscription.objects.first()
        subscription.amount = upgrade[0]
        subscription.total = upgrade[1]
        try:
            subscription.save()
            click.secho(f'Updated Successfully.', fg='green')
        except Exception:
            click.secho(f'Unable to update this subscription plan!', fg='red')


@subscription.command('show', short_help='Show subscription plan information.')
# @click.option('--show', is_flag=True, )
def show():
    subscription = Subscription.objects.first()
    click.secho(
        f'Subscription: {subscription.amount}/{subscription.total}', fg='green')


# # regster additional commands
# subscription.add_command(upgrade)
# subscription.add_command(show)
