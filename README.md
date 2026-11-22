# Surge DIRECT 规则

在 Surge 的 `[Rule]` 中使用这一条规则，即可同时匹配手工域名和中国大陆 IPv4、IPv6 网段。

```ini
RULE-SET,https://raw.githubusercontent.com/ENTERTEXT404/SG/main/RULE-SET/DIRECT.list,DIRECT
```

如果原来分别引用了 `DIRECT.list` 和 `CIDRCN.list`，请用上面一条替换两条规则，并将它放在需要优先匹配的代理或拦截规则之后，通常是原 `CIDRCN.list` 的位置。中国大陆 CIDR 沿用原来的 DNS 行为。如果之前在 `CIDRCN.list` 的引用上用了 `no-resolve`，请在合并后的引用上保留该选项。 [Surge RULE-SET 文档](https://manual.nssurge.com/rules/ruleset.html)

## 更新规则

- [`DIRECT.manual.list`](RULE-SET/DIRECT.manual.list) 保存手工规则，支持 `DOMAIN`、`DOMAIN-SUFFIX`、`IP-CIDR` 和 `IP-CIDR6`。CIDR 可加 `no-resolve`。规则行省略策略。
- [`CIDRCN.list`](RULE-SET/CIDRCN.list) 是中国大陆 CIDR 的同步快照，也可继续在 Surge 中单独引用。
- [`DIRECT.list`](RULE-SET/DIRECT.list) 由上述两份文件生成。编辑手工源文件后，在仓库根目录运行下列命令，把手工源文件和生成结果放进同一个 PR。GitHub Actions 会离线检查产物是否与输入一致。

```sh
python3 .github/scripts/sync_cidrcn.py --cached
```

AT 每天北京时间 08:30 同步，08:45 再运行一次 CIDRCN 同步。同步保留现有网段排除和异常变动校验，按地址族去重、聚合、排序，在同一个提交中发布两个生成文件。手工触发 AT 时，`publish` 默认为关闭，可用于预览。 [IPv4 上游](https://ruleset.skk.moe/List/ip/china_ip.conf) · [IPv6 上游](https://ruleset.skk.moe/List/ip/china_ip_ipv6.conf)
