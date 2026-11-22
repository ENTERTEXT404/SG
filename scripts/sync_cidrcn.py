"""Build the Surge CIDRCN rule set from Sukka's IPv4 and IPv6 lists."""

import argparse
import ipaddress
import re
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.request import Request, urlopen


TARGET = Path(__file__).resolve().parents[1] / "RULE-SET" / "CIDRCN.list"
SOURCES = {
    4: "https://ruleset.skk.moe/List/ip/china_ip.conf",
    6: "https://ruleset.skk.moe/List/ip/china_ip_ipv6.conf",
}
RULE_TYPES = {4: "IP-CIDR", 6: "IP-CIDR6"}
MAX_BYTES = 2 * 1024 * 1024

# See RULE-SET/CIDRCN.md for the IANA, APNIC and routing evidence.
EXCLUSIONS = {
    4: (
        "0.0.0.0/8", "10.0.0.0/8", "100.64.0.0/10", "127.0.0.0/8",
        "169.254.0.0/16", "172.16.0.0/12", "192.0.2.0/24", "192.168.0.0/16",
        "198.18.0.0/15", "198.51.100.0/24", "203.0.113.0/24", "224.0.0.0/4",
        "240.0.0.0/4",
        "14.227.96.0/20", "223.122.0.0/16", "223.123.0.0/17",
        "223.123.128.0/18", "223.123.192.0/20",
    ),
    6: (
        "::/128", "::1/128", "::ffff:0:0/96", "100::/64", "2001:2::/48",
        "2001:db8::/32", "3fff::/20", "fc00::/7", "fe80::/10", "ff00::/8",
    ),
}
SIZE_HEADER = re.compile(r"^#\s*Size:\s*([0-9]+)\s*$")
COMMENT = re.compile(r"#|//|;")


def fetch(url):
    request = Request(url, headers={"User-Agent": "SG-CIDRCN-Sync/1"})
    with urlopen(request, timeout=30) as response:
        return response.read(MAX_BYTES + 1)


def parse_rules(data, version, require_size):
    if len(data) > MAX_BYTES:
        raise ValueError("source exceeds the size limit")

    sizes = []
    valid = []
    total = 0
    for raw in data.decode("utf-8-sig").splitlines():
        if match := SIZE_HEADER.fullmatch(raw.strip()):
            sizes.append(int(match[1]))
        line = COMMENT.split(raw, maxsplit=1)[0].strip()
        if not line:
            continue
        total += 1
        fields = [field.strip() for field in line.split(",")]
        if len(fields) == 2 and fields[0] == RULE_TYPES[version]:
            fields = fields[1:]
        if len(fields) != 1 or "%" in fields[0] or not re.search(r"/[0-9]+$", fields[0]):
            continue
        try:
            network = ipaddress.ip_network(fields[0])
        except ValueError:
            continue
        if network.version == version and network.prefixlen:
            valid.append(network)

    if (require_size or sizes) and sizes != [total]:
        raise ValueError(f"source size header disagrees with the {total} rule lines")
    if not valid:
        raise ValueError("source has no valid CIDRs for this address family")
    return valid, total - len(valid)


def subtract(network, excluded):
    if not network.overlaps(excluded):
        return (network,)
    if network.subnet_of(excluded):
        return ()
    return network.address_exclude(excluded)


def build_rules(data, version, require_size):
    valid, ignored = parse_rules(data, version, require_size)
    unique = set(valid)
    upstream = list(ipaddress.collapse_addresses(unique))
    networks = upstream
    for cidr in EXCLUSIONS[version]:
        excluded = ipaddress.ip_network(cidr)
        networks = [part for network in networks for part in subtract(network, excluded)]
    if not networks:
        raise ValueError("no CIDRs remain after exclusions")

    result = sorted(ipaddress.collapse_addresses(networks))
    excluded_addresses = sum(net.num_addresses for net in upstream) - sum(
        net.num_addresses for net in result
    )
    print(
        f"IPv{version}: {len(valid)} valid, {ignored} ignored, "
        f"{len(valid) - len(unique)} duplicates, {len(unique) - len(upstream)} "
        f"redundant or merged, {excluded_addresses} excluded addresses, "
        f"{len(result)} published CIDRs"
    )
    return "".join(f"{RULE_TYPES[version]},{network}\n" for network in result)


def write_if_changed(target, data):
    if target.exists() and target.read_bytes() == data:
        print(f"{target.name} is up to date.")
        return

    mode = target.stat().st_mode & 0o777 if target.exists() else 0o644
    with NamedTemporaryFile(dir=target.parent, delete=False) as temporary:
        path = Path(temporary.name)
        try:
            temporary.write(data)
            temporary.close()
            path.chmod(mode)
            path.replace(target)
        finally:
            path.unlink(missing_ok=True)
    print(f"Updated {target.name}.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sources", nargs=2, type=Path, metavar=("IPV4", "IPV6"),
        help="use local source snapshots in place of downloads",
    )
    parser.add_argument("--output", type=Path, default=TARGET, help="output rule-set path")
    args = parser.parse_args()

    try:
        rules = []
        for index, (version, url) in enumerate(SOURCES.items()):
            source = args.sources[index] if args.sources else url
            try:
                data = source.read_bytes() if args.sources else fetch(source)
                rules.append(build_rules(data, version, require_size=not args.sources))
            except (OSError, ValueError) as error:
                raise ValueError(f"IPv{version} {source}: {error}") from error
        write_if_changed(args.output, "".join(rules).encode("utf-8"))
    except (OSError, ValueError) as error:
        print(f"CIDRCN sync failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
