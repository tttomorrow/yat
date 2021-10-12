-- @testpoint: 入参为null或''，求数据集的标准差

select STDDEV_POP(null);
select STDDEV_POP('');