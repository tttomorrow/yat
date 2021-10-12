-- @testpoint: generate_subscripts(array anyarray, dim int, reverse boolean)生成一系列包括给定数组的下标。当reverse为真时，该系列则以相反的顺序返回。

SELECT generate_subscripts('{NULL,1,NULL,2}'::int[], 1,0)as s;
SELECT generate_subscripts('{NULL,1,NULL,2}'::int[], 1,1)as s;