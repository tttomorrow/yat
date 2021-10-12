-- @testpoint: radians函数入参类型及个数校验，合理报错
select radians('你好HELLO');
select radians(90,90);
select radians();