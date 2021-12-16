-- @testpoint: 指定精度在合理范围值内，插入数值超出范围，自动截取

drop table if exists float04;
create table float04 (name float(5));
insert into float04 values (14165132.9999999999999999999999);
insert into float04 values (-14165132.999999999999999999999);
insert into float04 values (0.123456123456);
insert into float04 values (-9.876543210);
select * from float04;
drop table float04;
