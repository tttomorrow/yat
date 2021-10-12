-- @testpoint: 创建列存表，合理报错

drop table if exists test_uuid_02;
create table test_uuid_02 (id uuid) with(orientation=COLUMN, compression=no);
