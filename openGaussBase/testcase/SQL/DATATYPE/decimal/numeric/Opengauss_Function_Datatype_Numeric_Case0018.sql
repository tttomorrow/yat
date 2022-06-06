-- @testpoint: 指定精度&标度合理范围值，插入数据超出标度范围值，四舍五入自动截取

drop table if exists numeric_18;
create table numeric_18 (name numeric(6,2));
insert into numeric_18 values (0.123);
insert into numeric_18 values (123.12656);
insert into numeric_18 values (999.999999999);
select * from numeric_18;
drop table numeric_18;