-- @testpoint: 字符处理函数trim，入参取非字符串（字母），合理报错

select trim(both 'x' from xtomxx);
select trim(leading 'x' from xtomxx);
select trim(trailing 'x' from xtomxx);
select trim(trailing x from 'xtomxx');
select trim(leading x from 'xtomxx');
select trim(both x from 'xtomxx');


