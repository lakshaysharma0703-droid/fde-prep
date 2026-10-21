import httpx

username = "lakshaysharma0703-droid"
url = f"https://api.github.com/users/{username}"

response = httpx.get(url,timeout=10)
response.raise_for_status()

data = response.json()

print(f"Login: {data["login"]}")
print(f"Name: {data.get('name')}")
print(f"Public repos: {data['public_repos']}")
print(f"Account created: {data['created_at']}")