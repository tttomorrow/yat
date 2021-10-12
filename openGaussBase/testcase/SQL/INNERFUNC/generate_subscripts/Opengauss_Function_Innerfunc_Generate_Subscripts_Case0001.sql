-- @testpoint: generate_subscripts(array anyarray, dim int)生成一系列包括给定数组的下标
SELECT generate_subscripts('{NULL,1,NULL,2}'::int[], 1)as s;