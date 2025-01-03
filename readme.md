# git 历史提交内容修改  
需求: 修改git 的commit时间，commit内容，提交用户名修改，并且保持gitlab库上的时间也是过去的时间。

# 思路和步骤
raw_path 为原始需要修改的git库，new_path为新库  
通过 checkout 到 raw_path 中每个节点，作为当时的状态  
通过 cp 拷贝到 new_path 中作为文件修改的操作  
将后续 git commit -m 'test' --date='' 来设置commit时间     

# git command
```
    # git 日志获取
    # https://blog.csdn.net/bingyu9875/article/details/108846188  获取日志的项目
    git log --pretty='format:%H %cI %s'

```

# linux time set
``` 
    # git push 时间设置，通过修改linux时间
    # https://www.cnblogs.com/sdadx/p/13838696.html
    # 关闭时间同步
    sudo timedatectl set-ntp true  
    # 设置时间
    sudo date --set="2021-02-28 10:27:11"
```

# 使用指南 demo 
- 要求 linux , python > 3.6 
- tar -zxvf raw.tgz    # 解压例子git目录
- vi create_new.py     # 配置 main函数中 user 的信息
- python create_new.py git.log # 生成 git.log
- python create_new.py # 生成  cmd.sh
- vi git.log           # 修改 time和message
- bash cmd.sh          # 执行 创建new 新项目

