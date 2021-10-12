-- @testpoint: 表和锁（ACCESS SHARE）
drop table if exists table_1;
create table table_1(id int,sname char(20),city varchar(20),number number);
START TRANSACTION;
LOCK TABLE table_1 IN ACCESS SHARE MODE;
select * from table_1;
DELETE FROM table_1;
COMMIT;
DROP TABLE if exists table_1;