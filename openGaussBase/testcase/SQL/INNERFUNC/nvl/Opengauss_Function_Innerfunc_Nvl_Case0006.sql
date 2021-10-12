-- @testpoint: nvl函数参数二能隐式转换为第一个参数的类型
select nvl(1,'222');
select nvl('string',1);