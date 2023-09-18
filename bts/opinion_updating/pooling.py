import numpy as np

def pool_opinions(agent, nbs):
    """
    Pool the opinions from nearby agents
    and update opinion
    """
    # Pool if agent has neighbours
    if len(nbs) > 0:
        nbs_ops_array = np.array(nbs.opinion)
        # Add back in own opinion
        pool_array = np.append(nbs_ops_array, agent.opinion)
        h1 = (np.prod(pool_array))**agent.p.w
        h2 = (np.prod(1-pool_array))**agent.p.w
        # Update opinion using SProdOp
        agent.opinion = h1/(h1+h2)
    return agent

def evidentially_update(agent):
    """
    Update opinions from evidence at an epsilon chance 
    """
    # Upate using Chanelle's equation
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