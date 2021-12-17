-- @testpoint: 插入数值超出精度范围，自动截取

drop table if exists float8_04;
create table float8_04 (name float8);
insert into float8_04 values (14165132.111111111111111111111);
insert into float8_04 values (0.123456789123456789);
insert into float8_04 values (-14165132.999999999999999999999);
insert into float8_04 values (-0.123456789123456789);
select * from float8_04;
drop table float8_04;
