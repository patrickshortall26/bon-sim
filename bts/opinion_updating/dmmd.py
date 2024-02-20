def position_check(agent):
    # Check agents position doesn't round up to an index out of range
    for i in range(agent.p.ndim):
        if int(agent.pos[i]) == agent.p.size:
            agent.pos[i] -= 0.5
    return agent

def collect_evidence(agent):
    agent = position_check(agent)
    safe = not agent.model.search_space[int(agent.pos[0]),int(agent.pos[1])]
    if safe:
        agent.observations[0] += 1
    else:
        agent.observations[1] += 1
    return agent

def explore(agent):
    """ 
    Explore the environment and see if evidence supports current hypothesis
    """
    agent = collect_evidence(agent)
    # Change to dissemination state after explore time is over
    if agent.time_in_state % agent.explore_time == 0:
        agent.model.observations[0] += agent.observations[0]
        agent.model.observations[1] += agent.observations[1]
        if agent.opinion == 0.05:
            agent.option_quality = int(agent.model.nprandom.exponential((agent.observations[1]/agent.time_in_state)*agent.p.tau_disseminate))
            agent.observations = [0,1]
        elif agent.opinion == 0.95:
            agent.option_quality = int(agent.model.nprandom.exponential((agent.observations[0]/agent.time_in_state)*agent.p.tau_disseminate))
            agent.observations = [1,0]

        agent.state = "dissemination"
        agent.time_in_state = 0

        agent.ids_seen = []

    return agent

def disseminate(agent):
    inner_nbs = agent.neighbors(agent, distance=agent.p.detection_radius)
    if agent.option_quality < 1:
        # Update opinion with whatever more of their neighbours have said
        # If neighbours have said equal, keep same opinion
        if agent.observations[0] > agent.observations[1]:
            agent.opinion = 0.95
        elif agent.observations[1] > agent.observations[0]:
            agent.opinion = 0.05
        else:
            agent.opinion = agent.opinion

        agent.state = "exploration"
        agent.time_in_state = 0

        agent.explore_time = int(agent.model.nprandom.exponential(agent.p.tau_exploration)) + 1

        agent.observations = [0,0]
    else:
        if "Granuloma" not in inner_nbs.type:
            for nb in inner_nbs:
                # See what the neighbours (in dissemination state) are saying, don't count neighbours twice
                if nb.state == "dissemination" and nb.id not in agent.ids_seen:
                    agent.ids_seen.append(nb.id)
                    if nb.opinion == 0.05:
                        agent.observations[1] += 1
                    elif nb.opinion == 0.95:
                        agent.observations[0] +=1
        agent.option_quality -= 1 
    return agent

    

def update_opinion(agent):
    """
    Update agent's opinion through evidential updating and opinion pooling
    """
    agent.time_in_state += 1
    if agent.state == "exploration":
        agent = explore(agent)
    elif agent.state == "dissemination":
        agent = disseminate(agent)

    return agent