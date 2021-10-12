-- @testpoint: hll_hash_text(text),对text类型数据计算哈希值,入参为非text类型时合理报错

select hll_hash_text(天天开心);
select hll_hash_text(`天天开心`);
select hll_hash_text("天天开心");