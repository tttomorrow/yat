-- @testpoint: 表达式的输入，合理报错
select coalesce(2<3,1,null,2);
select coalesce(1,2<3,null,2);