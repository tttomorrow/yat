-- @testpoint: 创建临时表列存表,合理报错

drop table if exists test_json_13;
create local temporary table test_json_13 (id json) with (orientation=column, compression=no);
