# mcp-hot-news 开发文档

## 1. 开发环境设置

### 1.1 环境要求
- Python 3.8+
- Git
- pip

### 1.2 开发环境搭建

```bash
# 克隆项目
git clone https://github.com/yourusername/mcp-hot-news.git
cd mcp-hot-news

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装开发依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## 2. 项目结构

```
mcp-hot-news/
├── src/                    # 源代码目录
│   ├── server.py          # MCP服务器主模块
│   ├── news_fetcher.py    # 新闻数据获取模块
│   ├── news_processor.py  # 新闻数据处理模块
│   ├── models.py          # 数据模型定义
│   └── providers/         # 新闻提供者实现
│       ├── __init__.py
│       ├── base_provider.py
│       ├── wechat_provider.py
│       ├── zhihu_provider.py
│       └── weibo_provider.py
├── docs/                  # 文档目录
│   ├── system_design.md   # 系统设计文档
│   ├── module_design.md   # 模块设计文档
│   ├── code_review.md     # 代码审查文档
│   ├── usage.md          # 使用文档
│   └── development.md    # 开发文档
├── tests/                # 测试目录
├── requirements.txt       # 项目依赖
├── requirements-dev.txt   # 开发依赖
├── README.md             # 项目说明
└── .gitignore            # Git忽略文件
```

## 3. 开发规范

### 3.1 代码风格

- 遵循PEP 8规范
- 使用4空格缩进
- 每行不超过88字符
- 使用类型提示

### 3.2 命名规范

- 类名使用大驼峰命名法（PascalCase）
- 函数和变量使用小写加下划线命名法（snake_case）
- 常量使用大写加下划线命名法（UPPER_SNAKE_CASE）
- 私有方法使用单下划线前缀

### 3.3 注释规范

- 所有公共类和方法必须有docstring
- 复杂逻辑需要添加行内注释
- 使用Google风格的docstring

## 4. 开发流程

### 4.1 分支管理

- main: 主分支，保持稳定
- develop: 开发分支
- feature/*: 功能分支
- bugfix/*: 修复分支

### 4.2 提交规范

提交信息格式：
```
<type>(<scope>): <subject>

<body>

<footer>
```

类型（type）：
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 重构
- test: 测试相关
- chore: 构建/工具相关

示例：
```
feat(providers): 添加今日头条新闻源

- 实现今日头条提供者
- 添加解析逻辑
- 更新文档

Closes #123
```

### 4.3 代码审查

所有代码提交前需要经过代码审查：
1. 自我审查
2. 同事审查
3. 修复审查意见
4. 合并代码

## 5. 测试

### 5.1 单元测试

```bash
# 运行所有测试
pytest tests/

# 运行特定测试文件
pytest tests/test_news_fetcher.py

# 运行特定测试函数
pytest tests/test_news_fetcher.py::test_fetch_hot_news

# 生成覆盖率报告
pytest --cov=src tests/
```

### 5.2 集成测试

```bash
# 运行集成测试
pytest tests/integration/
```

## 6. 文档

### 6.1 文档更新

- 添加新功能时更新使用文档
- 修改设计时更新设计文档
- 重大变更更新README

### 6.2 文档格式

- 使用Markdown格式
- 包含代码示例
- 保持文档简洁清晰

## 7. 发布流程

### 7.1 版本号规范

遵循语义化版本（Semantic Versioning）：
- MAJOR.MINOR.PATCH
- 主版本号：不兼容的API修改
- 次版本号：向下兼容的功能性新增
- 修订号：向下兼容的问题修正

### 7.2 发布步骤

1. 更新版本号
2. 更新CHANGELOG
3. 创建发布标签
4. 推送到远程仓库
5. 构建和发布

## 8. 贡献指南

### 8.1 报告问题

- 使用GitHub Issues
- 提供详细的复现步骤
- 包含错误日志

### 8.2 提交代码

1. Fork项目
2. 创建功能分支
3. 提交代码
4. 创建Pull Request
5. 等待审查

## 9. 常见问题

### 9.1 开发环境问题

#### 问题：依赖安装失败

**解决方案：**
```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 9.2 代码问题

#### 问题：类型检查失败

**解决方案：**
```bash
# 运行类型检查
mypy src/

# 更新类型提示
# 根据错误信息修复类型问题
```

## 10. 工具和资源

### 10.1 开发工具

- IDE: VS Code / PyCharm
- 代码格式化: black
- 代码检查: flake8
- 类型检查: mypy

### 10.2 在线资源

- Python官方文档: https://docs.python.org/
- PEP 8: https://www.python.org/dev/peps/pep-0008/
- MCP文档: https://modelcontextprotocol.io/

## 11. 性能优化

### 11.1 性能分析

```bash
# 使用cProfile分析性能
python -m cProfile -s time -m src.server

# 使用memory_profiler分析内存
python -m memory_profiler src/server.py
```

### 11.2 优化建议

1. 使用异步IO
2. 实现缓存机制
3. 优化数据库查询
4. 使用高效的数据结构

## 12. 安全建议

### 12.1 代码安全

1. 不在代码中硬编码敏感信息
2. 使用环境变量存储配置
3. 定期更新依赖
4. 实现输入验证

### 12.2 部署安全

1. 使用HTTPS
2. 实现访问控制
3. 配置防火墙
4. 定期备份数据
