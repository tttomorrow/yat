-- @testpoint: hll_hash_integer(integer),对integer类型数据计算哈希值

select hll_hash_integer(0);
select hll_hash_integer(-2147483648);
select hll_hash_integer(2147483647);
select hll_hash_integer('2147483647');
select hll_hash_integer(false);
select hll_hash_integer(true);