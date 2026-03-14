# Agent

## 目录

- [环境配置](#环境配置)
  - [快速开始](#快速开始)
  - [一、WSL2 安装与配置](#一wsl2-安装与配置)
  - [二、uv 项目管理工具](#二uv-项目管理工具)
  - [三、项目初始化流程](#三项目初始化流程)

## 环境配置

### 快速开始

本项目需要以下环境：
- **WSL2**（Windows Subsystem for Linux 2）
- **Python 3.8+**
- **uv** 包管理工具

如果您是第一次配置开发环境，请按照下方步骤详细说明进行操作。

---

### 一、WSL2 安装与配置

#### 1.1 什么是 WSL2？

WSL2（Windows Subsystem for Linux 2）是微软提供的在Windows上运行Linux的技术，能让您在Windows系统中直接使用Linux环境和工具，无需双系统或虚拟机。

#### 1.2 系统要求

在开始之前，请确保您的电脑满足以下条件：

- ✅ **操作系统**：Windows 10 版本 2004 及以上，或 Windows 11
- ✅ **处理器虚拟化**：BIOS/UEFI 中已启用虚拟化支持（Intel VT-x 或 AMD-V）
- ✅ **内存**：至少 4GB RAM（建议 8GB 以上）
- ✅ **磁盘空间**：至少 10GB 可用空间

#### 1.3 检查虚拟化是否启用

在安装前，需要确认您的电脑已启用虚拟化：

1. 按 `Ctrl + Shift + Esc` 打开任务管理器
2. 点击【性能】标签
3. 选择【CPU】
4. 查看右下方是否显示 **"虚拟化: 已启用"**

**如果显示"已禁用"**，需要进入 BIOS/UEFI 设置：

1. 重启电脑，在开机时按 `Del`、`F2` 或 `F12`（根据主板品牌不同）
2. 找到 **Virtualization Technology** 或 **Intel VT-x** / **AMD-V** 选项
3. 设置为 **Enabled**（启用）
4. 保存并退出（通常按 `F10`）

#### 1.4 一键安装 WSL2

1. **以管理员身份打开 PowerShell**：
   - 按 `Win + X`，选择【Windows PowerShell（管理员）】或【终端（管理员）】

2. **执行安装命令**：

```powershell
wsl --install
```

这个命令会自动完成以下操作：
- ✓ 启用 WSL 功能
- ✓ 启用虚拟机平台
- ✓ 下载并安装最新的 Linux 内核
- ✓ 安装 Ubuntu 发行版（默认）

3. **重启电脑**：
   - 安装完成后，按照提示重启计算机

4. **首次配置**：
   - 重启后，Ubuntu 会自动启动
   - 系统会提示您创建 Linux 用户名和密码（请牢记！）
   - 用户名建议使用小写字母，密码输入时不会显示任何字符（这是正常的）

#### 1.5 验证安装

打开 PowerShell，执行以下命令查看 WSL 版本：

```powershell
wsl --version
```

查看已安装的 Linux 发行版：

```powershell
wsl --list --verbose
```

您应该能看到类似以下输出：

```
  NAME      STATE           VERSION
* Ubuntu    Running         2
```

#### 1.6 进入 WSL2 环境

有多种方式进入 WSL2：

**方式一：通过命令行**
```powershell
wsl                    # 进入默认的 Linux 发行版
```

**方式二：指定发行版**
```powershell
wsl -d Ubuntu          # 进入 Ubuntu
```

**方式三：使用 Windows Terminal**
- 打开 Windows Terminal
- 点击顶部的下拉箭头，选择 Ubuntu

**退出 WSL**
```bash
exit                   # 退出并返回 Windows
```

#### 1.7 /mnt 与 Windows 文件共享

WSL2 提供了便捷的文件系统互访功能：

##### 从 Linux 访问 Windows 文件

Windows 的所有磁盘会自动挂载到 `/mnt/` 目录下：

| Windows 路径 | Linux 路径 | 说明 |
|-------------|-----------|------|
| `C:\` | `/mnt/c/` | C 盘根目录 |
| `D:\` | `/mnt/d/` | D 盘根目录 |
| `C:\Users\用户名\Documents` | `/mnt/c/Users/用户名/Documents` | 文档文件夹 |

**示例**：在 WSL2 中访问 Windows 的 D 盘项目文件夹

```bash
cd /mnt/d/MyProject/Agent
ls                     # 列出文件
```

##### 从 Windows 访问 Linux 文件

1. 打开 Windows 文件资源管理器
2. 在地址栏输入：`\\wsl$\Ubuntu\home\你的用户名\`
3. 或者在 WSL 中执行 `explorer.exe .` 直接打开当前目录

##### ⚠️ 性能建议

- **推荐做法**：将项目文件存放在 Linux 文件系统中（`~` 或 `/home/用户名/`）
- **不推荐**：将项目存放在 `/mnt/c/` 等 Windows 挂载路径
- **原因**：跨文件系统访问会导致明显的性能下降，特别是对于包含大量小文件的项目（如 node_modules、.venv）

**最佳实践**：

```bash
# 在 WSL2 中创建项目目录
mkdir -p ~/projects
cd ~/projects
git clone <项目地址>
```

---

### 二、uv 项目管理工具

#### 2.1 什么是 uv？

`uv` 是一个现代化的 Python 包管理和项目管理工具，由 Astral 团队开发（Ruff 的作者）。它的特点是：

- ⚡ **极速**：依赖安装速度比 pip 快 10-100 倍
- 🔒 **可靠**：通过 `uv.lock` 锁文件确保环境一致性
- 🎯 **简单**：一个工具管理 Python 版本、虚拟环境和依赖
- 🌍 **兼容**：完全兼容 pip 和 PyPI 生态

#### 2.2 安装 uv

##### 在 WSL2 (Linux) 中安装

打开 WSL2 终端，执行以下命令：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

安装完成后，重新加载 shell 配置：

```bash
source ~/.bashrc
```

##### 验证安装

```bash
uv --version
```

如果显示版本号（如 `uv 0.x.x`），说明安装成功！

##### （可选）配置国内镜像加速

如果下载包速度较慢，可以配置清华大学镜像源：

```bash
export UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
```

将此行添加到 `~/.bashrc` 文件末尾以永久生效：

```bash
echo 'export UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple' >> ~/.bashrc
source ~/.bashrc
```

#### 2.3 uv 基本命令速查表

| 功能 | 命令 | 说明 |
|------|------|------|
| **项目初始化** | `uv init my_project` | 创建新的 Python 项目 |
| **添加依赖** | `uv add requests` | 安装包并添加到 pyproject.toml |
| **添加开发依赖** | `uv add --dev pytest` | 添加仅开发环境使用的包 |
| **移除依赖** | `uv remove requests` | 卸载包并从配置中移除 |
| **同步环境** | `uv sync` | 根据 uv.lock 安装所有依赖 |
| **运行脚本** | `uv run python script.py` | 在项目虚拟环境中运行 Python |
| **运行命令** | `uv run pytest` | 在虚拟环境中运行任何命令 |
| **列出已安装包** | `uv pip list` | 查看当前环境的所有包 |
| **管理 Python 版本** | `uv python install 3.11` | 安装指定 Python 版本 |
| **查看可用 Python** | `uv python list` | 列出系统中可用的 Python |

#### 2.4 创建新项目示例

```bash
# 创建项目
uv init my_agent
cd my_agent

# 添加依赖
uv add numpy pandas requests

# 添加开发工具
uv add --dev pytest black ruff

# 运行脚本
uv run python main.py
```

#### 2.5 核心概念详解

##### 📁 .venv（虚拟环境目录）

**作用**：
- 为每个项目创建独立的 Python 环境
- 避免不同项目之间的包版本冲突
- 防止污染系统全局 Python 环境

**自动管理**：
- `uv` 会在项目根目录自动创建 `.venv` 文件夹
- 使用 `uv run` 命令时会自动激活虚拟环境
- 无需手动 `source .venv/bin/activate`（但也可以手动激活）

**查看虚拟环境**：

```bash
ls -la                 # 可以看到 .venv 目录
which python           # 显示系统 Python 路径
uv run which python    # 显示项目虚拟环境的 Python 路径
```

##### 🔒 uv.lock（锁定文件）

**作用**：
- 记录项目所有依赖的**精确版本号**（包括间接依赖）
- 确保团队成员和生产环境使用完全相同的包版本
- 类似于 npm 的 `package-lock.json` 或 Rust 的 `Cargo.lock`

**工作流程**：

```bash
# 开发者 A：添加依赖
uv add flask          # 自动更新 uv.lock

# 提交到 Git
git add pyproject.toml uv.lock
git commit -m "添加 Flask 依赖"
git push

# 开发者 B：拉取代码
git pull
uv sync               # 根据 uv.lock 安装完全相同的版本
```

**为什么需要锁定文件？**

假设 `pyproject.toml` 中写着 `requests = ">=2.28.0"`：
- 开发者 A 在 2024 年安装，得到 `requests 2.28.0`
- 开发者 B 在 2026 年安装，得到 `requests 2.32.0`
- 可能导致不同的行为或 bug

有了 `uv.lock`，两人会安装完全相同的 `2.28.0` 版本！

**⚠️ 重要**：
- ✅ **务必将 `uv.lock` 提交到 Git**
- ❌ 不要将 `.venv` 提交到 Git（应加入 `.gitignore`）

##### 📝 pyproject.toml（项目配置文件）

这是 Python 项目的标准配置文件，包含：
- 项目元信息（名称、版本、作者）
- 依赖列表（人类可读的版本约束）
- 构建配置和工具设置

**示例**：

```toml
[project]
name = "my-agent"
version = "0.1.0"
description = "一个智能代理项目"
requires-python = ">=3.8"

dependencies = [
    "requests>=2.28.0",
    "numpy>=1.24.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
]
```

#### 2.6 环境管理进阶

##### 管理 Python 版本

```bash
# 查看可用的 Python 版本
uv python list

# 安装特定版本
uv python install 3.11
uv python install 3.12

# 为项目指定 Python 版本
uv python pin 3.11

# 查看当前项目使用的 Python
uv run python --version
```

##### 手动激活虚拟环境（可选）

虽然 `uv run` 会自动处理，但您也可以手动激活：

```bash
# 激活虚拟环境
source .venv/bin/activate

# 此时命令提示符前会显示 (my_project)
(my_project) $ python script.py
(my_project) $ pytest

# 退出虚拟环境
deactivate
```

##### 清理和重建环境

```bash
# 删除虚拟环境
rm -rf .venv

# 重新同步（会重新创建 .venv）
uv sync
```

---

### 三、项目初始化流程

当您首次克隆本项目或需要设置开发环境时，请按照以下步骤操作：

#### 步骤 1：克隆项目

```bash
# 在 WSL2 中执行
cd ~/projects                    # 切换到您的项目目录
git clone <本项目的Git地址>      # 克隆项目
cd Agent                         # 进入项目目录
```

#### 步骤 2：同步依赖

```bash
uv sync
```

此命令会：
- 读取 `uv.lock` 文件
- 自动创建 `.venv` 虚拟环境
- 安装所有依赖包（与团队保持一致的版本）

#### 步骤 3：验证环境

```bash
# 查看已安装的包
uv pip list

# 查看 Python 版本
uv run python --version
```

#### 步骤 4：运行项目

```bash
# 使用 uv run 运行脚本（推荐）
uv run python main.py

# 或者手动激活虚拟环境后运行
source .venv/bin/activate
python main.py
```

---

### 四、常见操作参考

#### 日常开发工作流

```bash
# 1. 添加新的依赖包
uv add openai anthropic

# 2. 运行测试
uv run pytest

# 3. 运行代码格式化
uv run black .

# 4. 运行类型检查
uv run mypy .

# 5. 更新依赖到最新兼容版本
uv sync --upgrade
```

#### 依赖管理

```bash
# 查看过时的包
uv pip list --outdated

# 添加指定版本的包
uv add "numpy==1.24.0"

# 添加版本范围
uv add "requests>=2.28.0,<3.0.0"

# 从 requirements.txt 导入（如果从旧项目迁移）
uv pip install -r requirements.txt
uv add $(cat requirements.txt)
```

#### 多环境管理

```bash
# 为不同的 Python 版本创建环境
uv venv --python 3.11
uv venv --python 3.12

# 在特定环境中运行
uv run --python 3.11 python script.py
```

---

### 五、故障排除提示

| 问题 | 解决方案 |
|------|---------|
| WSL2 启动失败 | 检查 Windows 功能是否启用，重启电脑 |
| 虚拟化未启用 | 进入 BIOS 启用 VT-x/AMD-V |
| uv 命令未找到 | 执行 `source ~/.bashrc` 或重启终端 |
| 依赖安装缓慢 | 配置国内镜像源（见 2.2 节） |
| 权限错误 | 避免使用 `sudo uv`，检查文件所有权 |

---

### 六、下一步

环境配置完成后，您可以：

1. 📚 阅读项目文档了解架构
2. 🧪 运行测试确保环境正常：`uv run pytest`
3. 💻 开始编写代码
4. 🤝 提交 Pull Request 贡献代码

有问题？请在项目 Issues 中提问！
