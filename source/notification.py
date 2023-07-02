from plyer import notification


def alert():
    notification.notify(
        title='POKEWARS ACTION',
        message='Bot is waiting',
        app_icon=None,
        timeout=5,
    )
