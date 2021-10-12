--  @testpoint:delete语法中，WHERE condition参数测试
drop table if exists t_delete05;
create table t_delete05(age int,salary numeric);
--插入数据
insert into t_delete05 values(25,8500);
insert into t_delete05 values(30,9500.50);
insert into t_delete05 values(45,6000);
--使用delete语句,where条件中使用between,删除1条数据
delete FROM t_delete05 WHERE age between 20 and 25;
--使用delete语句，where条件中使用IS NOT NULL,删除0条数据
delete FROM t_delete05 WHERE AGE IS NULL;
--使用delete语句，where条件中使用IS NOT NULL,删除2条数据
delete FROM t_delete05 WHERE AGE IS not NULL;
--使用delete语句，where条件中使用子查询
SELECT AGE FROM t_delete05 WHERE EXISTS (SELECT AGE FROM t_delete05 WHERE SALARY > 65000);
--删除表
drop table t_delete05;