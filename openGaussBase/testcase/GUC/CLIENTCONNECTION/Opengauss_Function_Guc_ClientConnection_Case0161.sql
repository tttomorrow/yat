-- @testpoint: set方法设置参数default_text_search_config，无效值时，合理报错
--查看默认
show default_text_search_config;
--设置，成功
set default_text_search_config to 'pg_catalog.simple';
show default_text_search_config;
--设置，报错
set default_text_search_config to 123;
set default_text_search_config to 'test';
set default_text_search_config to 'pg_catalog.simple%$#';
--no need to clean