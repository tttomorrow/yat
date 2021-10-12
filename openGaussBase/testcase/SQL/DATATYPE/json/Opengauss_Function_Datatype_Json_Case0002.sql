-- @testpoint: 创建普通列存表，插入数据，合理报错

drop table if exists test_json_02;
create table test_json_02 (id json) with(orientation=column,compression=no);
