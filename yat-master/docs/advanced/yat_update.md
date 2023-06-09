# Yat 升级指导

## Yat升级一般性原则

### 目录结构变化

!!! Note

    yat测试套下一般有若干必须存在的目录，如果不存在yat会拒绝执行，这些目录，随着后续渐进，需要新增的必须目录，
    一般升级yat时需要关注目录变化

#### 升级代价和操作
    
升级代价：极小

升级操作：添加必须的目录和文件

### 配置文件变化

!!! Note

    yat配置文件之前采样properties、xml等形式配置，但是不同类型的配置文件优缺点不一，yat后面慢慢会演进到统一使用yaml形式的配置文件

#### 升级代价和操作

升级代价：极小

升级操作：修改配置文件的形式和内容

### 用例输出变化

!!! Note

    yat支持众多类型的测试用例，yat升级时可能伴随着用例输出文件变化的情况
    
一般对于不同的用例类型yat输出情况不同：

- zsql用例：输出依赖zsql本身的变化，yat不做任何处理（例外，yat新版本输出会在zsql上加上-a参数，用例输出会带上执行的sql）
- sql用例：这部分用例的输出是yat本身控制的，版本升级会有一定变化
- shell：用例几乎不会有变化
- python单元测试用例：不依赖输出，单元测试用例自判断结果

#### 升级代价和操作

依情况而定，具体如下

##### 使用了多文件匹配功能

升级代价：代价中

升级操作：找到一个100%用例通过的数据库版本，重新执行后替换所有期望文件，
之后多次跑用例，获取大部分多目标期望文件，小概率的期望文件可以在平时跑CI时得到

##### 使用了正则匹配功能

升级代价：代价中

升级操作：找到一个100%用例通过的数据库版本，重新执行后替换所有期望文件，后续发现失败，在手动修改期望文件

##### 未使用上述功能

升级代价：代价小

升级操作：找到一个100%用例通过的数据库版本，重新执行后替换所有期望文件


## 0.4.X版本升级0.10.X

1. 必须目录新增：schedule
2. 调度文件放到：schedule
3. 配置文件改为yaml形式
4. 期望替换

## 0.7.X版本升级0.10.X

1. 必须目录新增：schedule
2. 调度文件放到：schedule
3. 配置文件改为yaml形式
4. 期望替换




