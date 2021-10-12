-- @testpoint: 字符处理函数trim，参数1为非字符串（数字）

select trim(both 2 from '2394812');
select trim(trailing 2 from '243542');
select trim(leading 2 from '24435');

