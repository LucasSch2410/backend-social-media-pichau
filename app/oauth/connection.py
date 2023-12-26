import dropbox
import sys
from dropbox import DropboxOAuth2Flow
from dropbox.exceptions import AuthError

APP_KEY = "emm8mikk0bmdwbn"

def authenticate_dropbox():
    auth_flow = DropboxOAuth2Flow(APP_KEY, )

    authorize_url = auth_flow.start()
    print("1. Go to: " + authorize_url)
    print("2. Click \"Allow\" (you might have to log in first).")
    print("3. Copy the authorization code.")
    auth_code = input("Enter the authorization code here: ").strip()

    try:
        oauth_result = auth_flow.finish(auth_code)
    except AuthError as e:
        print('Erro ao se conectar ao Dropbox com o token de acesso: %s' % (e,))
        sys.exit(3)

    return dropbox.Dropbox(oauth2_access_token=oauth_result.access_token)

if __name__ == "__main__":
    # If this script is run directly, authenticate and print the current user's account info
    dbx = authenticate_dropbox()
    account_info = dbx.users_get_current_account()
    print("Successfully set up client for user:", account_info.display_name)
