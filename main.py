import json
import requests


class PackageComparator:
    def __init__(self):
        self.api_url = 'https://rdb.altlinux.org/api'

    def get_branch(self, branch):
        url = self.api_url + f'/export/branch_binary_packages/{branch}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Error fetching data: {e}')
            return None

    @staticmethod
    def compare_packages(p10_data, sisyphus_data):
        p10_packages = {tuple(package.values()) for package in p10_data['packages']}
        sisyphus_packages = {tuple(package.values()) for package in sisyphus_data['packages']}
        only_in_p10 = p10_packages - sisyphus_packages
        only_in_sisyphus = sisyphus_packages - p10_packages

        p10_packages = {(package['name'], package['arch']): package for package in p10_data['packages']}
        sisyphus_packages = {(package['name'], package['arch']): package for package in sisyphus_data['packages']}

        common_packages = p10_packages.keys() & sisyphus_packages.keys()
        newer_in_sisyphus = []
        for pkg_key in common_packages:
            sisyphus_pkg = sisyphus_packages[pkg_key]
            p10_pkg = p10_packages[pkg_key]
            if (sisyphus_pkg['epoch'], sisyphus_pkg['version'], sisyphus_pkg['release']) > (
                    p10_pkg['epoch'], p10_pkg['version'], p10_pkg['release']):
                newer_in_sisyphus.append(sisyphus_pkg)
        result = {
            'only_in_p10': {'length': len(only_in_p10),
                            'packages': [{'name': i[0], 'epoch': i[1], 'release': i[2], 'arch': i[3], 'disttag': i[4],
                                          'buildtime': i[5], 'source': i[6]} for i in list(only_in_p10)]
                            },
            'only_in_sisyphus': {'length': len(only_in_sisyphus),
                                 'packages': [
                                     {'name': i[0], 'epoch': i[1], 'release': i[2], 'arch': i[3], 'disttag': i[4],
                                      'buildtime': i[5], 'source': i[6]} for i in list(only_in_sisyphus)]
                                 },
            'newer_in_sisyphus': {'length': len(newer_in_sisyphus),
                                  'packages': newer_in_sisyphus
                                  }
        }
        return result


if __name__ == '__main__':
    comparator = PackageComparator()
    sisyphus_res = comparator.get_branch('sisyphus')
    p10_res = comparator.get_branch('p10')
    if sisyphus_res and p10_res:
        res = comparator.compare_packages(p10_res, sisyphus_res)
        print(res)
        with open('result.txt', 'w') as file:
            file.write(json.dumps(res))
