--  @testpoint:收集文献统计相关函数测试
--ts_stat函数
SELECT ts_stat('select ''hello world''::tsvector');
SELECT ts_stat('select ''hello:2A world:3 world''::tsvector');