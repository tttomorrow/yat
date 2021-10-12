-- @testpoint: degrees函数入参个数及类型校验，合理报错
select degrees('hello你好');
select degrees();
select degrees(1,99);