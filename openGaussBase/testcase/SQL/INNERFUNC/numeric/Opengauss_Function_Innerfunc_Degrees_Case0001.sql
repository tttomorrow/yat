-- @testpoint: degrees函数入参为特殊值
select degrees(0);
select degrees(1);
select degrees(-1);
select degrees(pi());
select degrees(pi()/2);
select degrees(4*pi());
select degrees(5*pi()/2);