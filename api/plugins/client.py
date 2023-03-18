import httpx


class SlackClient:
    BASE_URL = "https://slack.com/api"

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_access_token(self, code: str):
        res = httpx.post(
            f"{self.BASE_URL}/oauth.v2.access",
            files={"code": (None, code)},
            auth=httpx.BasicAuth(self.client_id, self.client_secret),
        )
        return res.json()

    def get_emojis(self, token: str):
        headers = { "Content-Type": "application/json; charset=utf-8", "Authorization": f"Bearer {token}"}
        res = httpx.post(
            f"{self.BASE_URL}/emoji.list", params={ "include_categories": True }, headers=headers
        )
        return res.json()


    def set_status(self, token: str, payload: dict):
        headers = { "Content-Type": "application/json; charset=utf-8", "Authorization": f"Bearer {token}"}
        payload = { "profile": payload }

        res = httpx.post(
            f"{self.BASE_URL}/users.profile.set", json=payload, headers=headers
        )
        return res.json()
