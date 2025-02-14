# 介绍
`hterm`是一款终端工具，目前支持建立`SSH`、`Serial`、`Shell`会话

# 功能
1. 会话管理
    - 图形界面会话创建、配置保存
2. 快捷命令发送
    - 支持从python脚本生成
    - 支持发送延时
3. 触发器
    - 正则匹配触发条件
    - 触发后发送文本，支持从python脚本生成
# 使用
### 安装uv
``` shell 
pip install uv
```
### 运行
1. 同步项目依赖环境
``` shell
uv sync
```
2. 运行
``` shell
uv run hterm/main.py
```
### 打包
``` shell
uv run build.py
```
成果物路径`dist/hterm`
