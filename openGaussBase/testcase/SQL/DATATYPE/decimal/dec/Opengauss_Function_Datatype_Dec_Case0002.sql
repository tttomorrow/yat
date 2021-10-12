-- @testpoint: 创建列存普通表，精度在合理范围值内，插入数据

drop table if exists dec_02;
create table dec_02 (id dec(4,2)) with (orientation=column, compression=no);
insert into dec_02 values (11.11);
insert into dec_02 values (23.00);
insert into dec_02 values (1.1);
select * from dec_02;
drop table dec_02;