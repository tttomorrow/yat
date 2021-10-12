-- @testpoint: 插入bool类型

drop table if exists bigint11;
create table bigint11 (name bigint);
insert into bigint11 values ('1');
insert into bigint11 values ('0');
insert into bigint11 values (true);
insert into bigint11 values (false);
select * from bigint11;
drop table bigint11;