-- @testpoint: hll_hashval_ne(hll_hashval, hll_hashval),比较两个hll_hashval类型数据是否不相等

select hll_hashval_ne(hll_hash_text('ab', 214748367),hll_hash_bigint(0));
select hll_hashval_ne(hll_hash_text('天天开心', 10),hll_hash_text('天天开心', 10));
