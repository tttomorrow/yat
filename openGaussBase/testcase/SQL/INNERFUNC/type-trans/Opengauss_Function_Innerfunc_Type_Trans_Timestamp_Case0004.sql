-- @testpoint: 类型转换函数to_timestamp(string [,fmt])，字符串string按fmt指定的格式转换成时间戳类型的值

select to_timestamp('05 dec 2000', 'dd mon yyyy');
