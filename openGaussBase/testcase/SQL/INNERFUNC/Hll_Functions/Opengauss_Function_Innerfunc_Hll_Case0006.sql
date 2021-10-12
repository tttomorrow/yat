-- @testpoint: 函数hll_hash_smallint(smallint)，入参为非smallint类型时，合理报错

select hll_hash_smallint(-32769);
select hll_hash_smallint(32768);
select hll_hash_smallint('nihao');




