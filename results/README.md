# Stage 5C execution ledgers

The repository owner explicitly authorized public disclosure of the complete plus-arm ledger on 2026-09-02, after PR #14 recorded the incident summary.

`stage5c_6a_s_plus_protocol_invalid.ndjson.gz.part00` 至 `part17` 是
`docs/STAGE5C_6A_S_EXECUTION_INCIDENT.md` 所記 plus-arm ledger 的固定 49,152-byte 分片；
最後一片較短。分片只為 GitHub API 傳輸與封存，不能各自解壓縮。

在本目錄重組：

```bash
cat stage5c_6a_s_plus_protocol_invalid.ndjson.gz.part?? \
  > stage5c_6a_s_plus_protocol_invalid.ndjson.gz
```

重組 gzip 的 SHA-256 必須為：

```text
520c42f8c523031763dde10f1086c1a6c43f855950afc1fae5097933729ccd63
```

解壓後 NDJSON 的 SHA-256 必須為：

```text
32338ee83000c198747c1bd9cd5c9e98a5d054abde25e804be83533fe7de81e1
```

此 ledger 的正式語意是 `PROTOCOL-INVALID` incident evidence，不得用來事後重判 6a-S、
形成跨 target numerical contrast，或作候選設計輸入。
