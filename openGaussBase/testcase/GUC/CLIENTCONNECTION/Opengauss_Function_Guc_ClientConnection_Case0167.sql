-- @testpoint: set方法设置参数gin_fuzzy_search_limit，无效值时，合理报错
--查看默认
show gin_fuzzy_search_limit;
--设置，成功
set gin_fuzzy_search_limit to 2147483647;
--设置，报错
set gin_fuzzy_search_limit to 'test';
set gin_fuzzy_search_limit to '2147483647%$#';
set gin_fuzzy_search_limit to '-1';
set gin_fuzzy_search_limit to '2147483648';
set gin_fuzzy_search_limit to '';
--no need to clean