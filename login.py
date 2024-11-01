
import credentials as cd
from fyers_apiv3 import fyersModel

def generate_access_token(client_id,secret_key,redirect_uri):
    response_type = "code"
    # Create a session model with the provided credentials
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type=response_type
    )
    # Generate the auth code using the session model
    response = session.generate_authcode()
    # Print the auth code received in the response
    print(response)
    response_type = "code"
    grant_type = "authorization_code"
    # The authorization code received from Fyers after the user grants access
    print("Paste Opened Url Here : \n")
    url = str(input())
    auth = url.split('auth_code=')
    auth_code = auth[1].split('&state')[0]
    # Create a session object to handle the Fyers API authentication and token generation
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type=response_type,
        grant_type=grant_type
    )
    # Set the authorization code in the session object
    session.set_token(auth_code)
    # Generate the access token using the authorization code
    res = session.generate_token()
    # Print the response, which should contain the access token and other details
    access_token = res['access_token']
    print(access_token)

    with open('access.txt', 'w') as k:
        k.write(access_token)


if __name__ == '__main__':
    generate_access_token(cd.client_id, cd.secret_key, cd.redirect_uri)
