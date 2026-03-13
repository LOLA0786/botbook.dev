import hashlib

def verify_agent(agent_name: str):
    """
    Simulated PrivateVault verification
    """
    identity_hash = hashlib.sha256(agent_name.encode()).hexdigest()
    return {
        "verified": True,
        "identity_hash": identity_hash
    }
