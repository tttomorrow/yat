-- @testpoint: 创建视图，query语句使用values
--创建视图
create or replace view temp_view_025 as values(8,'worlcxcd');
--查询视图
select * from temp_view_025;
--删除视图
drop view temp_view_025;
