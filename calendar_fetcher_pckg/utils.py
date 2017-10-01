from dateutil.parser import parse


def filter_features(old_dict):
    """
    From an input dictionary, filter everything out and leave only
    start_datetime, end_datetime and summary.
    :param old_dict: Input dictionary
    :return: Filtered dictionay.
    """
    new_dict = {
        "start_datetime": old_dict['start']['dateTime'],
        "end_datetime": old_dict['end']['dateTime'],
        "summary": old_dict['summary']
    }
    return new_dict


def augment_with_duration(input_dict):
    input_dict['duration_minutes'] = (
        parse(input_dict['end_datetime'])
        - parse(input_dict['start_datetime'])
    ).seconds / 60


def pre_process(raw_events, useful_summaries_abspath):
    """
    This functions takes raw_events as returned by the GoogleCalendarService.get_events()
    and parses them into a clean form for further analysis. It uses a file to indicate it
    what event summaries to keep, and which to discard.
    :param raw_events: The result of the GoogleCalendarService.get_events() call.
    :param useful_summaries_abspath: An absolute filepath of a file containing the summaries to keep.
    :return: The events processed for further analysis.
    """
    events_with_durations = []
    for e in raw_events:
        try:
            valid_event = filter_features(e)
            augment_with_duration(valid_event)
            events_with_durations.append(valid_event)
        except KeyError:
            pass

    with open(useful_summaries_abspath, 'r') as file:
        names = {line.strip(): line.strip() for line in file}

    canonical_events = []
    for event in events_with_durations:
        try:
            valid_name = names[event['summary'].lower().split()[0]]
            event['summary'] = valid_name
            canonical_events.append(event)
        except KeyError:
            pass
    return canonical_events
