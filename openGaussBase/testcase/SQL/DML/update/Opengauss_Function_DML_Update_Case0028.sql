-- @testpoint: 修改表，alias参数测试，别名不符合标识符命名规范,合理报错
--建表
drop table if exists t_update01;
create table t_update01(id int,name varchar(10));
--插入数据
insert into t_update01 values(1,'hello'),(2,'world'),(3,'hello1');
--修改表数据，指定alias参数，别名由数字开头,合理报错
update t_update01 as 1_update01$ set id = 5 where name = 'world';
--修改表数据，指定alias参数，别名以()开头，省略as选项，合理报错
update t_update01 ()_update01$ set id = 5 where name = 'world';
--修改表数据，指定alias参数，别名以汉字开头，未报错，修改成功(和pg一致)
update t_update01 as 修改_update01$ set id = 5 where name = 'world';
--删除表
drop table t_update01;