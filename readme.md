# GitHub 到 Gitee 自动同步测试

本仓库用于测试 GitHub Actions 自动同步到 Gitee 的功能。

## 📦 仓库信息

- **GitHub 仓库**: https://github.com/VincentZyu233/github-gitee-sync-test
- **Gitee 仓库**: https://gitee.com/vincent-zyu/github-gitee-sync-test

## ⚙️ 工作原理

使用 GitHub Actions 实现 GitHub 代码自动推送到 Gitee，支持：

- ✅ **推送触发**: 每次 push 到 main/master 分支时自动同步
- ✅ **手动触发**: 可在 GitHub Actions 页面手动运行
- ✅ **定时同步**: 每天北京时间 9:00 自动同步

## 🚀 GitHub Actions 配置

### 前置要求

在配置 GitHub Actions 之前，需要先完成以下步骤：

1. **生成 SSH 密钥**
   ```bash
   ssh-keygen -t rsa -C "你的邮箱地址"
   ```

2. **在 Gitee 添加 SSH 公钥**
   - 访问 https://gitee.com/profile/sshkeys
   - 将生成的 `id_rsa.pub` 内容添加进去

3. **在 GitHub 添加 Secret**
   - 访问仓库的 Settings → Secrets and variables → Actions
   - 添加 Secret：
     - Name: `GITEE_PRIVATE_KEY`
     - Value: `id_rsa` 私钥文件的完整内容

### Workflow 配置

Workflow 文件位于：`.github/workflows/sync-to-gitee.yml`

```yaml
name: Sync to Gitee

on:
  # 推送时触发
  push:
    branches: [ main, master ]
  
  # 手动触发
  workflow_dispatch:
  
  # 定时触发（每天北京时间9点）
  schedule:
    - cron: '0 1 * * *'

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: 配置 Git
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
      
      - name: 设置 SSH 密钥
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.GITEE_PRIVATE_KEY }}" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
          ssh-keyscan gitee.com >> ~/.ssh/known_hosts
      
      - name: 添加 Gitee 远程仓库
        run: |
          git remote add gitee git@gitee.com:vincent-zyu/github-gitee-sync-test.git
      
      - name: 推送到 Gitee
        run: |
          git push gitee main:master --force
```

## 📝 使用说明

### 1. 自动同步

直接 push 到 GitHub 仓库的 main 或 master 分支，Actions 会自动触发同步：

```bash
git add .
git commit -m "Update files"
git push origin main
```

### 2. 手动同步

1. 访问 GitHub 仓库的 **Actions** 标签页
2. 选择 **Sync to Gitee** workflow
3. 点击 **Run workflow** 按钮
4. 选择分支，点击绿色按钮执行

### 3. 查看同步状态

- 访问 GitHub 仓库的 **Actions** 标签页查看运行记录
- 点击运行记录查看详细日志
- 访问 Gitee 仓库确认同步是否成功

## 🔧 配置说明

### 修改同步目标仓库

如果需要同步到其他 Gitee 仓库，修改 `.github/workflows/sync-to-gitee.yml` 中的以下内容：

```yaml
# 修改这里的目标仓库地址（使用 SSH 格式）
git remote add gitee git@gitee.com:你的用户名/你的仓库名.git
```

### 修改同步频率

修改 `schedule` 部分的 cron 表达式：

```yaml
schedule:
  # 格式：分 时 日 月 周
  # 每天 9 点运行
  - cron: '0 1 * * *'
  
  # 每小时运行
  - cron: '0 * * * *'
  
  # 每 5 分钟运行
  - cron: '*/5 * * * *'
```

### 修改触发分支

修改 `push` 部分的分支列表：

```yaml
push:
  branches: [ main, master, dev ]
```

## 💡 注意事项

1. **使用 SSH**: 本配置使用 SSH 方式推送，需要提前配置 SSH 密钥
2. **分支映射**: 当前配置将 GitHub 的 `main` 分支推送到 Gitee 的 `master` 分支
3. **强制推送**: 使用 `--force` 参数强制覆盖 Gitee 仓库
4. **权限要求**: GitHub Actions 需要有仓库的写权限（默认已开启）
5. **密钥安全**: `GITEE_PRIVATE_KEY` 包含敏感信息，切勿泄露

## 📚 相关资源

- [GitHub Actions 官方文档](https://docs.github.com/cn/actions)
- [GitHub 到 Gitee 自动同步教程](./github到gitee自动同步教程.md)

---

**测试时间**: 2025年12月29日
