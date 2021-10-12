-- @testpoint: 字符处理函数trim，参数2为算数表达式

select trim(trailing '1' from 2-1);
select trim(both '1' from 2-1);
select trim(leading '1' from 1-0);
select trim(both '1' from 2+1);
select trim(leading '1' from 1+3);
select trim(leading '1' from 1-3);

