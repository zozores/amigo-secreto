import random

def perform_draw(participants):
    """
    Assigns a match to each participant such that:
    1. No one matches themselves.
    2. Everyone is matched exactly once.
    3. No sub-loops if possible (though simple derangement is enough for basic secret santa).
    
    This implementation uses a simple shuffle and check approach.
    """
    if len(participants) < 2:
        raise ValueError("Need at least 2 participants")

    ids = [p.id for p in participants]
    
    # Try to find a valid permutation
    # For small N, this is very fast.
    # For a robust solution, we can just rotate the list.
    # A simple rotation guarantees no fixed points (p[i] != i)
    
    shuffled = ids[:]
    random.shuffle(shuffled)
    
    # Check for fixed points
    # If any p[i] == i, just rotate the list until no fixed points?
    # Actually, a simple rotation of a shuffled list isn't enough if the shuffle happened to align with original indices.
    # But wait, we are assigning matches.
    # Let's just do a derangement shuffle.
    
    # Simple approach:
    # 1. Shuffle the list of receivers.
    # 2. If any sender[i] == receiver[i], swap receiver[i] with receiver[(i+1)%N]
    # This is not perfect randomness but good enough for simple secret santa.
    # Better approach: Keep shuffling until valid. For N < 100 this is instant.
    
    while True:
        random.shuffle(shuffled)
        if all(p.id != s_id for p, s_id in zip(participants, shuffled)):
            break
            
    # Assign matches
    for p, match_id in zip(participants, shuffled):
        p.match_id = match_id
