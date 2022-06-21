def collate(samples):
    # 'samples (graph, label)'
    graphs, labels = map(list, zip(*samples))
    for g in graphs:
        print(g)