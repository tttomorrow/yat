# Yat suite命令说明

## 命令行格式说明

```bash
yat suite [sub-command] [options]
```

支持的子命令有：

- run
- init
- mkschd
- bkfill (not support now)

下面对子命令和其选项进行详细说明

## 子命令说明

### run

run命令用来执行测试套，其中run关键字可以省略，例如：

```bash
yat suite run

yat suite # 等于 yat suite run 
```

run命令支持很多选项以丰富其功能，具体的每一项选项如下：

#### -d/--test-dir

用来指定测试套所在目录，不指定默认为当前目录

#### -s/--schedule

用来指定要执行的调度文件，不指定的话默认从schedule/schedule.schd中加载，如果找不到给定的文件，就会报错

**需要注意**

如果用户指定的调度文件路径是一个相对路径，调度文件的搜索顺序为：

1. 当前目录
2. 测试套根目录下的schedule目录

如果用户指定的调度文件是一个绝对路径，这直接使用此文件

!!! Note

    推荐将调度文件都放到测试套根目录下的`schedule`目录中，所有需要指定调度文件时，直接使用相对路径指定即可
    
如,在下面目录结构下：

```text
.
├── conf
│   ├── configure.yml
│   ├── env.sh
│   ├── macro.yml
│   └── nodes.yml
├── expect
│   └── abc
├── lib
│   └── pyzenith.so
├── log
├── result
│   └── test_001
├── schedule
│   ├── schedule1.schd
│   ├── schedule2.schd
│   └── sub-schedule
│       ├── schedule3.schd
│       └── schedule4.schd
├── temp
└── testcase
    └── test_001.py

```

指定不同的调度文件可以这么写：

```bash
yat sutie -s schedule1.schd
yat suite -s schedule2.schd
yat suite -s sub-schedule/schedule3.schd
yat suite -s sub-schedule/schedule4.schd
```

可以看到用户根本不需要关系调度文件的绝对路径和位置，只需要指定名称即可

#### -m/--mode

#### -l/--left

#### -r/--right

#### -t/--target

#### -f/--configure

#### -p/prefix-run-shell 

#### --timeout

设置所有用例超时时间，单位秒，详见[用例超时设置章节](../../advanced/timeout)

#### -i/--macro

#### -n/--node

#### -e/--macro-file

#### -o/--output

#### -x/--cases

#### --width

设置打印报告宽度，在用例名字特别长、嵌套目录特别深的情况下，由于报告宽度限制，用例名字会被截断，适当增加打印宽度

!!! Note

    其实终极解决办法是，用例命名规范、用例目录嵌套规范，如果目录嵌套大于4层，用例名字过长，要考虑一下自己对用例的类型划分和用例要测什么
    真的清楚了吗？思路越清晰，用例越简单！！

#### --bare

不打印报告头和报告尾信息，直接打印一行一行的用例执行情况

#### --color

打印报告在终端中彩色输出

!!! Warning

    前提是中断支持彩色模式

#### --lib-path

#### --no-echo

#### --panic

只要有用例失败，就直接退出yat


#### --no-clean


### init

init子命令可以初始化一个空的默认测试套模板，用户可以使用此命令快速生成测试套

#### -d/--test-dir

同run，不指定默认在当前目录生成测试套模板

如：

```bash
yat suite init  # 在当前目录生成测试套模板
yat suite init -d ../abc # 在上级目录生成一个目录名字为abc的测试套
```

#### -c/--config-opt

初始化测试套时，覆盖默认的配置文件

### mkschd

mkschd子命令用来生成默认的调度文件

!!! Warning

    使用此命令生成的调度文件默认使用用例名字字典序，如果对调度顺序没有要求，这样是方便快捷的，但是如果对调度顺序敏感，就不适合直接生成了
    用户可以使用此命令生成一个用例名字字典序排序的调度文件，然后手工调整

#### -d/--test-dir

同run
