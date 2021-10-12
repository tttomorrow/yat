-- @testpoint: 使用bigint别名int8

drop table if exists bigint16;
create table bigint16 (name int8);
insert into bigint16 values (123);
insert into bigint16 values (9999.8888);
insert into bigint16 values (-23668);
insert into bigint16 values (-0.000012);
select * from bigint16;
drop table bigint16;