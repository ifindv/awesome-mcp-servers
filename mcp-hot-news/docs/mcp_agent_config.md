# MCP Agent 配置指南

## 在 Agent 中配置 MCP 热点新闻服务器

### 1. 配置概述

MCP (Model Context Protocol) 服务器可以通过配置文件添加到支持 MCP 的 Agent 中。本指南将说明如何配置 `mcp-hot-news` 服务器。

### 2. 配置文件位置

MCP Agent 的配置文件通常位于以下位置：

- **Windows**: `%APPDATA%\Code\User\globalStorage\mcp-agent\config.json`
- **macOS**: `~/Library/Application Support/Code/User/globalStorage/mcp-agent/config.json`
- **Linux**: `~/.config/Code/User/globalStorage/mcp-agent/config.json`

### 3. 配置文件格式

配置文件使用 JSON 格式，基本结构如下：

```json
{
  "mcpServers": {
    "mcp-hot-news": {
      "command": "python3",
      "args": [
        "e:/code/mcp-servers/mcp-hot-news/src/server.py"
      ],
      "env": {}
    }
  }
}
```

### 4. 配置说明

#### 4.1 服务器名称

`"mcp-hot-news"` 是服务器的唯一标识符，你可以在 Agent 中使用这个名称来引用该服务器。

#### 4.2 命令 (command)

指定运行服务器的命令。对于 Python 服务器，使用 `python` 或 `python3`。

#### 4.3 参数 (args)

指定传递给命令的参数。这里需要提供 `server.py` 的完整路径。

**注意**：

- 在 Windows 上使用正斜杠 `/` 或双反斜杠 `\\` 作为路径分隔符
- 确保路径指向正确的 `server.py` 文件

#### 4.4 环境变量 (env)

如果需要设置环境变量，可以在 `env` 字段中添加：

```json
{
  "mcpServers": {
    "mcp-hot-news": {
      "command": "python",
      "args": [
        "e:/code/mcp-servers/mcp-hot-news/src/server.py"
      ],
      "env": {
        "PYTHONPATH": "e:/code/mcp-servers/mcp-hot-news/src"
      }
    }
  }
}
```

### 5. 多服务器配置

如果需要配置多个 MCP 服务器，可以在 `mcpServers` 中添加多个条目：

```json
{
  "mcpServers": {
    "mcp-hot-news": {
      "command": "python",
      "args": [
        "e:/code/mcp-servers/mcp-hot-news/src/server.py"
      ]
    },
    "other-server": {
      "command": "node",
      "args": [
        "path/to/other/server.js"
      ]
    }
  }
}
```

### 6. 使用虚拟环境

如果使用 Python 虚拟环境，需要指定虚拟环境中的 Python 解释器：

```json
{
  "mcpServers": {
    "mcp-hot-news": {
      "command": "e:/code/mcp-servers/mcp-hot-news/venv/Scripts/python.exe",
      "args": [
        "e:/code/mcp-servers/mcp-hot-news/src/server.py"
      ]
    }
  }
}
```

### 7. 验证配置

配置完成后，重启 Agent 并检查：

1. Agent 启动日志中是否显示 `mcp-hot-news` 服务器已连接
2. 在 Agent 中尝试调用新闻相关功能
3. 检查是否有错误信息

### 8. 可用功能

配置成功后，Agent 将可以使用以下功能：

- 获取热点新闻
- 按新闻源获取新闻（微信、知乎、微博）
- 按分类获取新闻（科技、娱乐、体育、财经、社会、国际、其他）
- 搜索新闻
- 获取新闻分类列表
- 获取新闻源列表

### 9. 故障排除

#### 9.1 服务器无法启动

**检查项**：

- Python 路径是否正确
- `server.py` 文件路径是否正确
- 是否安装了所有依赖（运行 `pip install -r requirements.txt`）

#### 9.2 Agent 无法连接到服务器

**检查项**：

- 配置文件路径是否正确
- 配置文件格式是否正确（JSON 语法）
- Agent 是否支持 MCP

#### 9.3 功能不可用

**检查项**：

- 服务器是否正常启动
- Agent 日志中是否有错误信息
- 尝试手动运行服务器：`python e:/code/mcp-servers/mcp-hot-news/src/server.py`

### 10. 高级配置

#### 10.1 自定义日志级别

可以通过环境变量设置日志级别：

```json
{
  "mcpServers": {
    "mcp-hot-news": {
      "command": "python",
      "args": [
        "e:/code/mcp-servers/mcp-hot-news/src/server.py"
      ],
      "env": {
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

#### 10.2 使用不同的工作目录

如果需要指定工作目录：

```json
{
  "mcpServers": {
    "mcp-hot-news": {
      "command": "python",
      "args": [
        "src/server.py"
      ],
      "cwd": "e:/code/mcp-servers/mcp-hot-news"
    }
  }
}
```

### 11. 示例对话

配置成功后，你可以与 Agent 进行如下对话：

```
你：今天有什么热点新闻？
Agent：[调用 get_hot_news] 今天的热点新闻包括：
1. [新闻标题1] - 热度：100
2. [新闻标题2] - 热度：95
...

你：有什么科技新闻吗？
Agent：[调用 get_news_by_category] 最新的科技新闻有：
1. [科技新闻标题1] - 热度：80
2. [科技新闻标题2] - 热度：75
...

你：搜索关于人工智能的新闻
Agent：[调用 search_news] 找到以下关于人工智能的新闻：
1. [AI新闻标题1] - 热度：90
2. [AI新闻标题2] - 热度：85
...
```

### 12. 更新日志

#### v0.1.0 (2024-01-01)

- 初始版本
- 支持 MCP Agent 配置
- 提供完整的配置指南
