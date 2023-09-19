import numpy as np

def dezerofy(pool_array):
    """
    Change any 0s or 1s in pool array to a teeny tiny number or 1 - a teeny tiny number
    """
    for i, opinion in enumerate(pool_array):
        if opinion == np.float64(0):
            pool_array[i] = 2.2204460492503131e-16
        if opinion >= 1:
            pool_array[i] = 1 - 2.2204460492503131e-16
    return pool_array

def pool_opinions(agent, nbs):
    """
    Pool the opinions from nearby agents
    and update opinion
    """
    # Pool if agent has neighbours and none are granuloma
    if len(nbs) > 0 and "Granuloma" not in nbs.type:
        nbs_ops_array = np.array(nbs.opinion)
        pool_array = dezerofy(np.append(nbs_ops_array, agent.opinion))
        # Check that no opinions have been rounded to 0 or 1
        h1 = (np.prod(pool_array))**agent.p.w
        h2 = (np.prod(1-pool_array))**agent.p.w
        # Update opinion using SProdOp
        agent.opinion = h1/(h1+h2)
    return agent

def evidentially_update(agent):
    """
    Update opinions from evidence at an epsilon chance 
    """
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
    if agent.model.random.random() <= agent.p.pooling_epsilon:
        inner_nbs = agent.neighbors(agent, distance=agent.p.pooling_radius)
        agent = pool_opinions(agent, inner_nbs)
    return agent