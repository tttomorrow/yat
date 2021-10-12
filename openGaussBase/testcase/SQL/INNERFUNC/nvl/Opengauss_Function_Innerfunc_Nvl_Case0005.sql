-- @testpoint: nvl函数参数二不能隐式转换为第一个参数的类型，合理报错
select nvl(1,'string');
select nvl(1,'o2');