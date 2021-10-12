-- @testpoint: 修改表，alias参数测试，别名符合标识符命名规范
--建表
drop table if exists t_update01;
create table t_update01(id int,name varchar(10));
--插入数据
insert into t_update01 values(1,'hello'),(2,'world'),(3,'hello1');
--修改数据，指定alias参数，别名由为字母、下划线、数字（0-9）或美元符号（$）组成
update t_update01 t_update01$ set id = id + 1 where name = 'hello';
select * from t_update01;
--修改数据，指定alias参数，别名以_开头，添加as选项
update t_update01 as _update01$ set id = 50 where name = 'hello1';
--修改表数据，指定alias参数，别名以大写字母开头
update t_update01 as T_update01$ set id = 5 where name = 'world';
--修改数据，指定alias参数，别名以大写字母开头且添加双引号
update t_update01 as "T_update01$" set id = 54 where name = 'world';
--删除表
drop table t_update01;