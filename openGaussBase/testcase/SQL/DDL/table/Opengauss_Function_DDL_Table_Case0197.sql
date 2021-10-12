-- @testpoint: 存储过程中truncate table
drop procedure if exists proc_001;
drop table if exists table_001;
create table table_001(id int);
select * from table_001;
CREATE OR REPLACE PROCEDURE proc_001()
AS
BEGIN
    truncate table table_001;
END;
/
call proc_001();
select * from table_001;
drop procedure if exists proc_001;
drop table if exists table_001;





