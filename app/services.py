class NotificationService:
    def notify(self, title, message):
        # In a real app, this would show desktop notifications
        # For now, just print to console
        print(f"{title}: {message}")
