-- @testpoint: 修改表的一列类型char为varchar类型，插入数据，超过长度限制，合理报错
-- @modify at: 2020-11-23
--建表
drop table if exists temp_table_alter_008;
create global temporary table temp_table_alter_008(a char,c varchar(10)) on commit preserve rows;
--插入数据，报错
insert into temp_table_alter_008 values('测试','测试人员');
--修改a列数据类型
alter table temp_table_alter_008 modify(a varchar(60));
--插入数据
insert into temp_table_alter_008 values('测试','测试人');
insert into temp_table_alter_008 values('dddddhdfghjkl5455221%^%^&*&&*edrtfyuio',90);
--修改a列数据类型
alter table temp_table_alter_008 modify(a char(60));
alter table temp_table_alter_008 modify(a varchar(100));
--查询表
select * from temp_table_alter_008;
--删表
drop table temp_table_alter_008;