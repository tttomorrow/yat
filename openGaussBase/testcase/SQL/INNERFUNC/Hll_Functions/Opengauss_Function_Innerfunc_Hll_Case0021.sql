-- @testpoint: hll_hash_text(text),对text类型数据计算哈希值

select hll_hash_text(1);
select hll_hash_text('ab');
select hll_hash_text('ab@-#$');
select hll_hash_text('天天开心');