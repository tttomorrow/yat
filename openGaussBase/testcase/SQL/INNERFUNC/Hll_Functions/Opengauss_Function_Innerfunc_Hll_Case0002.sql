-- @testpoint: 函数hll_hash_boolean(bool)，对bool类型数据计算哈希值，入参为其他类型时，合理报错

select hll_hash_boolean('12');
select hll_hash_boolean('nihao');
select hll_hash_boolean('你好');
select hll_hash_boolean(@);