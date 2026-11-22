# CIDRCN

`CIDRCN.list` 由 [Sukka's Ruleset](https://github.com/SukkaW/Surge) 的
[中国大陆 IPv4](https://ruleset.skk.moe/List/ip/china_ip.conf) 和
[中国大陆 IPv6](https://ruleset.skk.moe/List/ip/china_ip_ipv6.conf) 规则改编，
按 [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/) 发布。
改动包括筛选 CIDR、去重、聚合、排除有依据的网段，以及按 IPv4、IPv6 和网络地址排序。

## 同步

GitHub Actions 每天北京时间 08:30（UTC 00:30）同步。也可以在 Actions 的
**CIDRCN** 页面选择 **Run workflow**，对 `main` 手动运行。清单内容有差异时才提交。
脚本检查在线源的规则数量声明，并在两种地址族都生成成功后写入。

从仓库根目录运行以下命令。第二条命令使用事先保存的上游文件复现生成结果。

```sh
python3 scripts/sync_cidrcn.py
python3 scripts/sync_cidrcn.py --sources china_ip.conf china_ip_ipv6.conf --output /tmp/CIDRCN.list
```

## 排除依据

特殊用途排除项来自 IANA 的 [IPv4](https://www.iana.org/assignments/iana-ipv4-special-registry)、
[IPv6](https://www.iana.org/assignments/iana-ipv6-special-registry) 地址登记表及
[IPv4](https://www.iana.org/assignments/multicast-addresses/)、
[IPv6](https://www.iana.org/assignments/ipv6-multicast-addresses/) 组播登记表。
地理排除项于 2026-11-22 按 APNIC 登记与 RIPE RIS 路由交叉核验。

| 排除网段 | 登记和路由依据 |
| --- | --- |
| `14.227.96.0/20` | 越南 VNPT，AS45899。[APNIC](https://rdap.apnic.net/ip/14.227.96.0) · [RIPE RIS](https://stat.ripe.net/ui2013/14.227.96.0/20) |
| `223.122.0.0/16` | 中国移动香港，区间内更具体路由来自 AS9231、AS137872。[APNIC 上半段](https://rdap.apnic.net/ip/223.122.0.0) · [APNIC 下半段](https://rdap.apnic.net/ip/223.122.128.0) · [RIPE RIS](https://stat.ripe.net/ui2013/223.122.0.0/16) |
| `223.123.0.0/17` | 巴基斯坦 CMPak（Zong），AS59257、AS138423。[APNIC 上半段](https://rdap.apnic.net/ip/223.123.0.0) · [APNIC 下半段](https://rdap.apnic.net/ip/223.123.64.0) · [RIPE RIS](https://stat.ripe.net/ui2013/223.123.0.0/17) |
| `223.123.128.0/18`、`223.123.192.0/20` | 中国移动香港，区间内更具体路由分别来自 AS137872、AS9231。[APNIC /18](https://rdap.apnic.net/ip/223.123.128.0) · [APNIC /20](https://rdap.apnic.net/ip/223.123.192.0) · [RIPE RIS /18](https://stat.ripe.net/ui2013/223.123.128.0/18) · [RIPE RIS /20](https://stat.ripe.net/ui2013/223.123.192.0/20) |

脚本按上表逐段扣除地址。上游的 `223.122.0.0/15` 中，APNIC 登记为中国大陆
CMNET 的 `223.123.208.0/20` 和 `223.123.224.0/19` 仍在清单中。
