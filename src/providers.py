import re
from apk_index import direct_requirements
SUFFIXES = {
    'alpha': -4, 'beta': -3, 'pre': -2, 'rc': -1,
    'cvs': 1, 'svn': 2, 'git': 3, 'hg': 4, 'p': 5,
}
def split_requirement(token):
    name, op, version = re.split(r'([<>=~]+)', token, maxsplit=1) \
        if re.search(r'[<>=~]', token) else (token, '', '')
    return name, op, version
def version_key(version):
    main, _, revision = version.partition('-r')
    release, *suffixes = main.split('_')
    parts = re.findall(r'\d+|[a-z]+', release)
    tokens = tuple((0, int(x)) if x.isdecimal() else (1, x) for x in parts)
    ranks = []
    for suffix in suffixes:
        name, number = re.fullmatch(r'([a-z]+)(\d*)', suffix).groups()
        ranks.append((SUFFIXES.get(name, 0), int(number or 0)))
    return tokens, tuple(ranks or [(0, 0)]), int(revision or 0)
def matches(version, op, required):
    if not op:
        return True
    if not version:
        return False
    if '~' in op and version_key(version)[0][:len(version_key(required)[0])] \
            == version_key(required)[0]:
        return True
    actual_key, required_key = version_key(version), version_key(required)
    if actual_key < required_key:
        return '<' in op
    if actual_key > required_key:
        return '>' in op
    return '=' in op
def provider_index(packages):
    providers = {}
    for name, fields in packages.items():
        providers.setdefault(name, []).append((name, fields['V']))
        for token in fields.get('p', '').split():
            alias, _, version = split_requirement(token)
            providers.setdefault(alias, []).append((name, version))
    return providers
def resolve_requirement(providers, token):
    name, op, required = split_requirement(token)
    choices = providers.get(name, [])
    selected = [pkg for pkg, ver in choices if matches(ver, op, required)]
    return selected or [token]
def package_neighbors(packages):
    providers = provider_index(packages)
    def neighbors(name):
        if name not in packages:
            return []
        result = []
        for token in direct_requirements(packages, name):
            result.extend(resolve_requirement(providers, token))
        return result
    return neighbors
