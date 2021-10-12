# multi-suite schedule

!!! Note

    `Yat Schedule`是`Yat`提供的一种同时调度多个`Yat`测试套的调度器，用户通过制定调度文件来进行多个`Yat`测试套的并行或串行的调度

## Yat Schedule文法说明

### 并行调度

```text
parallel {
    suite 'path/to/suite/dir/1';
    suite 'path/to/suite/dir/2' '-s' 'schedule-A.schd';
    suite 'path/to/suite/dir/2' '-s' 'schedule-B.schd';

    ...
}
```

- 其中`parallel {}`表示一组并行调度的调度列表，将所需要进行调度的测试套列表写进`{}`中间即可
- `suite suite-path param1 param2 param3 ...` 描述了调度一个测试套需要的信息，包括：
- - 关键字`suite`
- - `suite-path`测试套的路径，此路径如果是相对路径，相对`schedule`调度文件所在目录
- - 参数列表`param1 param2 param3 ...`运行yat测试套需要的参数，相当于运行`yat suite run param1 param2 param3 ...`
- `parallel {}`中所有的测试套都是并行调度的

### 串行调度

```text
serial {
    suite 'path/to/suite/dir/1';
    suite 'path/to/suite/dir/2' '-s' 'schedule-A.schd';
    suite 'path/to/suite/dir/2' '-s' 'schedule-B.schd';

    ...
}
```

所有的文法表示都和并行调度相同，不同点：

- 调度组以`serial`开头
- 所有的测试套一个一个串行执行

### 串行并行嵌套调度

```text
serial {
    suite 'path/to/suite/dir/1';
    suite 'path/to/suite/dir/2' '-s' 'schedule-A.schd';
    suite 'path/to/suite/dir/2' '-s' 'schedule-B.schd';

    ...

    parallel {
        suite 'path/to/suite/dir/1';
        suite 'path/to/suite/dir/2' '-s' schedule-A.schd '-m' single;
        suite 'path/to/suite/dir/2' '-s' 'schedule-B.schd';

        serial {
            suite 'path/to/suite/dir/1';
            suite 'path/to/suite/dir/2' '-s' 'schedule-A.schd';
            suite 'path/to/suite/dir/2' '-s' 'schedule-B.schd';
        }
    }

    ...
}
```

- 理论上嵌套层次没有限制，嵌套层次限制于内存资源和操作系统最大线程和进程数，建议最多嵌套2层
- 可以任意组合`serial {}`和`parallel {}`块儿

### 调度文件规范

- 一般情况下调度文件文件后缀用.ys结尾
- 调度文件放到所有测试套所在目录的上层目录

## 命令行接口说明

### 执行调度

```bash
yat schedule -s all.ys
```

### 帮助信息查看

```bash
yat schedule --help
```
