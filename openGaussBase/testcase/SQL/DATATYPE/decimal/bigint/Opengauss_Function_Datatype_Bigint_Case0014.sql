-- @testpoint: 插入0值

drop table if exists bigint14;
create table bigint14 (c1 bigint,c2 bigint,c3 bigint,c4 bigint,c5 bigint);
insert into bigint14 values (0);
insert into bigint14 values (0,0);
insert into bigint14 values (0,0,0);
insert into bigint14 values (0,0,0,0);
insert into bigint14 values (0,0,0,0,0);
select * from bigint14;
drop table bigint14;