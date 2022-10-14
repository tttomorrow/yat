-- @testpoint: 验证增删分区原语法和MySQL兼容语法对普通表执行，合理报错
drop table if exists b_table_t1;
create table b_table_t1(c1 int,c2 text);
insert into b_table_t1 values(1,'a'),(2,'b'),(3,'c');
-- 原语法合理报错
alter table b_table_t1 add partition p1 values less than (1); 
alter table b_table_t1 add partition p1 values(1);
alter table b_table_t1 add partition p1 values(1),add partition p2 values(2);
alter table b_table_t1 drop partition p1,drop partition p2;
-- MySQL语法合理报错
alter table b_table_t1 add partition (partition p1 values less than (1));
alter table b_table_t1 add partition (partition p1 values(1));
alter table b_table_t1 add partition (partition p1 values(1),partition p2 values(2));
alter table b_table_t1 drop partition p1,p2;
drop table b_table_t1;
