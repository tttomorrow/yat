-- @testpoint: 插入数值超出精度范围，自动截取

drop table if exists float8_04;
create table float8_04 (name float8);
select * from float8_04;
drop table float8_04;
