-- @testpoint: 创建临时列存表,合理报错

drop table if exists test_uuid_13;
create temporary table test_uuid_13 (id uuid) with(orientation=column, compression=no);