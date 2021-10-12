-- @testpoint: 插入字符串形式有效数值
-- @remarks: 默认会将插入的值隐式转换为bigint形式，且bigserial数据类型取值>1

drop table if exists bigserial_04;
create table bigserial_04 (name bigserial);
insert into bigserial_04 values ('00123');
insert into bigserial_04 values ('456');
insert into bigserial_04 values ('11235569');
select * from bigserial_04;
drop table bigserial_04;
