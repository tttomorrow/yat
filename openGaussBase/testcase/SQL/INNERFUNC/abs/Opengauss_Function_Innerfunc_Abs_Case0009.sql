-- @testpoint: 定义函数，结合函数的使用
drop table if exists t_abs;
create table t_abs(c_id int);
insert into t_abs VALUES(002);
insert into t_abs VALUES(125);
insert into t_abs VALUES(056);
insert into t_abs VALUES(089);
insert into t_abs VALUES(256);
insert into t_abs VALUES(089);
insert into t_abs VALUES(256);
insert into t_abs VALUES(123);
create or replace function f_abs(id int)
return int
as
begin
    return abs(id);
end;
/
select f_abs(-99) from sys_dummy;
select c_id from t_abs where c_id is not null and f_abs(-99)= 99;
drop function f_abs;
drop table if exists t_abs;