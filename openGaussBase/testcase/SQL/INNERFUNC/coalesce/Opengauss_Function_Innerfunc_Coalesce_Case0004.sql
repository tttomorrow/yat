-- @testpoint: 字符串的输入，合理报错
select coalesce('aaa',1,null,2);