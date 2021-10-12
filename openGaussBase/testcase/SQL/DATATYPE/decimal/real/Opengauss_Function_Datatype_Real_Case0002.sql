-- @testpoint: 插入负整数

drop table if exists real_02;
create table real_02 (name real);
insert into real_02 values (-1212);
insert into real_02 values (-999999);
insert into real_02 values (-1);
insert into real_02 values (-2);
insert into real_02 values (-3);
select * from real_02;
drop table real_02;
