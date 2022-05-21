-- @testpoint: 类型转换函数to_timestamp(double precision)，把unix纪元转换成时间戳，入参为有效值


select to_timestamp(0);
select to_timestamp(1);
select to_timestamp(10);
select to_timestamp(1111);
select to_timestamp(1284352325);
select to_timestamp(12346789.12);
select to_timestamp(-9998);