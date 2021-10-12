-- @testpoint: 存储过程中删除临时表,删除后查询表，合理报错
-- @modify at: 2020-11-24
--建表
drop table if exists temp_table_028;
create global temporary table temp_table_028(id int,name varchar2(20));
--插入数据
insert into temp_table_028 values (1,'a values');
--创建存储过程
create or replace procedure proc_drop_temp_table_028(v_name  varchar2 ) as
begin
    execute immediate 'drop table if exists temp_table_'|| v_name ;
end;
/
--执行匿名块语句
begin
 proc_drop_temp_table_028('028');
end;
/
--查询表数据，报错
select * from temp_table_028;
--删除存储过程
drop procedure proc_drop_temp_table_028;
