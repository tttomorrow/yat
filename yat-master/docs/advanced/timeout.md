# 用例超时设置

!!! Note
    
    用例超时时间可以通过三种方式设置
    
## 通过配置文件设置

设置粒度：全局设置

在configure.xml中添加

```yaml
yat.case.timeout = 5
```

设置全局用例超时

## 通过命令行设置

设置粒度：全局设置

通过如下方式设置

```shell
yat suite --timeout 5
```

## 通过用例属性设置

设置粒度：用例级别设置

在调度文件中给用例添加timeout属性进行设置，例如：

```text
setup: data_init
group: tc_test_case_001(timeout=5) tc_test_case_002
```

## 三种设置方式优先级

通过用例属性设置 > 通过命令行设置 > 通过配置文件设置