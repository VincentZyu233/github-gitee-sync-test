# 使用 Python 脚本配置 SSH 密钥

本仓库提供了一个 Python 脚本 `setup_ssh_key.py`，可以自动生成 SSH 密钥对，并指导你完成配置。

## 🚀 快速开始

### 1. 运行脚本

在仓库根目录下执行：

```bash
python setup_ssh_key.py
```

或者如果使用 Python 3：

```bash
python3 setup_ssh_key.py
```

### 2. 按照脚本提示操作

脚本会逐步引导你完成以下步骤：

#### 步骤 1: 添加公钥到 Gitee

脚本会显示公钥内容，复制后访问：
- https://gitee.com/profile/sshkeys
- 点击「添加公钥」，粘贴内容

#### 步骤 2: 添加公钥到 GitLab

使用相同的公钥，访问：
- https://gitlab.com/-/profile/keys
- 点击「Add new key」，粘贴内容
- 如果提示「Fingerprint already exists」，直接添加即可（说明公钥已经在其他平台使用过）

#### 步骤 3: 配置 GitHub Secret

脚本会显示完整的私钥内容（包括开头和结尾的标记），复制后访问：
- https://github.com/VincentZyu233/github-gitee-sync-test/settings/secrets/actions
- 点击「New repository secret」
- Name 输入: `SSH_PRIVATE_KEY`
- Value 粘贴私钥完整内容
- 点击「Add secret」

#### 步骤 4: 提交并推送代码

执行以下命令：

```bash
git add .
git commit -m "Add SSH key for sync"
git push github main
```

然后访问 GitHub Actions 页面查看同步结果：
- https://github.com/VincentZyu233/github-gitee-sync-test/actions

## 💡 为什么使用这个脚本？

### 解决的问题

之前直接在 PowerShell 中执行 `cat ~\.ssh\id_rsa` 复制私钥时，遇到的问题是：

1. **内容截断**：PowerShell 可能不会完整显示长文本
2. **格式错误**：复制时可能缺少开头或结尾的标记
3. **手动操作繁琐**：需要手动切换多个平台配置

### 脚本的优势

1. ✅ **自动生成密钥**：生成新的 RSA 4096 位密钥对
2. ✅ **完整显示**：确保公钥和私钥内容完整显示
3. ✅ **步骤引导**：逐步引导完成配置
4. ✅ **避免错误**：减少手动复制粘贴的错误

## 📁 生成的文件

脚本会在当前目录生成：

- `deploy_key` - SSH 私钥（已添加到 .gitignore，不会提交）
- `deploy_key.pub` - SSH 公钥（可以安全提交到仓库）

## 🔒 安全说明

- 私钥文件 `deploy_key` 已添加到 `.gitignore`，不会被提交到仓库
- 公钥文件 `deploy_key.pub` 是公开的，可以安全提交
- 建议将私钥文件备份到安全位置
- 如果密钥泄露，可以重新运行脚本生成新密钥

## 🔧 高级用法

### 使用现有的密钥

如果你已经有 SSH 密钥，不想生成新的，可以：

1. 手动复制你的私钥到 `deploy_key`
2. 手动复制你的公钥到 `deploy_key.pub`
3. 按照上述步骤配置各平台

### 重新生成密钥

如果密钥出现问题，可以重新运行脚本，脚本会提示是否覆盖现有密钥：

```bash
python setup_ssh_key.py
```

选择 `y` 重新生成密钥。

## 🐛 常见问题

### Q1: 脚本运行失败，提示找不到 Python

**A**: 确保已安装 Python 3，可以使用以下命令检查：

```bash
python --version
# 或
python3 --version
```

如果没有安装，从 https://www.python.org/downloads/ 下载安装。

### Q2: 脚本提示生成密钥失败

**A**: 可能是 `ssh-keygen` 命令未找到。确保已安装 Git，Git 包含 `ssh-keygen`。

或者手动生成密钥：

```bash
ssh-keygen -t rsa -b 4096 -C "github-actions-sync" -f deploy_key -N ""
```

### Q3: 配置后同步仍然失败

**A**: 检查以下几点：

1. 确认 SSH_PRIVATE_KEY 是否正确配置（完整包含开头和结尾标记）
2. 确认公钥已添加到 Gitee 和 GitLab
3. 查看 GitHub Actions 的详细日志
4. 确认仓库名称和用户名正确

### Q4: GitLab 提示 "Fingerprint already exists"

**A**: 这是正常的！说明这个 SSH 公钥已经在其他平台（如 Gitee）使用过。同一个公钥可以用在多个 Git 平台，直接点击添加即可。

## 📚 相关文档

- [GitHub Actions 同步到 Gitee 和 GitLab](gitlab配置说明.md)
- [GitHub 到 Gitee 自动同步教程](github到gitee自动同步教程.md)

## ✅ 完成检查清单

配置完成后，确认以下项目：

- [ ] 公钥已添加到 Gitee
- [ ] 公钥已添加到 GitLab
- [ ] GitHub Secret `SSH_PRIVATE_KEY` 已配置
- [ ] 代码已推送到 GitHub
- [ ] GitHub Actions 运行成功
- [ ] Gitee 仓库已同步
- [ ] GitLab 仓库已同步

如果全部勾选，恭喜！配置完成！🎉
