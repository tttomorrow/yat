-- @testpoint: 字符处理函数trim，入参数量超过两个时合理报错

select trim(leading '1','2' from '1uoiusf8','2iouf899');
select trim(both '1','2' from '1uoiusf8','2iouf899');
select trim(trailing '1','2' from '1009-02-01');

