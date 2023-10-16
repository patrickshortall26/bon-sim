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
        agent.observations[1] += 1
    else:
        agent.observations[0] += 1
    return agent

def explore(agent):
    """ 
    Explore the environment and see if evidence supports current hypothesis
    """
    agent = collect_evidence(agent)
    agent.time_in_state += 1
    # Change to dissemination state with a 3 percent chance
    if agent.model.random.random() <= 0.03:
        if agent.opinion == 0.05:
            agent.option_quality = int((agent.observations[0]/agent.time_in_state)*20)
        elif agent.opinion == 0.95:
            agent.option_quality = int((agent.observations[1]/agent.time_in_state)*20)
        agent.state = "dissemination"
        agent.observations = [0,0]
        agent.time_in_state = 0
    return agent

def disseminate(agent):
    inner_nbs = agent.neighbors(agent, distance=agent.p.pooling_radius)
    if agent.option_quality < 1:
        # Update opinion with whatever more of their neighbours have said
        # If neighbours have said equal, keep same opinion
        if agent.observations[0] > agent.observations[1]:
            agent.opinion = 0.05
        elif agent.observations[1] > agent.observations[0]:
            agent.opinion = 0.95
        else:
            agent.opinion = agent.opinion
        agent.state = "exploration"
        agent.observations = [0,0]
    else:
        if "Granuloma" not in inner_nbs.type:
            for nb in inner_nbs:
                # See what the neighbours (in dissemination state) are saying
                if nb.state == "dissemination":
                    if nb.opinion == 0.05:
                        agent.observations[0] += 1
                    elif nb.opinion == 0.95:
                        agent.observations[1] +=1
        agent.option_quality -= 1 
    return agent

    

def update_opinion(agent):
    """
    Update agent's opinion through evidential updating and opinion pooling
    """
    if agent.state == "exploration":
        agent = explore(agent)
    elif agent.state == "dissemination":
        agent = disseminate(agent)

    return agent