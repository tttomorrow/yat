-- @testpoint: 插入浮点数，四舍五入

drop table if exists bigint03;
create table bigint03 (name bigint);
insert into bigint03 values (2.00000000001);
insert into bigint03 values (122.3340);
insert into bigint03 values (-2.03);
insert into bigint03 values (-122.3340);
select * from bigint03;
drop table bigint03;
