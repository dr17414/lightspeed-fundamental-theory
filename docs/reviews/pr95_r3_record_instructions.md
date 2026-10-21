# PR #95 r3：canonical追加與目前狀態同步的待套用patch

這是操作者明確授權的範圍：三本canonical帳只追加，STATUS／README只替換目前狀態。
由於自動核准審查拒絕重傳含歷史內容的整份接觸帳與STATUS，這份交付只保存差異，
不含歷史帳本文字，也不使用GitHub API重傳歷史檔案。

**本PR只加入patch檔及本說明，未實際修改canonical三帳或STATUS。只合併這兩個檔案，
不算完成canonical登記。** 必須把patch實際套用到另個紀錄分支、核對只追加／逐字／來源後，
將真正修改三帳及目前狀態的commit交獨立GO並合併main，才滿足#95契約的整合開始條件。

base head：`5d060cb1a34a97531cb98d6d35cfd9d0728b2714`
base tree：`d71d6bc19108e6fea9d705b47a334088e84d425e`
patch SHA-256：`90ddcb2619d29e050b6d717681c2f84b43be3e165620a2a27a0022e132ca2a05`

patch內容：EXP-0077／0078原補充段落、0079選題申報全文及0080 Claude本人原句逐字整合；
0081記GPT修訂／曝光範圍。補充檔和研究稿保留原樣，canonical為整合後權威。
原文「擬／未整合」字樣保留歷史來源，不視為第二套現行登記。
帳本只有新增行；STATUS與README只有目前狀態的替換。無K／state／pairing或策略選擇，
沒有新的數值／符號研究、RNG或科學執行，formal／T6／CI／tests均不變。

請先核對以下base blobs；若有變更，停止並核對下一個可用EXP-ID，不能盲套無context patch。

- `README.md`：`541d48248267021357b585988bb382a26f34281f`
- `docs/STATUS.md`：`41a5a533953f6be98a96326ebbcb0b41bc11e08a`
- `docs/STAGE5C_EXPLORATION_ACTIVATION.md`：`409e39c51c557637f5f3794b74cce3d3d8ef2cce`
- `docs/stage5c_development_log.md`：`67d58b699101d55c48f6eb1be6f94f201ec9768c`
- `docs/stage5c_exploration_exposure_log.md`：`b48d61802c83a60604d2562b030991e2baaff855`

在已核對上述base的隔離checkout中，可使用：

```bash
git apply --check --unidiff-zero docs/reviews/pr95_r3_canonical_append_only.patch
git apply --unidiff-zero docs/reviews/pr95_r3_canonical_append_only.patch
git diff --check
python verify_integrity.py
```

本說明沒有執行push／merge或取得canonical整合GO；套用後需核對三帳byte-prefix、
0077–0080逐字與ID唯一性，以及其餘檔案保全，再交exact-head增量複核。
在取得契約與整合兩者GO、必要CI、原樣合併與tree核對前，不開始構造。
