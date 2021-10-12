-- @testpoint: 在存储过程中给临时表插入数据
-- @modify at: 2020-11-24
--建表
drop table if exists temp_table_064;
create  temporary table temp_table_064(id int);
--创建存储过程
drop procedure if exists proc_064;
CREATE OR REPLACE PROCEDURE proc_064()
AS
BEGIN
    FOR id IN 1..10 loop
        INSERT INTO temp_table_064 VALUES(id);
    END loop;
END;
/
--查询表
select * from temp_table_064;
--删除存储过程
drop procedure proc_064;
--删表
drop table temp_table_064;