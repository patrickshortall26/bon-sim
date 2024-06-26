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

def collect_evidence(agent):
    agent = position_check(agent)
    safe = not agent.model.search_space[int(agent.pos[0]),int(agent.pos[1])]
    if safe:
        agent.obs_count += 1
    else:
        agent.obs_count -= 1
    return agent
    
def pool_opinions(agent, nbs):
    """
    Pool the opinions from nearby agents
    and update opinion
    """
    # Pool if agent has neighbours and none are granuloma
    if len(nbs) > 0 and "Granuloma" not in nbs.type:
        nbs_ops_array = np.array(nbs.opinion)
        pool_array = np.append(nbs_ops_array, agent.opinion)    # add agent's opinion back in
        h1 = (np.prod(pool_array))**agent.p.w
        h2 = (np.prod(1-pool_array))**agent.p.w
        # Update opinion using SProdOp
        agent.opinion = h1/(h1+h2)
    return agent

def evidentially_update(agent):
    """
    Update opinions from evidence
    """
    if agent.obs_count > 0:
        agent.opinion = ((1-agent.p.alpha)*agent.opinion)/(((1-agent.p.alpha)*agent.opinion)+agent.p.alpha*(1-agent.opinion))
    elif agent.obs_count < 0:
        agent.opinion = (agent.p.alpha*agent.opinion)/((agent.p.alpha*agent.opinion)+((1-agent.p.alpha)*(1-agent.opinion)))
    else:
        pass
        
    return agent

def update_opinion(agent):
    """
    Update agent's opinion through evidential updating and opinion pooling
    """
    agent = collect_evidence(agent) # Update observations
    if agent.model.t % agent.p.tau_evidence == 0:
        agent = evidentially_update(agent)
        agent = bounds_check(agent)
        agent.obs_count = 0
    if agent.model.t % agent.p.tau_sharing == 0:
        inner_nbs = agent.neighbors(agent, distance=agent.p.detection_radius)
        agent = pool_opinions(agent, inner_nbs)
        agent = bounds_check(agent)
    return agent