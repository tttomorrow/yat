-- @testpoint: generate_series(start, stop)生成一个数值序列，从start到stop，步长为1。
-- int 类型的参数
SELECT * FROM generate_series(2,4);
-- bigint 类型的参数
SELECT * FROM generate_series(-26,-4);
-- numeric 类型的参数
SELECT * FROM generate_series(263.1234,289.369);