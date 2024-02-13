from scipy.stats import beta

def position_check(agent):
    # Check agents position doesn't round up to an index out of range
    for i in range(agent.p.ndim):
        if int(agent.pos[i]) == agent.p.size:
            agent.pos[i] -= 0.5
    return agent

def make_observation(agent):
    """
    See if the area is white or black
    white = safe
    black = unsafe
    """
    # Check agents position isn't out of index range
    agent = position_check(agent)
    # Make observation
    safe = not agent.model.search_space[int(agent.pos[0]),int(agent.pos[1])]
    if safe:
        agent.observations[0] += 1
        agent.last_observation = 0.95
    else:
        agent.observations[1] += 1
        agent.last_observation = 0.05
    return agent

def neighbour_time(agent):
    nbs = agent.neighbors(agent, distance=agent.p.detection_radius)
    if "Granuloma" not in nbs.type:
        for nb in nbs:
            if agent.p.u_plus == True and nb.opinion != 0.5:        # If neighbour is 'decided' take that as their opinion
                # See what the neighbours are saying
                if nb.opinion == 0.95:
                    agent.observations[0] += 1
                elif nb.opinion == 0.05:
                    agent.observations[1] += 1
            else:                                                   # If not get what their last observation was
                # See what the neighbours are saying
                if nb.last_observation == 0.95:
                    agent.observations[0] += 1
                elif nb.last_observation == 0.05:
                    agent.observations[1] += 1
    return agent

def cdf_check(agent):
    """
    Get posterior for agent at 0.5 and see if that meets the critical threshold for a decision to be made
    """
    p = beta.cdf(0.5, agent.observations[0] + agent.p.alpha_0, agent.observations[1] + agent.p.alpha_0)
    if p > agent.p.p_c:
        agent.opinion = 0.05
    elif (1-p) > agent.p.p_c:
        agent.opinion = 0.95
    return agent


def update_opinion(agent):
    """
    Update agent's opinion using the 'Bayes Bots' algorithm
    """
    agent.time_since_observation += 1
    # Make an observation every tau seconds
    if agent.time_since_observation == agent.p.tau:
        agent = make_observation(agent)
        agent.time_since_observation = 0
    # If undecided, get the neighbouring agents last observations and update posterior
    if agent.opinion == 0.5:
        # See what the neighbours are saying
        agent = neighbour_time(agent)
        # Try and make a decision
        agent = cdf_check(agent)

    return agent