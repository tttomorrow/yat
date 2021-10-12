--  @testpoint:序列和表关联，删除序列分别添加CASCADE和不添加CASCADE，注意提示不同
--创建Book表
drop table if exists book;
CREATE TABLE book(
  id INTEGER PRIMARY KEY ,
  name CHARACTER VARYING(50),
  price DOUBLE PRECISION,
  author CHARACTER VARYING(20)
 );
 --创建自动增长序列
 drop SEQUENCE if exists book_id_seq;
 CREATE SEQUENCE book_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
 --为book表添加自动增长序列
 ALTER TABLE book ALTER COLUMN id SET DEFAULT nextval('book_id_seq');
 --向book表插入数据
INSERT INTO public.book VALUES (nextval('book_id_seq'),'《本色》',30.5,'乐嘉');
INSERT INTO public.book VALUES (nextval('book_id_seq'),'《平凡世界》',90.5,'路遥');
INSERT INTO public.book VALUES (nextval('book_id_seq'),'《Java编程思想》',60.5,'詹姆斯·高斯林');
--删除序列，不添加CASCADE，合理报错
drop SEQUENCE book_id_seq;
--删除序列添加RESTRICT，合理报错
drop SEQUENCE book_id_seq RESTRICT;
--删除序列，添加CASCADE，删除成功
drop SEQUENCE book_id_seq CASCADE;
--删表
drop table  book;