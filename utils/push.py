import datetime
from push_notifications.models import APNSDevice, GCMDevice


def send_push(user, text, action=None):
    a = APNSDevice.objects.filter(user = user)
    b = GCMDevice.objects.filter(user = user)
    if a.exists():
        a[0].send_message(text, badge=1, sound="default")
    elif b.exists():
        b[0].send_message(text)