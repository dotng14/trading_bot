def login_robinhood():
    try:
        login_data = r.login(config.USERNAME, config.PASSWORD, pickle_name="pickle_name")
        print("Logged in successfully.")
        return login_data
    except Exception as e:
        # Handle MFA challenge
        if "challenge" in str(e):
            challenge_id = r.get_current_challenge_id()
            print("MFA required.")
            mfa_code = input("Enter the verification code sent to your device: ")
            # Complete the challenge with the provided code
            r.respond_to_challenge(challenge_id, mfa_code)
            print("Logged in successfully.")
            return r.login(config.USERNAME, config.PASSWORD)
        else:
            print(f"Login failed: {e}")