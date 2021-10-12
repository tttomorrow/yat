-- @testpoint: 类型转换函数to_bigint，入参在边界值上、下、其它类型、其它进制、空值、特殊字符等，合理报错





select to_bigint(' ');

select to_bigint('&……%￥#');

select to_bigint('0x6e');

select to_bigint('三七');
