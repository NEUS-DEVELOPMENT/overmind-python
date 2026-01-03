import random

def adjust_risk_with_context(score: int, metadata: dict) -> int:
    """
    מעשיר risk_score לפי מידע קריטי מהקשר ההתרעה
    """
    final_score = score
    if not metadata:
        return final_score

    if metadata.get("source_reputation") == "BAD_IP":
        final_score += 2
    if metadata.get("time_of_day") == "OFF_HOURS":
        final_score += 1
    if metadata.get("target_asset") == "CROWN_JEWELS":
        final_score += 3

    return min(final_score, 10)

def generate_ephemeral_logic(agent_type: str, context: dict = None) -> str:
    """
    יוצר פקודת פעולה פולימורפית בהתאם לסוג הסוכן והקשר האירוע
    """
    strikes = [
        "ACTIVATE_STRIKE_MODE",
        "ENGAGE_COUNTERMEASURE",
        "DEPLOY_DEFENSE_FORCE",
        "PROVOKE_DEFENSE_SEQUENCE",
    ]
    defenses = [
        "INITIATE_DEFENSE_PROTOCOL",
        "ACTIVATE_SHIELD",
        "ISOLATE_THREAT",
        "DEPLOY_BARRIER"
    ]
    ghosts = [
        "ENTER_GHOST_MODE",
        "DISENGAGE_AND_FADE",
        "ENGAGE_CAMOUFLAGE_PROTOCOL",
        "SHADOW_EXIT"
    ]
    noise = "".join(random.choices("ABCDEFGHJKLMNOPQRSTUVWXYZ0123456789", k=8))

    if agent_type == "Strike":
        cmd = random.choice(strikes)
    elif agent_type == "Defense":
        cmd = random.choice(defenses)
    else:
        cmd = random.choice(ghosts)

    event_id = context.get("event_id") if context and "event_id" in context else str(random.randint(1000,9999))
    return f"ID[{event_id}] NOISE[{noise}] | EXEC({cmd})"

def analyze(threat_report):
    """
    תהליך מוכלל ומודרני לניתוח התרעה והפקת החלטה ופקודה דינמית
    """
    score = adjust_risk_with_context(
        threat_report['risk_score'],
        threat_report.get('metadata')
    )
    if score >= 8:
        agent_type = "Strike"
    elif score >= 5:
        agent_type = "Defense"
    else:
        agent_type = "Ghost"

    logic = generate_ephemeral_logic(agent_type, context=threat_report.get('metadata', {}))

    return {
        "agent_type": agent_type,
        "action_logic": logic,
    }
