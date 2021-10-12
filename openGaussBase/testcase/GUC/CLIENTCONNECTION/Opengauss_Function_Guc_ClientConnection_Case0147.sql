-- @testpoint: set方法设置参数extra_float_digits为负数，建表查询
--查看默认值
show extra_float_digits;
--设置为负数,表示消除不需要的数据位
set extra_float_digits to -15;
--建表并插入数据
drop table if exists float_type_t147;
create table float_type_t147 (FT_COL2 FLOAT4);
insert into float_type_t147 values(10.365456);
--查询
select * from float_type_t147;
--清理环境
set extra_float_digits to 0;
drop table if exists float_type_t147;