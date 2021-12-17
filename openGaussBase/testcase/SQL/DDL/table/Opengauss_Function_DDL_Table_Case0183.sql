-- @testpoint: 表和锁（ACCESS EXCLUSIVE）
drop table if exists table_2;
create table table_2(id int,sname char(20),city varchar(20),number number);
insert into table_2 values(1,'joe','a',12323455646);
insert into table_2 values(2,'jojo','b',124232345456);
insert into table_2 values(3,'jane','c',12557676878);
START TRANSACTION;
LOCK TABLE table_2 IN ACCESS EXCLUSIVE MODE;
select * from table_2;
DELETE FROM table_2;
COMMIT;
DROP TABLE if exists table_2;
