-- @testpoint: 插入浮点数，小数点后位数长度截取，只保留两位

drop table if exists test_money05;
create table test_money05 (name money);
select * from test_money05;
drop table test_money05;
