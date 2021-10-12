-- @testpoint: 设置为空串（''）的时候，系统会自动转换成一对双引号
set search_path to '';
--查看
show search_path;
--恢复默认
set search_path to "$user",public;
show search_path;