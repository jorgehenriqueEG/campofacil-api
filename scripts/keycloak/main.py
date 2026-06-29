import psycopg2
import time
import requests

from env_vars import (
    db_name,
    db_user,
    db_password,
    db_host,
    db_port,
    keycloak_host,
    keycloak_realm,
    keycloak_admin_user,
    keycloak_admin_password,
)


def create_schema_for_keycloak():

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
    )
    conn.autocommit = True

    try:
        with conn.cursor() as cursor:
            # Create the keycloak schema if it doesn't exist
            cursor.execute("CREATE SCHEMA IF NOT EXISTS keycloak;")
            print("Schema 'keycloak' created successfully (if it did not exist).")
    except Exception as e:
        print(f"Error creating schema: {e}")
    finally:
        conn.close()


def wait_for_keycloak_to_start():

    keycloak_url = f"{keycloak_host}/realms/master"
    limit = 60  # Maximum number of attempts
    attempts = 0

    print("Waiting for Keycloak to start...")
    while attempts < limit:
        try:
            response = requests.get(keycloak_url)
            if response.status_code == 200:
                print("Keycloak is up and running!")
                return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(5)
        attempts += 1

    print("Keycloak did not start within the expected time frame.")
    raise Exception("Keycloak startup timed out.")


def get_master_token():
    url = f"{keycloak_host}/realms/master/protocol/openid-connect/token"
    data = {
        "grant_type": "password",
        "client_id": "admin-cli",
        "username": keycloak_admin_user,
        "password": keycloak_admin_password,
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()["access_token"]


def analyze_response(response):
    if response.status_code >= 200 and response.status_code < 300:
        print("Operation successful.")
    elif response.status_code == 409:
        print("Resource already exists.")
    else:
        print(f"Unexpected response: {response.status_code} - {response.text}")
        response.raise_for_status()


def create_realm(token):
    print("Creating realm...")
    url = f"{keycloak_host}/admin/realms"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "realm": keycloak_realm,
        "enabled": True,
    }
    response = requests.post(url, json=data, headers=headers)
    analyze_response(response)
    print("Realm created successfully.")


def create_client(token, client_id):
    print("Creating client...")
    url = f"{keycloak_host}/admin/realms/{keycloak_realm}/clients"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "clientId": client_id,
        "enabled": True,
        "publicClient": True,
        "directAccessGrantsEnabled": True,
        "redirectUris": ["*"],
    }
    response = requests.post(url, json=data, headers=headers)
    analyze_response(response)
    print("Client created successfully.")


def increase_token_lifespan(token):
    print("Increasing token lifespan...")
    url = f"{keycloak_host}/admin/realms/{keycloak_realm}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "accessTokenLifespan": 3600,  # 1 hour
        "accessTokenLifespanForImplicitFlow": 3600,
        "ssoSessionIdleTimeout": 3600,
        "ssoSessionMaxLifespan": 3600,
    }
    response = requests.put(url, json=data, headers=headers)
    analyze_response(response)
    print("Token lifespan increased successfully.")


def get_client_uuid(token, client_id_string):
    url = f"{keycloak_host}/admin/realms/{keycloak_realm}/clients"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, params={"clientId": client_id_string}, headers=headers)
    response.raise_for_status()
    clients = response.json()
    if not clients:
        raise Exception(f"Client '{client_id_string}' not found.")
    return clients[0]["id"]


def assign_manage_users_role(token, client_id_string):
    print(f"Assigning manage-users role to service account of '{client_id_string}'...")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    realm_mgmt_uuid = get_client_uuid(token, "realm-management")

    role_response = requests.get(
        f"{keycloak_host}/admin/realms/{keycloak_realm}/clients/{realm_mgmt_uuid}/roles/manage-users",
        headers=headers,
    )
    role_response.raise_for_status()

    print("manage-users role assigned successfully.")


def remove_attribute_last_name(token):
    print("Removing 'lastName' attribute from user representation...")
    url = f"{keycloak_host}/admin/realms/{keycloak_realm}/users/profile"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    profile = response.json()
    old_attributes = profile.get("attributes", [])
    new_attributes = [attr for attr in old_attributes if attr.get("name") != "lastName"]
    if len(old_attributes) == len(new_attributes):
        print("'lastName' attribute not found, no changes needed.")
        return
    profile["attributes"] = new_attributes
    update_response = requests.put(url, json=profile, headers=headers)
    analyze_response(update_response)
    print("'lastName' attribute removed successfully.")


def configure_keycloak():
    token = get_master_token()
    create_realm(token)
    client_id = "campofacil-app"
    create_client(token, client_id)
    increase_token_lifespan(token)
    assign_manage_users_role(token, client_id)
    remove_attribute_last_name(token)

    username = "admin"
    create_user(token, username)


def create_user(token, username):
    print("Creating admin user...")
    url = f"{keycloak_host}/admin/realms/{keycloak_realm}/users"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "username": username,
        "enabled": True,
        "email": f"{username}@example.com",
        "emailVerified": True,
        "firstName": f"{username.capitalize()}",
        "lastName": "Test",
        "credentials": [
            {
                "type": "password",
                "value": username,
                "temporary": False,
            }
        ],
    }
    response = requests.post(url, json=data, headers=headers)
    analyze_response(response)
    print("Admin user created successfully.")


def main():
    create_schema_for_keycloak()
    wait_for_keycloak_to_start()
    configure_keycloak()


if __name__ == "__main__":
    main()
