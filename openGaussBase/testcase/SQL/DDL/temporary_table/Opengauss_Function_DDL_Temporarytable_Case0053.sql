-- @testpoint: 创建检查约束的临时表，违反约束，合理报错
-- @modify at: 2020-11-24
--建表
drop table if exists temp_table_053;
create temporary table temp_table_053 ( id_p int check (id_p>0), lastname varchar(255) not null);
--插入数据，成功
insert into temp_table_053 values(10,'qw');
insert into temp_table_053 values(09,'ijw');
insert into temp_table_053 values(123,'xcbnw');
--插入数据,报错
insert into temp_table_053 (id_p,lastname) values(0,'b');
insert into temp_table_053 values(-9,'xw');
--查询
select * from temp_table_053;
--删表
drop table  temp_table_053;