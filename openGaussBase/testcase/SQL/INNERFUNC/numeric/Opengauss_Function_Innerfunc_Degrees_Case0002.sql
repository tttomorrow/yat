-- @testpoint: degrees函数入参为合法数值类型
select degrees(255);
select degrees(-32768);
select degrees(32767);
select degrees(999.999);
select degrees(888/3);
select degrees(-8888/1111);
select degrees(5*5*7/5+3);