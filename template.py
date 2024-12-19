class Challenge:
    id = 0
    name = ""
    description = ""
    max_attempts = 0
    value = 0
    category = ""
    type = ""
    state = ""
    requirements = None
    connection_info = None
    next_id = None
    attribution = None

class DynamicChallenge:
    id = 0
    initial = 0
    minimum = 0
    decay = 0
    function = "logarithmic"

class DynamicDockerChallenge:
    id = 0
    initial = None
    minimum = None
    decay = None
    memory_limit = ""
    cpu_limit = 0
    dynamic_score = 0
    docker_image = ""
    redirect_type = ""
    redirect_port = ""

class File:
    id = 0
    type = "challenge"
    location = ""
    challenge_id = 0
    page_id = None
    sha1sum = None

class Flag:
    id = 0
    challenge_id = 0
    type = "static"
    content = ""
    data = ""

class Hint:
    id = 0
    type = "standard"
    challenge_id = 0
    content = ""
    cost = 0
    requirements = {
        "prerequisites": []
    }