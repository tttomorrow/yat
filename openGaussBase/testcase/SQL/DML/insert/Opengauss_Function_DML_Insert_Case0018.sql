-- @testpoint: 插入数据，使用insert..returning子句，指定字段的输出名称，名称不符合标识符规范，合理报错
--建表
drop table if exists t_insert02;
create table t_insert02(id int,name varchar(10));
--插入数据，输出名称以数字开头，合理报错
insert into t_insert02 values (2,'小名明') returning id,name as 1new_name;
--输出名称以汉字开头，未报错（和pg一致）
insert into t_insert02 values (2,'小名明') returning id,name as 插入new_name;
--输出名称以特殊字符开头，合理报错
insert into t_insert02 values (2,'小名明') returning id,name as *&……new_name;
--删表
drop table if exists t_insert02;
