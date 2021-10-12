-- @testpoint: nvl函数俩参数类型相同且不为空
select nvl(1,1);
select nvl('sting','m');
select length(nvl(to_date('2018','yyyy'),to_date('2018','yyyy')));
select nvl(1,1);
select nvl('sting','m');
select length(nvl(to_date('2018','yyyy'),to_date('2018','yyyy')));