-- @testpoint: hll_hash_text(text, int32),对text类型数据计算哈希值, 并设置hashseed（即改变哈希策略）

select hll_hash_text(1, 2147483647);
select hll_hash_text('ab', 2147483647);
select hll_hash_text('ab@-#$', 0);
select hll_hash_text('天天开心', 10);