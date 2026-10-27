# personal-kb-builder

[English](README.md) · [示例](examples/demo-kb) · [SKILL.md](SKILL.md)

一个可移植的 Agent **Skill**：把你自己的资料整理成一个可追溯的 Markdown 个人知识库。

> 原始数据留在原地。知识库只保存结构、摘要、来源、证据与索引，不保存你的文件副本。

## 为什么需要它

个人资料会散落在各种文件夹里：论文、笔记、幻灯片、代码、导出文件、书签。聊天助手能总结单个文件，但会忘记结构、来源和不确定性。个人知识库可以解决这个问题——前提是建立时有纪律：

- **一页一个项目/主题**，两分钟能读完；
- **每条结论都有来源和定位**（页码、段落、幻灯片、函数）；
- **区分证据性质**：计划不是结果，代码存在不等于代码能跑；
- **记录空白**，而不是用猜测填满；
- **原始数据不复制、不执行**。

这个 Skill 把这套纪律固化成流程：访谈 → 只读盘点 → 框架提案 → 生成骨架 → 3–5 条种子闭环 → 校验与交接。

## 工作流

```text
访谈（结构化提问）
   -> 只读盘点
   -> 框架提案（研究 / 工作 / 学习 / 生活 / 混合）
   -> 生成骨架（不编造内容）
   -> 3–5 条种子：来源 -> 证据 -> 卡片 -> 校验
   -> 交接（维护说明 + 覆盖缺口）
```

AI 每轮最多问 3 个问题、总共最多 8 个；未确认范围前不扫描；不复制源文件；不执行资料中的脚本。

## 快速开始

### 用 Agent（DSH，或任何加载 `SKILL.md` 的 Agent）

```bash
# DSH：放到以下任一目录
cp -r personal-kb-builder ~/.dsh/skills/
# 或 <项目>/.dsh/skills/ 或 <项目>/.agents/skills/
```

然后让 Agent 帮你建库，或直接调用：

- DSH：`/personal-kb-builder`
- 模型侧：`skill` 工具，`name: personal-kb-builder`

安装细节与其他 Agent 见 [references/platforms.md](references/platforms.md)。

### 用命令行（不用 Agent）

```bash
python scripts/init_kb.py --target ~/my-kb --name "我的知识库" --variant research --lang zh \
  --data-roots "/Users/me/Documents,/Volumes/Archive"
python scripts/scan.py --root "/Users/me/Documents" --out ~/my-kb/catalog
python scripts/check.py --kb ~/my-kb
```

只依赖 Python 3.9+ 标准库：无网络、无安装、无数据库服务。

## 产物结构

```text
my-kb/
  README.md            # 人看的入口
  AI_CONTEXT.md        # AI 入口：目标、边界、检索路线
  AGENTS.md            # 可选：Agent 操作规则
  profile/profile.md   # 访谈结果
  projects/            # 一页一个项目
  topics/              # 主题/方法卡片
  timeline.md
  open-questions.md
  catalog/
    evidence.md        # E 编号：来源、定位、证据性质、限制
    sources.jsonl      # 只读文件清单
    coverage.json      # 扫描了什么、没扫描什么
  maintenance/update.md
```

## 证据模型

| 字段 | 含义 |
|---|---|
| `source` | 绝对路径，或压缩包路径 + 成员名 |
| `locator` | 页码 / 段落 / 幻灯片 / 函数 / 表名 |
| `kind` | `user-confirmed` · `document-reported` · `plan` · `code-structure` · `second-hand` · `path-only` |
| `limitation` | `unverified` · `single-run` · `parameters:…` · `stale` · `image-only` · `partial` · `second-hand` |

区别本身就是价值：汇报说“做过”不等于经过审计；文件存在不等于能运行；计划不等于结果。

## 脚本

| 脚本 | 作用 |
|---|---|
| `scripts/init_kb.py` | 从 `templates/kb/` 生成知识库骨架 |
| `scripts/scan.py` | 只读盘点 → `sources.jsonl` + `coverage.json` |
| `scripts/check.py` | 校验必需文件、E 编号、字段、链接、JSON，可选校验来源是否存在 |

每次编辑后运行：

```bash
python scripts/check.py --kb ~/my-kb --check-sources
```

## 仓库结构

```text
SKILL.md              # Skill 流程
references/           # 按需读取：框架变体、访谈、证据、平台
templates/kb/         # 可复制骨架
scripts/              # init / scan / check（标准库）
examples/             # 合成示例库 + 示例数据
tests/                # 单元测试
```

## 设计原则

1. **原始数据只读**：不复制、不移动、不解压、不执行。
2. **先跑通最小端到端**：骨架 → 3–5 条种子 → 校验，再增加深度。
3. **来源优先于文笔**：没有定位的结论就是猜测。
4. **先问再做**：结构化提问、推荐项在前，总共不超过 8 个问题。
5. **空白是一等公民**：`open-questions.md` 与 `coverage.json` 是特性，不是失败。
6. **默认可移植**：纯 Markdown、纯文件、标准库脚本。

## 开发

```bash
python -m unittest discover -s tests -v
python scripts/check.py --kb examples/demo-kb --check-sources
```

示例库是合成的。不要向本仓库提交个人数据、真实路径或源文件内容。

## 许可

MIT，见 [LICENSE](LICENSE)。
