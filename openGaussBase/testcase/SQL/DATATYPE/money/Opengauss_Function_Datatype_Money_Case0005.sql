-- @testpoint: 插入浮点数，小数点后位数长度截取，只保留两位

drop table if exists test_money05;
create table test_money05 (name money);
insert into test_money05 values (12.1234567899);
insert into test_money05 values (0.999999999999999);
insert into test_money05 values (12.350000000);
select * from test_money05;
drop table test_money05;
