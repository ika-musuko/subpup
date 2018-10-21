def availability_to_readable(availability: str) -> str:
    availability_tokens = availability.split("~")
    # recurring
    if availability_tokens[0] == "R":
        days_of_week = availability_tokens[1].replace(",", ", ")
        time = availability_tokens[2]
        return "%s %s" % (days_of_week, time)

    # one time
    return availability_tokens[1]

