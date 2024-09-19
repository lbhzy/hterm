# hterm
`hterm`是一款终端工具，目前支持建立`SSH`、`Serial`、`Shell`会话

# 使用
1. 安装依赖
``` shell 
pip install -r requirements.txt
```
2. 运行
``` shell
py main.py
```

# 打包
运行`build.bat`，成果物路径`./dist/hterm`

# TODO
1. 会话管理
    - 图形界面会话创建、配置保存
2. 快捷命令发送
    - 支持脚本生成
3. 触发器
    - 正则匹配触发条件
    - 触发后支持多种行为
    - 发送文本支持脚本生成