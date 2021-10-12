-- @testpoint: 创建本地列存临时表，精度在合理范围值内，插入数据

drop table if exists dec_13;
create temporary table dec_13 (id dec(4,2)) with (orientation=column, compression=no);
insert into dec_13 values (11.11);
insert into dec_13 values (23.00);
insert into dec_13 values (1.1);
select * from dec_13;
drop table dec_13;