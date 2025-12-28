# GitLab 同步配置说明

## 📋 概述

本文档说明如何将 GitHub 仓库同时同步到 Gitee 和 GitLab。

## 🔧 配置步骤

### 1. 复用已有的 SSH 密钥

如果你已经按照之前的教程生成了 SSH 密钥，可以直接复用！同一个私钥可以同时用于 Gitee 和 GitLab。

### 2. 在 GitLab 添加 SSH 公钥

1. 访问 [GitLab SSH Keys 页面](https://gitlab.com/-/profile/keys)
2. 点击 "Add new key"
3. 将你之前生成的 `id_rsa.pub` 文件的内容复制进去
4. 设置 Title（如：GitHub Actions Sync）
5. 点击 "Add key"

**注意**：
- 如果之前已经在 Gitee 添加过这个公钥，GitLab 会提示 "Fingerprint already exists"，这是正常的，同一个公钥可以用在多个平台
- 只需要点击 "Add key" 即可，不需要重新生成密钥

### 3. 在 GitHub 更新 Secret

之前可能已经添加了 `GITEE_PRIVATE_KEY`，现在需要统一使用 `SSH_PRIVATE_KEY`：

1. 访问 GitHub 仓库的 Settings → Secrets and variables → Actions
2. 检查是否有 `GITEE_PRIVATE_KEY`，如果有，先删除它
3. 添加新的 Secret：
   - **Name**: `SSH_PRIVATE_KEY`
   - **Value**: 你的 `id_rsa` 私钥文件的完整内容
   ```text
   -----BEGIN RSA PRIVATE KEY-----
   ...
   -----END RSA PRIVATE KEY-----
   ```

**为什么改名为 `SSH_PRIVATE_KEY`？**
- 这个私钥将同时用于 Gitee 和 GitLab
- 使用更通用的命名更清晰
- 避免平台特定的命名

### 4. 提交配置文件

Workflow 文件已经配置好了，位置在 `.github/workflows/sync-to-gitee.yml`

现在提交并推送：

```bash
git add .
git commit -m "Add GitLab sync support"
git push github main
```

## 📝 Workflow 说明

当前 Workflow 会执行以下步骤：

```yaml
- 设置 SSH 密钥（同时配置 GitHub、Gitee、GitLab 的 known_hosts）
- 推送到 Gitee
- 推送到 GitLab
```

### 分支映射

- **Gitee**: GitHub 的 `main` → Gitee 的 `master`
- **GitLab**: GitHub 的 `main` → GitLab 的 `main`

如果需要修改分支映射，编辑 `.github/workflows/sync-to-gitee.yml`：

```yaml
# 推送到 Gitee
git push gitee main:master --force

# 推送到 GitLab
git push gitlab main:main --force
```

## 🔍 验证同步

### 1. 查看 GitHub Actions

1. 访问 https://github.com/VincentZyu233/github-gitee-sync-test/actions
2. 查看 "Sync to Multiple Platforms" workflow 的运行状态
3. 点击运行记录查看详细日志

### 2. 检查 Gitee 仓库

访问：https://gitee.com/vincent-zyu/github-gitee-sync-test

### 3. 检查 GitLab 仓库

访问：https://gitlab.com/VincentZyu233/github-gitee-sync-test

## 💡 常见问题

### Q1: GitLab 提示 "Fingerprint already exists"

**A**: 这是正常的！说明你的 SSH 公钥之前已经添加过（在 Gitee 或其他平台）。同一个公钥可以用在多个 Git 平台上，直接点击添加即可。

### Q2: 可以使用不同的 SSH 密钥吗？

**A**: 可以，但不推荐。使用同一个私钥更简单：
- 只需配置一个 GitHub Secret
- 减少密钥管理复杂度
- 便于后续维护

如果确实需要使用不同的密钥，可以修改 yml 文件：

```yaml
- name: 设置 Gitee SSH 密钥
  run: |
    echo "${{ secrets.GITEE_PRIVATE_KEY }}" > ~/.ssh/id_rsa_gitee
    chmod 600 ~/.ssh/id_rsa_gitee

- name: 设置 GitLab SSH 密钥
  run: |
    echo "${{ secrets.GITLAB_PRIVATE_KEY }}" > ~/.ssh/id_rsa_gitlab
    chmod 600 ~/.ssh/id_rsa_gitlab
```

然后在推送时指定不同的密钥（需要配置 SSH config）。

### Q3: 如何只同步到某一个平台？

**A**: 注释掉不需要的推送步骤即可：

```yaml
# - name: 添加 Gitee 远程仓库
#   run: |
#     git remote add gitee git@gitee.com:vincent-zyu/github-gitee-sync-test.git
# 
# - name: 推送到 Gitee
#   run: |
#     git push gitee main:master --force

- name: 添加 GitLab 远程仓库
  run: |
    git remote add gitlab git@gitlab.com:VincentZyu233/github-gitee-sync-test.git

- name: 推送到 GitLab
  run: |
    git push gitlab main:main --force
```

### Q4: 推送失败怎么办？

**检查清单**：
1. ✅ SSH 公钥是否正确添加到 Gitee 和 GitLab
2. ✅ GitHub Secret `SSH_PRIVATE_KEY` 是否正确配置
3. ✅ 仓库名称和用户名是否正确
4. ✅ 查看 GitHub Actions 的详细日志

## 🎉 完成！

配置完成后，每次推送到 GitHub，代码会自动同步到 Gitee 和 GitLab 两个平台！

### 仓库地址

- **GitHub**: https://github.com/VincentZyu233/github-gitee-sync-test
- **Gitee**: https://gitee.com/vincent-zyu/github-gitee-sync-test
- **GitLab**: https://gitlab.com/VincentZyu233/github-gitee-sync-test
