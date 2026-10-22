import httpx

def get_repo_count(username: str, base_url: str = "https://api.github.com",
                   timeout: float = 5) -> int | None:      # int | None = like int? in C#
    url = f"{base_url}/users/{username}"
    try:
        response = httpx.get(url, timeout=timeout)
        response.raise_for_status()                         # 4xx/5xx -> HTTPStatusError
    except httpx.HTTPStatusError as e:
        status = e.response.status_code
        if status == 404:
            print(f"  User '{username}' not found (404) - not retryable")
        else:
            print(f"  Server error {status} - {'retryable' if status >= 500 else 'not retryable'}")
        return None
    except httpx.TimeoutException:
        print(f"  Timed out after {timeout}s - retryable")
        return None
    except httpx.ConnectError:
        print(f"  Could not connect to {base_url} - check the URL or network")
        return None
    else:                                                   # only runs if no exception
        return response.json()["public_repos"]
    finally:
        print(f"  (finished call to {url})")                # always runs


print("1. Valid user:")
print(f"  Repos: {get_repo_count('lakshaysharma0703-droid')}")

print("\n2. User that doesn't exist:")
get_repo_count("this-user-should-not-exist-12345xyz")

print("\n3. Domain that doesn't exist:")
get_repo_count("anyone", base_url="https://this-domain-does-not-exist-xyz.com")

print("\n4. Slow server (3s delay, 1s timeout):")
get_repo_count("anyone", base_url="https://httpbin.org/delay/3", timeout=1)