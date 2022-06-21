def collate(samples):
    for z in zip(*samples):
        print(z)