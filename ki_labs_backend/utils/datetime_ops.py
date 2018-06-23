def get_rrule_format(datetime):
    """
    The rrulestr() function in the dateutils library requires a particular
    datetime formatting for the rrule string. This function formats a
    datetime object in the format expected by the rrulestr() function.

    Input: A datetime object e.g. datetime.datetime(2018, 06, 23, 9, 0, 0)
    Output: A string e.g. 20180623T090000
    """

    return datetime.strftime("%Y%m%dT%H%M%S")
