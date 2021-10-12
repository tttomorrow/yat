-- @testpoint: 入参为null或''，分组求标准差
select STDDEV_SAMP(null);
select STDDEV_SAMP('');