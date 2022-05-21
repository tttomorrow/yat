-- @testpoint: to_timestamp(double precision)把unix纪元转换成时间戳，入参为无效值时合理报错

select to_timestamp('0x5f');
select to_timestamp('999888762478.6427868173489');
select to_timestamp(-999888762478);
select to_timestamp(-#&%#^5);
select to_timestamp();