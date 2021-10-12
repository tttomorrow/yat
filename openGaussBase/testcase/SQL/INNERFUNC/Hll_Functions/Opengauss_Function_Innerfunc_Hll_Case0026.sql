-- @testpoint: hll_hash_any(anytype), 对任意类型数据计算哈希值,当对数据类型不进行强制转换时,合理报错

select hll_hash_any ('clusterName');