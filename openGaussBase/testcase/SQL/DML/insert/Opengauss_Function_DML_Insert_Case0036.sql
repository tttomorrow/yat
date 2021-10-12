-- @testpoint: 插入数据，指定default选项
--建表
drop table if exists t_insert001;
create table t_insert001(c_insert1 char(20),c_insert2 bit varying(10));
--插入数据,添加default，不给默认值，插入null
insert into t_insert001 default values;
insert into t_insert001 values (default);
--查询
select * from t_insert001;
--删除表
drop table t_insert001;