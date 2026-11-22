# Rule data sources

| Published data | Upstream | License |
| --- | --- | --- |
| `DIRECT.list` domain rules | [Loyalsoldier/surge-rules](https://github.com/Loyalsoldier/surge-rules), release files `direct.txt`, `private.txt`, `apple.txt`, and `icloud.txt` | [GNU GPL v3](GPL-3.0.txt) |
| `DIRECT.list` IPv4 and IPv6 CIDR rules | [Sukka's Ruleset](https://github.com/SukkaW/Surge), [IPv4 source](https://ruleset.skk.moe/List/ip/china_ip.conf) and [IPv6 source](https://ruleset.skk.moe/List/ip/china_ip_ipv6.conf) | [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/) |
| `REJECT.list` rules | [AWAvenue Ads Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule), [Surge RULE-SET source](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Surge-RULE-SET.list) | [GNU GPL v3](GPL-3.0.txt) |

SG publishes the domain and CIDR parts of `DIRECT.list` together as separate types of rules. Each part is derived independently and retains its source attribution and license. SG filters, deduplicates, and sorts the rules, applies the exclusions documented in [the workflow](../../.github/workflows/AT.yml), and adds `no-resolve` to REJECT IP rules.
