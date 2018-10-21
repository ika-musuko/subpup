from project import app

@app.context_processor
def inject_app_context():
    return {
        "debug": app.debug,
        "availability_to_readable" : availability_to_readable
    }


def availability_to_readable(availability: str) -> str:
    if availability is None:
        return "NULL"
    availability_tokens = availability.split("~")
    # recurring
    if availability_tokens[0] == "R":
        days_of_week = availability_tokens[1].replace(",", ", ")
        time = availability_tokens[2]
        return "%s %s" % (days_of_week, time)

    # one time
    return availability_tokens[1]

