-- @testpoint: 字符处理函数trim，参数1不在参数2指定位置

select trim(both 'T' from 'xTomxx');
select trim(both 'w' from 'xTomxx');
select trim(leading 'w' from 'xTomxx');
select trim(leading 'T' from 'xTomxx');
select trim(trailing 'w' from 'xTomxx');
select trim(trailing 'T' from 'xTomxx');

