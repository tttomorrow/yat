-- @testpoint: generate_series(start, stop, step)生成一个数值序列，从start到stop，步长为step。
-- int 类型的参数
SELECT * FROM generate_series(2,18,4);
-- bigint 类型的参数
SELECT * FROM generate_series(-26,-4,6);
-- numeric 类型的参数
SELECT * FROM generate_series(263.1234,289.369,10);