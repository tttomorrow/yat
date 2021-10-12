-- @testpoint: 指定精度在合理范围值内，插入数值超出范围，自动截取
-- @modified at:2020-11-23

drop table if exists float04;
create table float04 (name float(5));
select * from float04;
drop table float04;
