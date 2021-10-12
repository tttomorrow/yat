-- @testpoint: nvl函数参数1为null，参数2不为null
select nvl(null,1);
select nvl(null,'string');
select length(nvl(null,to_date('2018','yyyy')));
select length(to_date('2018','yyyy'));
