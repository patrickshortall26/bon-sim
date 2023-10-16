import numpy as np

def position_check(agent):
    # Check agents position doesn't round up to an index out of range
    for i in range(agent.p.ndim):
        if int(agent.pos[i]) == agent.p.size:
            agent.pos[i] -= 0.5
    return agent

def bounds_check(agent):
    """
    Check that agents opinion hasn't strayed out of [0.05,0.95]
    If it has clamp it back to 0.05 or 0.95 respectively
    """
    if agent.opinion < 0.05:
            agent.opinion = 0.05
    elif agent.opinion > 0.95:
            agent.opinion = 0.95
    return agent
    
def pool_opinions(agent, nbs):
    """
    Pool the opinions from nearby agents
    and update opinion
    """
    # Pool if agent has neighbours and none are granuloma
    if len(nbs) > 0 and "Granuloma" not in nbs.type:
        nbs_ops_array = np.array(nbs.opinion)
        pool_array = np.append(nbs_ops_array, agent.opinion)
        h1 = (np.prod(pool_array))**agent.p.w
        h2 = (np.prod(1-pool_array))**agent.p.w
        # Update opinion using SProdOp
        agent.opinion = h1/(h1+h2)
    return agent

def evidentially_update(agent):
    """
    Update opinions from evidence
    """
    agent = position_check(agent)
    safe = not agent.model.search_space[int(agent.pos[0]),int(agent.pos[1])]
    if safe:
        agent.opinion = ((1-agent.p.alpha)*agent.opinion)/(agent.opinion+agent.p.alpha-2*agent.p.alpha*agent.opinion)
    else:
        agent.opinion = ((1-agent.p.alpha)*(1-agent.opinion))/((1-agent.p.alpha)*agent.opinion+agent.p.alpha*(1-agent.opinion))
    return agent

def update_opinion(agent):
    """
    Update agent's opinion through evidential updating and opinion pooling
    """
    if agent.model.random.random() <= agent.p.evidence_epsilon:
        agent = evidentially_update(agent)
        agent = bounds_check(agent)
    if agent.model.random.random() <= agent.p.pooling_epsilon:
        inner_nbs = agent.neighbors(agent, distance=agent.p.pooling_radius)
        agent = pool_opinions(agent, inner_nbs)
        agent = bounds_check(agent)
    return agent