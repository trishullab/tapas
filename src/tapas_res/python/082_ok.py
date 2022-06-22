def process_message(things):
    return ','.join((str(e['x']) + " " + str(e['y'])) for e in things)