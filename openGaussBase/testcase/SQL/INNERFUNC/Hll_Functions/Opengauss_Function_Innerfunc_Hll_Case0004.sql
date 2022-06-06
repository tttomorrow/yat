-- @testpoint: 函数hll_hash_boolean(bool, int32) ,入参为其他类型时，合理报错

--入参1为其他类型,入参2为int类型
select hll_hash_boolean('nihao', 10);
select hll_hash_boolean('12', 0);
select hll_hash_boolean('你好', 2147483647);
select hll_hash_boolean(@,10);

--入参2为其他类型，入参1为bool类型
select hll_hash_boolean('yes', 2147483648);
select hll_hash_boolean(true, 'nihao');
select hll_hash_boolean(true, @#);
select hll_hash_boolean(true, -1);
select hll_hash_boolean('no', 'no');