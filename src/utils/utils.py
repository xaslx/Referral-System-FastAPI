import secrets




def generate_new_referral_code() -> str:
    return secrets.token_hex(5)