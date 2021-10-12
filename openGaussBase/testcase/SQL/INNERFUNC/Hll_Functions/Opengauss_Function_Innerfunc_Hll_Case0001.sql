-- @testpoint: 函数hll_hash_boolean(bool)，对bool类型数据计算哈希值

select hll_hash_boolean(true);
select hll_hash_boolean('t');
select hll_hash_boolean(1);
select hll_hash_boolean('y');
select hll_hash_boolean('yes');
select hll_hash_boolean('1');

select hll_hash_boolean(false);
select hll_hash_boolean('f');
select hll_hash_boolean(0);
select hll_hash_boolean('0');
select hll_hash_boolean('n');
select hll_hash_boolean('no');