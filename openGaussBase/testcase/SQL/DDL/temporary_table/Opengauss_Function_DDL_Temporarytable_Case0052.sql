-- @testpoint: 创建非空约束的临时表,违反约束，合理报错
-- @modify at: 2020-11-24
--建表
drop table if exists temp_table_052;
create temporary table temp_table_052
(id                         number(7)
   constraint temp_table_052_id_nn not null,
 use_filename               varchar2(20),
 filename                   varchar2(255),
 text                       varchar2(2000)
  );
 --插入数据
insert into temp_table_052 values(1,'李','小龙','中国功夫');
--非空约束字段，插入空值，报错
insert into temp_table_052 values('','李','小龙','中国功夫');
insert into temp_table_052 values(null,'李','小龙','中国功夫');
--建表2
drop table if exists temp_table_052_bak;
create temporary table temp_table_052_bak as select text as text from temp_table_052;
--查询
select * from temp_table_052_bak;
--删表
drop table temp_table_052;
drop table temp_table_052_bak;