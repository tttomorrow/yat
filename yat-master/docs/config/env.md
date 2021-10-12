# env.sh配置说明

!!! Note

    不要将`macro.yml`和`env.sh`两个文件混淆，`macro.yml`中是定义宏变量的，可以在期望文件、用例文件中使用，
    而`env.sh`是在执行执行yat命令之前，先`sources`一下，这个文件，相当于`yat`自己`profile`文件，用户可以在里面写
    任何`shell`命令，但是建议只定义环境变量等。
    
## 举例

例如我们要禁止`zsql`执行时卡主提示`SSL`不安全，让用户输入`Y`，就可以在`env.sh`中写入：

```bash
export ZSQL_SSL_QUIET=TRUE 
```

`env.sh` 用途和功能很简单，这里不做过多说明，理解用户`profile`文件就能理解`yat`的`env.sh`
