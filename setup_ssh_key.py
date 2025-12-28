#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSH 密钥生成和配置脚本
用于生成新的 SSH 密钥对，并显示配置步骤
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, capture=True):
    """执行命令"""
    try:
        if capture:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
            return result.returncode, result.stdout, result.stderr
        else:
            result = subprocess.run(cmd, shell=True)
            return result.returncode, "", ""
    except Exception as e:
        return -1, "", str(e)

def main():
    print("=" * 80)
    print("GitHub Actions SSH 密钥配置工具")
    print("=" * 80)
    print()
    
    # 获取脚本所在目录
    script_dir = Path(__file__).parent
    private_key_path = script_dir / "deploy_key"
    public_key_path = script_dir / "deploy_key.pub"
    
    # 检查是否已存在密钥
    if private_key_path.exists():
        print(f"⚠️  检测到已存在的密钥文件: {private_key_path}")
        choice = input("是否重新生成？(y/N): ").strip().lower()
        if choice != 'y':
            print("使用现有密钥...")
        else:
            print("正在生成新的 SSH 密钥（传统 PEM 格式）...")
            # 使用 -m PEM 生成传统格式的 RSA 密钥，兼容性更好
            returncode, stdout, stderr = run_command(
                f'ssh-keygen -t rsa -b 4096 -m PEM -C "github-actions-sync" -f "{private_key_path}" -N ""'
            )
            if returncode != 0:
                print(f"❌ 生成密钥失败: {stderr}")
                return
    else:
        print("正在生成新的 SSH 密钥（传统 PEM 格式）...")
        # 使用 -m PEM 生成传统格式的 RSA 密钥，兼容性更好
        returncode, stdout, stderr = run_command(
            f'ssh-keygen -t rsa -b 4096 -m PEM -C "github-actions-sync" -f "{private_key_path}" -N ""'
        )
        if returncode != 0:
            print(f"❌ 生成密钥失败: {stderr}")
            return
    
    # 读取公钥和私钥
    try:
        with open(private_key_path, 'r', encoding='utf-8') as f:
            private_key = f.read()
        
        with open(public_key_path, 'r', encoding='utf-8') as f:
            public_key = f.read()
    except Exception as e:
        print(f"❌ 读取密钥文件失败: {e}")
        return
    
    print()
    print("=" * 80)
    print("步骤 1: 添加公钥到 Gitee")
    print("=" * 80)
    print()
    print("📌 复制以下公钥内容:")
    print("-" * 80)
    print(public_key)
    print("-" * 80)
    print()
    print("然后访问: https://gitee.com/profile/sshkeys")
    print("点击「添加公钥」，粘贴上述内容")
    input("\n按 Enter 键继续...")
    print()
    
    print("=" * 80)
    print("步骤 2: 添加公钥到 GitLab")
    print("=" * 80)
    print()
    print("📌 使用相同的公钥（已复制）")
    print()
    print("访问: https://gitlab.com/-/user_settings/ssh_keys")
    print("点击「Add new key」，粘贴公钥内容")
    print("如果提示「Fingerprint already exists」，直接添加即可")
    input("\n按 Enter 键继续...")
    print()
    
    print("=" * 80)
    print("步骤 3: 配置 GitHub Secret")
    print("=" * 80)
    print()
    print("📌 复制以下私钥完整内容（包含开头和结尾的标记）:")
    print("-" * 80)
    print(private_key)
    print("-" * 80)
    print()
    print("然后访问:")
    print("https://github.com/VincentZyu233/github-gitee-sync-test/settings/secrets/actions")
    print()
    print("1. 点击「New repository secret」")
    print("2. Name 输入: SSH_PRIVATE_KEY")
    print("3. Value 粘贴上述私钥完整内容")
    print("4. 点击「Add secret」")
    input("\n按 Enter 键继续...")
    print()
    
    print("=" * 80)
    print("步骤 4: 提交并推送代码")
    print("=" * 80)
    print()
    print("执行以下命令:")
    print("  git add .")
    print("  git commit -m \"Add SSH key for sync\"")
    print("  git push github main")
    print()
    print("然后访问 GitHub Actions 页面查看同步结果:")
    print("https://github.com/VincentZyu233/github-gitee-sync-test/actions")
    print()
    
    print("=" * 80)
    print("✅ 配置完成！")
    print("=" * 80)
    print()
    print("📁 生成的文件位置:")
    print(f"   私钥: {private_key_path}")
    print(f"   公钥: {public_key_path}")
    print()
    print("💡 提示:")
    print("   - 私钥文件 deploy_key 已添加到 .gitignore，不会被提交")
    print("   - 公钥文件 deploy_key.pub 可以安全提交到仓库")
    print("   - 请妥善保管私钥文件")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        sys.exit(1)
