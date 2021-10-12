-- @testpoint: 表在存储过程中使用中调用
drop procedure if exists proc_001;
drop table if exists table_001;
create table table_001(id int);
select * from table_001;
CREATE OR REPLACE PROCEDURE proc_001()
AS
BEGIN
    FOR id IN 1..10 loop
        INSERT INTO table_001 VALUES(id);
    END loop;
END;
/
call proc_001();
select * from table_001;

drop procedure if exists proc_001;
drop table if exists table_001;