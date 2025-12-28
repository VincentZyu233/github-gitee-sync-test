# GitHub 到 Gitee 自动同步教程

## 📋 概述

本教程介绍如何使用 GitHub Actions 实现代码从 GitHub 自动同步到 Gitee 的功能。

## 🎯 方案一：使用 gitee-mirror-action（推荐）

适用于需要同步**整个用户或组织所有仓库**的情况。

### 1. 准备工作

#### 1.1 生成 Gitee Token

1. 访问 [Gitee Token 配置页](https://gitee.com/profile/personal_access_tokens)
2. 点击"生成新令牌"
3. 设置 token 名称（如：github-mirror）
4. 选择权限：
   - ✅ projects: 授权操作项目
   - ✅ groups: 授权操作组织
   - ✅ pull_requests: 授权操作 PR
5. 点击"提交"
6. **立即复制生成的 Token**（只显示一次，务必保存）

#### 1.2 生成 SSH 密钥

打开终端（Git Bash、PowerShell 或 CMD），执行：

```bash
ssh-keygen -t rsa -C "你的邮箱地址"
```

提示：
- 当询问保存路径时，直接回车使用默认路径
- 当询问密码时，可以留空直接回车

生成后会得到两个文件：
- `id_rsa` - 私钥（保密）
- `id_rsa.pub` - 公钥

#### 1.3 在 Gitee 添加 SSH 公钥

1. 访问 [Gitee SSH 公钥配置页](https://gitee.com/profile/sshkeys)
2. 点击"添加公钥"
3. 将 `id_rsa.pub` 文件的内容复制进去
4. 点击"确定"

### 2. 配置 GitHub 仓库

#### 2.1 创建同步仓库

在 GitHub 创建一个新仓库（或使用现有仓库），专门用于同步配置。

#### 2.2 添加 Secrets

1. 打开 GitHub 仓库页面
2. 点击 `Settings` → `Secrets and variables` → `Actions`
3. 点击 `New repository secret`

添加以下两个密钥：

**Secret 1: GITEE_TOKEN**
- Name: `GITEE_TOKEN`
- Value: 第1.1步生成的 Gitee Token

**Secret 2: GITEE_PRIVATE_KEY**
- Name: `GITEE_PRIVATE_KEY`
- Value: `id_rsa` 文件的全部内容（包括 `-----BEGIN RSA PRIVATE KEY-----` 和 `-----END RSA PRIVATE KEY-----`）

#### 2.3 创建 GitHub Actions Workflow

在仓库中创建 `.github/workflows/sync-to-gitee.yml` 文件：

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
  mirror:
    runs-on: ubuntu-latest
    steps:
      - name: Mirror GitHub repos to Gitee
        uses: Yikun/gitee-mirror-action@v0.10
        with:
          # 源：GitHub用户名
          src: github/your-github-username
          
          # 目标：Gitee用户名
          dst: gitee/your-gitee-username
          
          # Gitee SSH私钥
          dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
          
          # Gitee Token
          dst_token: ${{ secrets.GITEE_TOKEN }}
          
          # 可选：账户类型（用户或组织）
          # account_type: org
          
          # 可选：黑名单（不同步的仓库）
          # black_list: "repo1,repo2"
          
          # 可选：白名单（只同步这些仓库）
          # white_list: "repo1,repo2"
          
          # 可选：静态列表（用于同步指定仓库）
          # static_list: "repo1,repo2"
          
          # 可选：是否强制同步
          # force_update: true
```

### 3. 高级配置示例

#### 3.1 同步指定仓库

```yaml
- name: Mirror GitHub repos to Gitee
  uses: Yikun/gitee-mirror-action@v0.10
  with:
    src: github/your-github-username
    dst: gitee/your-gitee-username
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    dst_token: ${{ secrets.GITEE_TOKEN }}
    # 只同步这三个仓库
    white_list: "repo1,repo2,repo3"
```

#### 3.2 同步组织仓库

```yaml
- name: Mirror GitHub repos to Gitee
  uses: Yikun/gitee-mirror-action@v0.10
  with:
    src: github/your-org-name
    dst: gitee/your-gitee-username
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    dst_token: ${{ secrets.GITEE_TOKEN }}
    # 指定是组织
    account_type: org
```

#### 3.3 排除某些仓库

```yaml
- name: Mirror GitHub repos to Gitee
  uses: Yikun/gitee-mirror-action@v0.10
  with:
    src: github/your-github-username
    dst: gitee/your-gitee-username
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    dst_token: ${{ secrets.GITEE_TOKEN }}
    # 不同步这些仓库
    black_list: "test-repo,demo-repo"
```

### 4. 执行同步

#### 4.1 自动触发

- **Push 触发**：每次推送到 main/master 分支时自动同步
- **定时触发**：按 cron 表达式定时执行（示例为每天9点）
- **Workflow 触发**：在 GitHub Actions 页面手动点击运行

#### 4.2 手动触发

1. 访问 GitHub 仓库的 `Actions` 标签页
2. 选择 `Sync to Gitee` workflow
3. 点击 `Run workflow` 按钮
4. 选择分支，点击绿色 `Run workflow` 按钮

### 5. 查看同步结果

1. 访问 GitHub 仓库的 `Actions` 标签页
2. 查看最新的 workflow 运行记录
3. 点击进入查看详细日志
4. 访问 Gitee 确认仓库是否同步成功

---

## 🎯 方案二：单仓库同步（使用 Git 命令）

适用于只需要同步**单个仓库**的情况。

### 1. 添加 Gitee 远程仓库

在本地仓库执行：

```bash
# 添加 Gitee 远程仓库
git remote add gitee https://gitee.com/your-username/your-repo.git

# 或者使用 SSH（推荐）
git remote add gitee git@gitee.com:your-username/your-repo.git
```

### 2. 创建同步 Workflow

创建 `.github/workflows/sync-single-repo.yml`：

```yaml
name: Sync Single Repo to Gitee

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Sync to Gitee
        run: |
          # 配置 Git
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          
          # 添加 Gitee 远程仓库
          git remote add gitee https://gitee.com/your-username/your-repo.git
          
          # 推送到 Gitee
          git push gitee main:master --force
```

### 3. 使用 SSH 推送（推荐）

如果需要使用 SSH，需要在 GitHub Secrets 中添加：

**Secret: GITEE_SSH_KEY**
- 添加你的 `id_rsa` 私钥内容

然后修改 workflow：

```yaml
- name: Setup SSH
  run: |
    mkdir -p ~/.ssh
    echo "${{ secrets.GITEE_SSH_KEY }}" > ~/.ssh/id_rsa
    chmod 600 ~/.ssh/id_rsa
    ssh-keyscan gitee.com >> ~/.ssh/known_hosts

- name: Sync to Gitee
  run: |
    git remote add gitee git@gitee.com:your-username/your-repo.git
    git push gitee main:master --force
```

---

## 🎯 方案三：使用自定义脚本（类似 koishi-registry-aggregator）

适用于需要**复杂处理逻辑**的情况（如数据处理后再同步）。

### 示例：数据同步 + 部署

```yaml
name: Data Sync and Deploy

on:
  schedule:
    - cron: '*/5 * * * *'  # 每5分钟
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: 处理数据
        run: |
          # 你的数据处理脚本
          python process_data.py
          # 或
          go run main.go

      - name: 部署到 Gitee
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          
          git add .
          git commit -m "Update data [skip ci]"
          
          # 推送到 Gitee
          git push https://x-access-token:${{ secrets.GITEE_TOKEN }}@gitee.com/your-username/your-repo.git main --force
```

---

## 🔧 常见问题

### Q1: 同步失败怎么办？

**问题**：Actions 报错 "Permission denied"

**解决**：
1. 检查 Gitee Token 权限是否正确
2. 检查 SSH 密钥是否正确配置
3. 确认仓库名称拼写正确

### Q2: 如何只同步特定分支？

修改 workflow 中的 push 触发条件：

```yaml
on:
  push:
    branches: [ main ]  # 只同步 main 分支
```

### Q3: 同步速度慢怎么办？

**优化建议**：
1. 使用 SSH 方式推送（比 HTTPS 快）
2. 减少同步频率
3. 使用白名单，只同步必要的仓库

### Q4: 如何避免循环触发？

在 commit message 中添加 `[skip ci]`：

```bash
git commit -m "Sync to Gitee [skip ci]"
```

### Q5: Token 过期怎么办？

Token 有效期通常为 30 天，到期后需要：
1. 重新生成 Gitee Token
2. 更新 GitHub Secrets 中的 GITEE_TOKEN

---

## 📝 最佳实践

1. **安全性**
   - 不要将 Token 和私钥提交到代码仓库
   - 定期更新 Token
   - 使用最小权限原则

2. **性能优化**
   - 合理设置同步频率
   - 使用白名单减少同步范围
   - 监控 Actions 运行时间

3. **错误处理**
   - 添加通知机制（如邮件、钉钉、企业微信）
   - 记录详细日志
   - 设置重试机制

4. **测试**
   - 先用测试仓库验证配置
   - 检查同步后的代码完整性
   - 验证分支和标签是否正确

---

## 🎉 完成！

现在你的 GitHub 仓库会自动同步到 Gitee 了！

如有问题，可以查看 GitHub Actions 的运行日志来排查。
