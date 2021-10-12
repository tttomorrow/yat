-- @testpoint: 创建存储过程名称验证大小写
drop table if exists test;
drop table if exists LSB_abc;
drop procedure if exists p1;
create table  test(id int,name varchar(100),ctime date);
insert into test values (1,'test','2018-09-17 16:10:28');

create table LSB_abc as select * from test;

create or replace procedure p1() is
begin
insert into LSB_abc values(1,'test','2018-09-17 16:10:28');
end;
/

create or replace procedure P1() is
begin
insert into LSB_abc values(1,'test','2018-09-17 16:10:28');
end;
/

call p1();
select * from LSB_abc;
call P1();
select * from LSB_abc;


drop procedure if exists p1;
drop table test;
drop table LSB_abc;