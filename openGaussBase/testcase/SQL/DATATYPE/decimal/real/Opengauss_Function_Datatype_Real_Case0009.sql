-- @testpoint: 插入0值

drop table if exists real_09;
create table real_09 (name real);
insert into real_09 values (0);
insert into real_09 values (0);
insert into real_09 values (0);
select * from real_09;
drop table real_09;