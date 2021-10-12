--  @testpoint:to_tsvector函数结合表测试
 ---创建schema
 drop SCHEMA if EXISTS tsearch cascade;
 CREATE SCHEMA tsearch;
 --建表
 drop TABLE if EXISTS tt;
 CREATE TABLE tsearch.tt (id int, title text, keyword text, abstract text, body text, ti tsvector);
 INSERT INTO tsearch.tt(id, title, keyword, abstract, body) VALUES (1, 'China', 'Beijing', 'China','China, officially the People''s Republic of China (PRC), located in Asia, is the world''s most populous state.');

 UPDATE tsearch.tt SET ti =
    setweight(to_tsvector(coalesce(title,'')), 'A')    ||
    setweight(to_tsvector(coalesce(keyword,'')), 'B')  ||
    setweight(to_tsvector(coalesce(abstract,'')), 'C') ||
    setweight(to_tsvector(coalesce(body,'')), 'D');

 SELECT ti from tsearch.tt WHERE to_tsquery('officially') @@ ti;
 --删除表
 drop TABLE tsearch.tt;
 --删除schema
 drop SCHEMA tsearch;