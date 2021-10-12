-- @testpoint: 插入bool类型

drop table if exists int06;
create table int06 (name int);
insert into int06 values (false);
insert into int06 values (true);
select * from int06;
drop table int06;