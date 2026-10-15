# Kane CLI 原图修复后的可重放测试资产

本目录保存已经实际通过的 Budget UI 测试定义、执行缓存和 Codex 本地计数修正。CLI 版本 0.8.23；这是同一演示账号的资产备份，身份 ID 指向既有 Test Manager 项目。仓库不含登录凭据、原始 session 日志、证据包、截图视频或 `.context`。

## 取回并执行

在已安装并登录 Kane CLI 的机器，从仓库根目录执行：

```sh
python3 qa/assurance/hydrate.py
node qa/assurance/check_count_oracle.mjs qa/assurance/patched-count-oracle.json
kane-cli testrun run .testmuai/tests/budget-category-shows-exactly-the-two-eligible-preview-2_test.md --parallel 1 --dry-run --agent
kane-cli testrun run .testmuai/tests/budget-category-shows-exactly-the-two-eligible-preview-2_test.md --parallel 1 --headless --no-adaptive-heal --on-failure fail-fast --name assurance-git-replay --agent --stream-members
```

hydrate 先核对 SHA256，只在文件缺失或内容完全相同时继续；不会覆盖不同的本地资产。上面的显式路径选择不依赖 `.context`。需要 `--from-context t-2` 和覆盖回写时，请先通过官方 `context sync` 恢复受控 Wiki 中的同一图谱；不要把图谱手工合并到 Git。

## 本次已通过什么

最终真实执行 `cf4c12a4-51d4-4649-b9cb-9c82910b84f7`：1/1 用例、3/3 根步骤 replay 通过，authored=0、adaptive-heal 关闭、exit 0、upload=ok；关联图谱 5/5 AC proven，stale=0。**成员 commit=false / readonly_fallback，本轮结果上传成功，但不是平台测试版本发布成功。**

原始前两步及 5 个业务 AC 保留，新增第 3 步只独立验证“没有额外卡片”。官方生成先使用固定两个元素，后使用摘要数字，均不能证明动态卡片数量。**Codex 修正了一个生成读取动作；这不是厂商 AI 原生一次生成成功。** 动态 DOM 表达式如下，expected=2 未改：

```js
Array.from(el(0).querySelectorAll('.cursor-pointer.group'))
  .filter(e => e.getClientRects().length > 0).length
```

`patch_count_oracle.py` 是当时的严格补丁脚本，仅接受已审查的“摘要数字”旧资产；本目录缓存已经应用，**不要再对它重复打补丁**。`check_count_oracle.mjs` 验证真实表达式在 0/1/3 张可见卡片时拒绝，2 张时通过，额外隐藏卡片不计数；它是离线算子检查，不能替代浏览器。

资产内的 execution.json、meta.json 与 actions.ndjson 是 CLI 实际重放所需生成结构，保留原值和 SHA256；状态字段只是原运行的元数据，不代表取回后的新运行已经通过。运行记录请看 CLI 新返回的 execution ID。原图备份、完整过程视频及操作截图在授权 Wiki 2792165237。
