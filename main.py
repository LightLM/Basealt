import requests


class Parser:
    def __init__(self):
        self.api_url = 'https://rdb.altlinux.org/api'

    def get_branch(self, branch):
        url = self.api_url + f'/export/branch_binary_packages/{branch}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None


if __name__ == '__main__':
    api = Parser()
    sisyphus_packages = api.get_branch('sisyphus')
    p10_packages = api.get_branch('p10')
    print(p10_packages)
