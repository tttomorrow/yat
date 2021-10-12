--  @testpoint:使用自定义序列（Sequence）向表插入数据
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
--查询book表中数据（id列自动以等差为1递增）
SELECT * FROM book;
--删除表
drop table book;
--删除序列
 drop SEQUENCE book_id_seq;

