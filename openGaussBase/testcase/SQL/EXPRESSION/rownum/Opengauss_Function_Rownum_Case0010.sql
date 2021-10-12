-- @testpoint: 检查rownum的执行计划是否最优 合理报错

drop table if exists teacher;
create table teacher
(
    id int PRIMARY key,
    name varchar(10) not null
);
create or replace procedure insert_data(id_begin in int, name in varchar(10))
as
begin
forall i in 1..10000
insert into teacher values (i + id_begin, name);
end;
/
call insert_data(0, 'aaa');
EXPLAIN analyse select * from teacher;
EXPLAIN analyse select * from teacher where rownum < 10;
drop procedure if exists insert_data;
--清理环境
drop table if exists teacher;