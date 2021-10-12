-- @testpoint: 插入bool类型

drop table if exists bigserial_10;
create table bigserial_10 (name bigserial);
insert into bigserial_10 values ('1');
insert into bigserial_10 values ('0');
insert into bigserial_10 values (true);
insert into bigserial_10 values (false);
select * from bigserial_10;
drop table bigserial_10;