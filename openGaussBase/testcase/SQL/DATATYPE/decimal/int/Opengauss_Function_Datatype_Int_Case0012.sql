-- @testpoint: 插入浮点数，四舍五入取整

drop table if exists int12;
create table int12 (name int);
insert into int12 values (122.3340);
insert into int12 values (99999.99999);
insert into int12 values (-122.3340);
insert into int12 values (-99999.99999);
select * from int12;
drop table int12;