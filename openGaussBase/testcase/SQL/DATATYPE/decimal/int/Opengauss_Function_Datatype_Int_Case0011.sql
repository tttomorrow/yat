-- @testpoint: 插入负整数

drop table if exists int11;
create table int11 (name int);
insert into int11 values (-1223340);
insert into int11 values (-999999999);
insert into int11 values (-1);
insert into int11 values (-2);
insert into int11 values (-3);
select * from int11;
drop table int11;