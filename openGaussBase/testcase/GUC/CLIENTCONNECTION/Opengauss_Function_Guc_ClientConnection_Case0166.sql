-- @testpoint: ALTER SYSTEM SET方法设置gin_fuzzy_search_limit参数，合理报错
--查看默认
show gin_fuzzy_search_limit;
--设置，报错
ALTER SYSTEM SET gin_fuzzy_search_limit to 2147483647;