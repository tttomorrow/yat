-- @testpoint: 创建有唯一约束的临时表，违反约束，合理报错
-- @modify at: 2020-11-24
--建表
drop table if exists temp_table_051;
create  temporary table temp_table_051(a int,b char(10) UNIQUE);
--插入数据
insert into temp_table_051 values(4,'a');
insert into temp_table_051 values(2,'cd');
insert into temp_table_051 values (2,'aw');
insert into temp_table_051 values (2,'');
--插入数据，报错
insert into temp_table_051 values (3,'a');
--查询
select * from temp_table_051;
--删表
drop table temp_table_051;
