-- @testpoint: nvl函数参数1不为空，参数2为null
select nvl(1,null);
select nvl('string',null);
select length(nvl(to_date('2018','yyyy'),null));
select nvl(1.1,null);
